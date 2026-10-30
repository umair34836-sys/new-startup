<?php
// Bridge API for the Claude sessions. Auth: "Authorization: Bearer <token>" (only its sha256 is stored).
declare(strict_types=1);

function route_api(string $m, string $path): void
{
    header('X-Content-Type-Options: nosniff');
    $ip = client_ip();
    $hash = setting('bridge_token_hash');
    $sent = '';
    if (preg_match('/^Bearer\s+(\S+)$/', (string) ($_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? ''), $mm)) {
        $sent = $mm[1];
    }
    if ($hash === '' || $sent === '' || !hash_equals($hash, hash('sha256', $sent))) {
        rate_limit_or_abort("apifail:$ip", 20, 900, true);
        json_out(['error' => 'unauthorized'], 401);
    }
    rate_limit_or_abort('api', 6000, 3600, true);
    $body = json_decode((string) ($m === 'POST' && !str_ends_with($path, '/upload/chunk') ? file_get_contents('php://input') : ''), true) ?: [];

    if ($path === '/ping') {
        json_out(['ok' => true, 'brand' => setting('brand_name'), 'chunk' => chunk_bytes(), 'time' => now()]);
    }

    // Open events = work to do: new orders, change requests, client messages, approvals.
    if ($path === '/events' && $m === 'GET') {
        $evs = rows('SELECT * FROM events WHERE done_at IS NULL ORDER BY id LIMIT 50');
        $out = [];
        foreach ($evs as $e) {
            $out[] = ['event' => $e, 'order' => api_order((int) $e['order_id'])];
        }
        json_out(['events' => $out]);
    }

    if (preg_match('#^/events/(\d+)/(take|done)$#', $path, $mm) && $m === 'POST') {
        $e = row('SELECT * FROM events WHERE id = ?', [(int) $mm[1]]) ?? json_out(['error' => 'not found'], 404);
        if ($mm[2] === 'take') {
            update('events', ['taken_at' => now()], 'id = ?', [$e['id']]);
            q("UPDATE orders SET status = 'in_progress', updated_at = ? WHERE id = ? AND status IN ('submitted','revision')", [now(), $e['order_id']]);
        } else {
            update('events', ['done_at' => now()], 'id = ?', [$e['id']]);
        }
        json_out(['ok' => true]);
    }

    if (preg_match('#^/orders/(\d+)$#', $path, $mm) && $m === 'GET') {
        json_out(['order' => api_order((int) $mm[1])]);
    }

    if (preg_match('#^/files/(\d+)$#', $path, $mm) && $m === 'GET') {
        $f = row('SELECT * FROM files WHERE id = ?', [(int) $mm[1]]) ?? json_out(['error' => 'not found'], 404);
        send_file($f, true, 'bridge', 3);
    }

    if ($path === '/upload/init' && $m === 'POST') {
        $o = row('SELECT id FROM orders WHERE id = ?', [(int) ($body['order_id'] ?? 0)]) ?? json_out(['error' => 'order not found'], 404);
        $r = upload_init((int) $o['id'], 'output', 'bridge', (string) ($body['name'] ?? ''), (int) ($body['size'] ?? 0));
        json_out($r, isset($r['error']) ? 400 : 200);
    }
    if (in_array($path, ['/upload/chunk', '/upload/finish', '/upload/status'], true) && $m === 'POST') {
        $up = row('SELECT * FROM uploads WHERE token = ?', [(string) ($_GET['token'] ?? '')]) ?? json_out(['error' => 'upload not found'], 404);
        $r = match ($path) {
            '/upload/chunk' => upload_chunk($up, (int) ($_GET['offset'] ?? -1)),
            '/upload/finish' => upload_finish($up),
            default => ['received' => (int) $up['received'], 'size' => (int) $up['size']],
        };
        json_out($r, isset($r['error']) ? 409 : 200);
    }

    if (preg_match('#^/orders/(\d+)/(deliver|message)$#', $path, $mm) && $m === 'POST') {
        $id = (int) $mm[1];
        row('SELECT id FROM orders WHERE id = ?', [$id]) ?? json_out(['error' => 'order not found'], 404);
        $text = mb_substr(trim((string) ($body['note'] ?? $body['body'] ?? '')), 0, 10000);
        // Owner rule 2026-10-30: nothing a client reads may name the tools or process (app/guard.php).
        if ($hits = guard_find($text)) {
            json_out(['error' => 'blocked_terms', 'terms' => $hits,
                'hint' => 'Clients only see "Edited by MrCopper804". Rewrite the text without tool/process words.'], 422);
        }
        if ($mm[2] === 'deliver') {
            $f = row("SELECT * FROM files WHERE id = ? AND order_id = ? AND kind = 'output'", [(int) ($body['file_id'] ?? 0), $id])
                ?? json_out(['error' => 'output file not found on this order'], 400);
            $vid = add_version($id, (int) $f['id'], $text);
            q('UPDATE events SET done_at = ? WHERE order_id = ? AND done_at IS NULL', [now(), $id]);
            json_out(['ok' => true, 'version_id' => $vid]);
        }
        if ($text === '') {
            json_out(['error' => 'empty message'], 400);
        }
        json_out(['ok' => true, 'message_id' => add_message($id, 'studio', $text)]);
    }

    if (preg_match('#^/clients/(\d+)/session$#', $path, $mm) && $m === 'POST') {
        $s = (string) ($body['session'] ?? '');
        if (!preg_match('/^[A-Za-z0-9_-]{1,120}$/', $s)) {
            json_out(['error' => 'bad session id'], 400);
        }
        update('users', ['claude_session' => $s], "id = ? AND role = 'client'", [(int) $mm[1]]);
        json_out(['ok' => true]);
    }

    json_out(['error' => 'unknown endpoint'], 404);
}

function api_order(int $id): ?array
{
    $o = row('SELECT * FROM orders WHERE id = ?', [$id]);
    if (!$o) {
        return null;
    }
    $c = row('SELECT id, name, email, phone, currency, claude_session, admin_note FROM users WHERE id = ?', [$o['user_id']]);
    $answers = order_answers($o);
    $labels = [];
    foreach (questions() as $k => $qq) {
        if (($answers[$k] ?? '') !== '') {
            $labels[$qq['label']] = $answers[$k];
        }
    }
    return [
        'id' => (int) $o['id'], 'title' => $o['title'], 'status' => $o['status'],
        'length_sec' => (int) $o['length_sec'], 'currency' => $o['currency'], 'rate' => (float) $o['rate'],
        'estimate' => (float) $o['estimate'], 'final_price' => $o['final_price'] === null ? null : (float) $o['final_price'],
        'submitted_at' => $o['submitted_at'], 'answers' => $labels, 'script' => $o['script'], 'ideas' => $o['ideas'],
        'client' => $c,
        'files' => array_map(fn($f) => ['id' => (int) $f['id'], 'kind' => $f['kind'], 'name' => $f['orig_name'], 'mime' => $f['mime'],
            'size' => (int) $f['size'], 'sha256' => $f['sha256'], 'created_at' => $f['created_at']],
            rows('SELECT * FROM files WHERE order_id = ? ORDER BY id', [$id])),
        'versions' => rows('SELECT id, number, file_id, note, created_at FROM versions WHERE order_id = ? ORDER BY number', [$id]),
        'messages' => rows('SELECT id, sender, kind, body, version_id, created_at FROM messages WHERE order_id = ? ORDER BY id', [$id]),
    ];
}
