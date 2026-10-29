<?php
// JSON API for the native Android app (Capacitor). Auth: "Authorization: Bearer <app token>" (only sha256 stored),
// so no cookies and no CSRF. Files are fetched with short-lived signed URLs (a <video> tag cannot send headers).
declare(strict_types=1);

const APP_ORIGINS = ['https://localhost', 'http://localhost', 'capacitor://localhost'];

function route_app(string $m, string $path): void
{
    header('X-Content-Type-Options: nosniff');
    header('Cache-Control: no-store');
    $origin = (string) ($_SERVER['HTTP_ORIGIN'] ?? '');
    if (in_array($origin, array_merge(APP_ORIGINS, (array) config('app_dev_origins', [])), true)) {
        header('Access-Control-Allow-Origin: ' . $origin);
        header('Vary: Origin');
        header('Access-Control-Allow-Headers: Authorization, Content-Type, Range');
        header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
        header('Access-Control-Expose-Headers: Content-Range, Content-Length');
        header('Access-Control-Max-Age: 86400');
    }
    if ($m === 'OPTIONS') {
        http_response_code(204);
        exit;
    }
    $ip = client_ip();
    $in = [];
    if ($m === 'POST' && $path !== '/upload/chunk') {
        $in = json_decode((string) file_get_contents('php://input'), true);
        $in = is_array($in) ? $in : [];
    }
    $s = fn(string $k) => is_string($in[$k] ?? null) ? trim($in[$k]) : '';

    // ---- Public endpoints ----
    if ($path === '/config' && $m === 'GET') {
        json_out(app_config());
    }
    if (preg_match('#^/files/(\d+)$#', $path, $fm) && $m === 'GET') {
        // Signed link: /files/ID?exp=<unix>&u=<user id>&sig=<hmac>
        $f = row('SELECT * FROM files WHERE id = ?', [(int) $fm[1]]);
        $uid = (int) ($_GET['u'] ?? 0);
        $exp = (int) ($_GET['exp'] ?? 0);
        if (!$f || $exp < time() || !hash_equals(file_sig((int) $f['id'], $uid, $exp), (string) ($_GET['sig'] ?? ''))) {
            json_out(['error' => 'Link expired. Reload.'], 403);
        }
        rate_limit_or_abort("dl:$uid", 600, 3600, true);
        send_file($f, ($_GET['dl'] ?? '') === '1', 'u' . $uid, 2);
    }
    if ($path === '/register' && $m === 'POST') {
        rate_limit_or_abort("register:$ip", 5, 3600, true);
        $r = register_user($s('name'), $s('email'), $s('phone'), (string) ($in['password'] ?? ''), $s('currency'));
        if (isset($r['errors'])) {
            json_out(['error' => implode(' ', $r['errors'])], 400);
        }
        $u = row('SELECT * FROM users WHERE id = ?', [$r['id']]);
        if ($u['status'] !== 'active') {
            json_out(['pending' => true, 'message' => 'Account created. You can log in as soon as we approve it.']);
        }
        json_out(['token' => issue_app_token((int) $u['id'], $s('device')), 'user' => app_user($u)]);
    }
    if ($path === '/login' && $m === 'POST') {
        rate_limit_or_abort("login:$ip", 10, 900, true);
        rate_limit_or_abort('loginmail:' . strtolower($s('email')), 10, 900, true);
        $u = row('SELECT * FROM users WHERE email = ?', [strtolower($s('email'))]);
        $ok = password_verify((string) ($in['password'] ?? ''), $u['password_hash'] ?? dummy_hash());
        if (!$u || !$ok || $u['status'] === 'blocked') {
            json_out(['error' => 'Wrong email or password.'], 401);
        }
        if ($u['status'] !== 'active') {
            json_out(['error' => 'Your account is waiting for approval.'], 403);
        }
        update('users', ['last_login_at' => now()], 'id = ?', [$u['id']]);
        json_out(['token' => issue_app_token((int) $u['id'], $s('device')), 'user' => app_user($u)]);
    }
    if ($path === '/forgot' && $m === 'POST') {
        rate_limit_or_abort("forgot:$ip", 5, 3600, true);
        rate_limit_or_abort('forgotmail:' . strtolower($s('email')), 3, 3600, true);
        start_password_reset($s('email'));
        json_out(['ok' => true, 'message' => 'If an account with that email exists, we sent a link to set a new password.']);
    }

    // ---- Logged-in endpoints ----
    $user = app_auth();
    rate_limit_or_abort("app:{$user['id']}", 3000, 3600, true);

    if ($path === '/me' && $m === 'GET') {
        json_out(['user' => app_user($user)] + app_config());
    }
    if ($path === '/logout' && $m === 'POST') {
        q('DELETE FROM app_tokens WHERE id = ?', [$user['_token_id']]);
        json_out(['ok' => true]);
    }
    if ($path === '/password' && $m === 'POST') {
        if (!password_verify((string) ($in['current'] ?? ''), $user['password_hash'])) {
            json_out(['error' => 'Current password is wrong.'], 400);
        }
        if ($e = validate_password((string) ($in['new'] ?? ''))) {
            json_out(['error' => $e], 400);
        }
        set_password((int) $user['id'], (string) $in['new'], false);
        // Other app devices are logged out too; this device keeps a fresh token.
        q('DELETE FROM app_tokens WHERE user_id = ?', [$user['id']]);
        json_out(['ok' => true, 'token' => issue_app_token((int) $user['id'], 'app')]);
    }
    if ($path === '/orders' && $m === 'GET') {
        $list = rows('SELECT * FROM orders WHERE user_id = ? ORDER BY updated_at DESC', [$user['id']]);
        json_out(['orders' => array_map(fn($o) => app_order_summary($o), $list)]);
    }
    if ($path === '/orders' && $m === 'POST') {
        rate_limit_or_abort("neworder:{$user['id']}", 20, 3600, true);
        $id = create_draft($user);
        json_out(['order' => app_order($id, $user)]);
    }
    if (preg_match('#^/orders/(\d+)$#', $path, $mm) && $m === 'GET') {
        order_for_user_json((int) $mm[1], $user);
        json_out(['order' => app_order((int) $mm[1], $user)]);
    }
    if (preg_match('#^/orders/(\d+)/save$#', $path, $mm) && $m === 'POST') {
        $o = order_for_user_json((int) $mm[1], $user);
        if ($o['status'] !== 'draft') {
            json_out(['error' => 'This order was already sent.'], 400);
        }
        $post = ['title' => $s('title'), 'length_sec' => (int) ($in['length_sec'] ?? 0), 'script' => (string) ($in['script'] ?? ''),
            'ideas' => (string) ($in['ideas'] ?? ''), 'q' => is_array($in['q'] ?? null) ? $in['q'] : []];
        $errors = save_order_form($o, $user, $post, !empty($in['submit']));
        if ($errors) {
            json_out(['error' => implode(' ', $errors), 'errors' => $errors], 400);
        }
        json_out(['order' => app_order((int) $o['id'], $user)]);
    }
    if (preg_match('#^/orders/(\d+)/(changes|approve|message)$#', $path, $mm) && $m === 'POST') {
        $o = order_for_user_json((int) $mm[1], $user);
        rate_limit_or_abort("msg:{$user['id']}", 30, 3600, true);
        $body = (string) ($in['body'] ?? '');
        $err = match ($mm[2]) {
            'changes' => request_changes($o, $body),
            'approve' => approve_order($o, $body),
            'message' => client_message($o, $body),
        };
        if ($err) {
            json_out(['error' => $err], 400);
        }
        json_out(['order' => app_order((int) $o['id'], $user)]);
    }
    if (preg_match('#^/orders/(\d+)/files/(\d+)/delete$#', $path, $mm) && $m === 'POST') {
        $o = order_for_user_json((int) $mm[1], $user);
        $f = row("SELECT * FROM files WHERE id = ? AND order_id = ? AND kind = 'input'", [(int) $mm[2], $o['id']]);
        if ($f && $o['status'] === 'draft') {
            delete_file($f);
        }
        json_out(['order' => app_order((int) $o['id'], $user)]);
    }
    if ($path === '/upload/init' && $m === 'POST') {
        $o = order_for_user_json((int) ($in['order_id'] ?? 0), $user);
        if ($o['status'] === 'approved') {
            json_out(['error' => 'This order is closed.'], 400);
        }
        $r = upload_init((int) $o['id'], 'input', 'client', $s('name'), (int) ($in['size'] ?? 0));
        json_out($r, isset($r['error']) ? 400 : 200);
    }
    if (in_array($path, ['/upload/chunk', '/upload/finish'], true) && $m === 'POST') {
        $up = row("SELECT * FROM uploads WHERE token = ? AND kind = 'input'", [(string) ($_GET['token'] ?? '')]);
        if (!$up) {
            json_out(['error' => 'Upload not found. Start again.'], 404);
        }
        order_for_user_json((int) $up['order_id'], $user);
        $r = $path === '/upload/chunk' ? upload_chunk($up, (int) ($_GET['offset'] ?? -1)) : upload_finish($up);
        json_out($r, isset($r['error']) ? ($path === '/upload/chunk' ? 409 : 400) : 200);
    }
    json_out(['error' => 'Unknown endpoint'], 404);
}

function issue_app_token(int $userId, string $device): string
{
    $t = 'pa_' . bin2hex(random_bytes(32));
    insert('app_tokens', ['user_id' => $userId, 'token_hash' => hash('sha256', $t), 'device' => mb_substr($device, 0, 80),
        'created_at' => now(), 'last_used_at' => now()]);
    return $t;
}

function app_auth(): array
{
    $h = (string) ($_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '');
    if (!preg_match('/^Bearer\s+(pa_[a-f0-9]{64})$/', $h, $mm)) {
        rate_limit_or_abort('appfail:' . client_ip(), 30, 900, true);
        json_out(['error' => 'Please log in again.', 'auth' => false], 401);
    }
    $t = row('SELECT * FROM app_tokens WHERE token_hash = ?', [hash('sha256', $mm[1])]);
    // Tokens die after 90 days without use.
    if ($t && strtotime($t['last_used_at'] . ' UTC') < time() - 90 * 86400) {
        q('DELETE FROM app_tokens WHERE id = ?', [$t['id']]);
        $t = null;
    }
    $u = $t ? row("SELECT * FROM users WHERE id = ? AND status = 'active'", [$t['user_id']]) : null;
    if (!$u) {
        rate_limit_or_abort('appfail:' . client_ip(), 30, 900, true);
        json_out(['error' => 'Please log in again.', 'auth' => false], 401);
    }
    if (strtotime($t['last_used_at'] . ' UTC') < time() - 3600) {
        update('app_tokens', ['last_used_at' => now()], 'id = ?', [$t['id']]);
    }
    $u['_token_id'] = (int) $t['id'];
    return $u;
}

function order_for_user_json(int $id, array $user): array
{
    $o = row('SELECT * FROM orders WHERE id = ? AND user_id = ?', [$id, $user['id']]);
    if (!$o) {
        json_out(['error' => 'Not found'], 404);
    }
    return $o;
}

function file_sig(int $fileId, int $userId, int $exp): string
{
    $secret = setting('app_secret');
    if ($secret === '') {
        $secret = bin2hex(random_bytes(32));
        set_setting('app_secret', $secret);
    }
    return hash_hmac('sha256', "$fileId|$userId|$exp", $secret);
}

function signed_file_url(int $fileId, int $userId): string
{
    $exp = time() + 6 * 3600;
    return site_url("api/v1/files/$fileId?u=$userId&exp=$exp&sig=" . file_sig($fileId, $userId, $exp));
}

function app_user(array $u): array
{
    return ['id' => (int) $u['id'], 'name' => $u['name'], 'email' => $u['email'], 'phone' => $u['phone'],
        'currency' => $u['currency'], 'rate' => rate_for($u, $u['currency']), 'role' => $u['role']];
}

function app_config(): array
{
    $qs = [];
    foreach (questions() as $k => $q) {
        $qs[] = ['key' => $k] + $q;
    }
    return [
        'brand' => setting('brand_name'), 'splash' => setting('splash_subtitle'), 'tagline' => setting('brand_tagline'),
        'support' => setting('support_contact'), 'privacy' => setting('privacy_text'),
        'questions' => $qs, 'statuses' => ORDER_STATUSES, 'max_file_mb' => (int) setting('max_file_mb'),
        'app' => ['native_version' => (int) setting('app_version'), 'apk_url' => is_file(storage_dir() . '/app/app.apk') ? site_url('app/download') : null,
            'notes' => setting('app_notes'), 'bundle_version' => setting('bundle_version'),
            'bundle_url' => is_file(storage_dir() . '/app/bundle.zip') ? site_url('app/bundle.zip') : null,
            'bundle_sha256' => setting('bundle_sha256'), 'bundle_min_native' => (int) setting('bundle_min_native')],
    ];
}

function app_order_summary(array $o): array
{
    return ['id' => (int) $o['id'], 'title' => $o['title'], 'status' => $o['status'], 'length_sec' => (int) $o['length_sec'],
        'currency' => $o['currency'], 'price' => (float) ($o['final_price'] ?? $o['estimate']), 'price_is_final' => $o['final_price'] !== null,
        'updated_at' => $o['updated_at']];
}

function app_order(int $id, array $user): array
{
    $o = row('SELECT * FROM orders WHERE id = ?', [$id]);
    $uid = (int) $user['id'];
    $files = [];
    foreach (rows('SELECT * FROM files WHERE order_id = ? ORDER BY id', [$id]) as $f) {
        // Outputs only once delivered as a version.
        if ($f['kind'] === 'output' && !row('SELECT id FROM versions WHERE file_id = ?', [$f['id']])) {
            continue;
        }
        $files[] = ['id' => (int) $f['id'], 'kind' => $f['kind'], 'name' => $f['orig_name'], 'mime' => $f['mime'], 'size' => (int) $f['size'],
            'url' => signed_file_url((int) $f['id'], $uid)];
    }
    $versions = [];
    foreach (rows('SELECT v.*, f.mime, f.size, f.orig_name FROM versions v JOIN files f ON f.id = v.file_id WHERE v.order_id = ? ORDER BY v.number DESC', [$id]) as $v) {
        $versions[] = ['id' => (int) $v['id'], 'number' => (int) $v['number'], 'note' => $v['note'], 'created_at' => $v['created_at'],
            'file_id' => (int) $v['file_id'], 'mime' => $v['mime'], 'size' => (int) $v['size'], 'name' => $v['orig_name'],
            'url' => signed_file_url((int) $v['file_id'], $uid)];
    }
    $msgs = array_map(fn($x) => ['id' => (int) $x['id'], 'from' => $x['sender'] === 'client' ? 'me' : 'studio', 'kind' => $x['kind'],
        'body' => $x['body'], 'created_at' => $x['created_at']], rows('SELECT * FROM messages WHERE order_id = ? ORDER BY id', [$id]));
    return app_order_summary($o) + ['rate' => (float) $o['rate'], 'estimate' => (float) $o['estimate'], 'answers' => order_answers($o),
        'script' => (string) $o['script'], 'ideas' => (string) $o['ideas'], 'files' => $files, 'versions' => $versions, 'messages' => $msgs,
        'submitted_at' => $o['submitted_at']];
}
