<?php
// Client-facing pages: account, orders, uploads, review loop.
declare(strict_types=1);

function route_web(string $m, string $path): void
{
    $ip = client_ip();

    if ($path === '/') {
        $u = current_user();
        if ($u) {
            redirect($u['role'] === 'admin' ? 'admin' : 'orders');
        }
        view('auth/home');
        exit;
    }

    if ($path === '/manifest.webmanifest') {
        header('Content-Type: application/manifest+json');
        header('Cache-Control: public, max-age=86400');
        $brand = setting('brand_name');
        echo json_encode([
            'name' => $brand, 'short_name' => mb_substr($brand, 0, 12), 'start_url' => base_url('orders'),
            'scope' => base_url(''), 'display' => 'standalone', 'background_color' => '#120b2b', 'theme_color' => '#120b2b',
            'icons' => [
                ['src' => base_url('assets/icons/icon-192.png'), 'sizes' => '192x192', 'type' => 'image/png', 'purpose' => 'any'],
                ['src' => base_url('assets/icons/icon-512.png'), 'sizes' => '512x512', 'type' => 'image/png', 'purpose' => 'any'],
                ['src' => base_url('assets/icons/maskable-512.png'), 'sizes' => '512x512', 'type' => 'image/png', 'purpose' => 'maskable'],
            ],
        ], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
        exit;
    }

    if ($path === '/login') {
        $error = null;
        if ($m === 'POST') {
            rate_limit_or_abort("login:$ip", 10, 900);
            rate_limit_or_abort('loginmail:' . strtolower(post('email')), 10, 900);
            $r = attempt_login(post('email'), (string) ($_POST['password'] ?? ''));
            if ($r === 'ok') {
                redirect('/');
            }
            $error = $r === 'pending' ? 'Your account is waiting for approval. We will activate it soon.' : 'Wrong email or password.';
        }
        view('auth/login', ['error' => $error, 'email' => post('email')]);
        exit;
    }

    if ($path === '/register') {
        $errors = [];
        if ($m === 'POST') {
            rate_limit_or_abort("register:$ip", 5, 3600);
            $r = register_user(post('name'), post('email'), post('phone'), (string) ($_POST['password'] ?? ''), post('currency'));
            if (isset($r['id'])) {
                if (attempt_login(post('email'), (string) $_POST['password']) === 'ok') {
                    flash('Welcome! Start your first video order.');
                    redirect('orders');
                }
                flash('Account created. You can log in as soon as we approve it.');
                redirect('login');
            }
            $errors = $r['errors'];
        }
        view('auth/register', ['errors' => $errors, 'old' => $_POST]);
        exit;
    }

    if ($path === '/logout' && $m === 'POST') {
        logout();
        redirect('login');
    }

    $user = require_login();

    if ($path === '/account') {
        $msg = null;
        if ($m === 'POST') {
            rate_limit_or_abort("pw:{$user['id']}", 10, 900);
            if (!password_verify((string) ($_POST['current'] ?? ''), $user['password_hash'])) {
                $msg = ['err', 'Current password is wrong.'];
            } elseif ($e = validate_password((string) ($_POST['new'] ?? ''))) {
                $msg = ['err', $e];
            } else {
                update('users', ['password_hash' => hash_password((string) $_POST['new'])], 'id = ?', [$user['id']]);
                session_regenerate_id(true);
                $msg = ['ok', 'Password changed.'];
            }
        }
        view('client/account', ['user' => $user, 'msg' => $msg]);
        exit;
    }

    if ($path === '/orders') {
        $orders = rows('SELECT * FROM orders WHERE user_id = ? ORDER BY updated_at DESC', [$user['id']]);
        view('client/orders', ['user' => $user, 'orders' => $orders]);
        exit;
    }

    if ($path === '/orders/new' && $m === 'POST') {
        rate_limit_or_abort("neworder:{$user['id']}", 20, 3600);
        $id = create_draft($user);
        redirect("orders/$id");
    }

    if (preg_match('#^/orders/(\d+)$#', $path, $mm)) {
        $order = order_for_user((int) $mm[1], $user);
        $files = rows('SELECT * FROM files WHERE order_id = ? ORDER BY id', [$order['id']]);
        if ($order['status'] === 'draft') {
            view('client/order_form', ['user' => $user, 'order' => $order, 'files' => $files, 'errors' => []]);
        } else {
            view('client/order_view', ['user' => $user, 'order' => $order, 'files' => $files] + order_thread($order));
        }
        exit;
    }

    if (preg_match('#^/orders/(\d+)/save$#', $path, $mm) && $m === 'POST') {
        $order = order_for_user((int) $mm[1], $user);
        if ($order['status'] !== 'draft') {
            redirect("orders/{$order['id']}");
        }
        $submit = ($_POST['action'] ?? '') === 'submit';
        $errors = save_order_form($order, $user, $_POST, $submit);
        if (!$errors) {
            flash($submit ? 'Order sent! We will start working on it soon.' : 'Draft saved.');
            redirect("orders/{$order['id']}");
        }
        $order = order_for_user((int) $order['id'], $user);
        $files = rows('SELECT * FROM files WHERE order_id = ? ORDER BY id', [$order['id']]);
        view('client/order_form', ['user' => $user, 'order' => $order, 'files' => $files, 'errors' => $errors]);
        exit;
    }

    if (preg_match('#^/orders/(\d+)/(changes|approve|message)$#', $path, $mm) && $m === 'POST') {
        $order = order_for_user((int) $mm[1], $user);
        rate_limit_or_abort("msg:{$user['id']}", 30, 3600);
        $body = (string) ($_POST['body'] ?? '');
        $err = match ($mm[2]) {
            'changes' => request_changes($order, $body),
            'approve' => approve_order($order, $body),
            'message' => client_message($order, $body),
        };
        flash($err ?? match ($mm[2]) {
            'changes' => 'Thanks! Your changes were sent. You will get a new version here.',
            'approve' => 'Great, the order is approved. Thank you!',
            default => 'Message sent.',
        }, $err ? 'err' : 'ok');
        redirect("orders/{$order['id']}");
    }

    if (preg_match('#^/orders/(\d+)/files/(\d+)/delete$#', $path, $mm) && $m === 'POST') {
        $order = order_for_user((int) $mm[1], $user);
        $f = row("SELECT * FROM files WHERE id = ? AND order_id = ? AND kind = 'input'", [(int) $mm[2], $order['id']]);
        if ($f && $order['status'] === 'draft') {
            delete_file($f);
        }
        redirect("orders/{$order['id']}");
    }

    if (preg_match('#^/files/(\d+)(/download)?$#', $path, $mm)) {
        $f = row('SELECT * FROM files WHERE id = ?', [(int) $mm[1]]);
        if (!$f) {
            abort(404);
        }
        $o = order_for_user((int) $f['order_id'], $user);
        // Clients see their own inputs and only outputs that were delivered as a version.
        if ($user['role'] !== 'admin' && $f['kind'] === 'output' && !row('SELECT id FROM versions WHERE file_id = ?', [$f['id']])) {
            abort(404);
        }
        rate_limit_or_abort("dl:{$user['id']}", 600, 3600);
        send_file($f, !empty($mm[2]), 'u' . $user['id'], $user['role'] === 'admin' ? 4 : 2);
    }

    if (str_starts_with($path, '/upload/') && $m === 'POST') {
        upload_endpoint($path, $user);
    }
}

/** JSON endpoints used by assets/app.js for chunked uploads (clients upload inputs, admin uploads outputs). */
function upload_endpoint(string $path, array $user): never
{
    rate_limit_or_abort("up:{$user['id']}", 3000, 3600, true);
    $isAdmin = $user['role'] === 'admin';
    if ($path === '/upload/init') {
        $in = json_decode((string) file_get_contents('php://input'), true) ?: [];
        $order = order_for_user((int) ($in['order_id'] ?? 0), $user);
        $kind = $isAdmin && ($in['kind'] ?? '') === 'output' ? 'output' : 'input';
        if (!$isAdmin && $order['status'] === 'approved') {
            json_out(['error' => 'This order is closed.'], 400);
        }
        $r = upload_init((int) $order['id'], $kind, $isAdmin ? 'admin' : 'client', (string) ($in['name'] ?? ''), (int) ($in['size'] ?? 0));
        json_out($r, isset($r['error']) ? 400 : 200);
    }
    $token = (string) ($_GET['token'] ?? '');
    $up = row('SELECT * FROM uploads WHERE token = ?', [$token]);
    if (!$up) {
        json_out(['error' => 'Upload not found. Start again.'], 404);
    }
    order_for_user((int) $up['order_id'], $user);
    if ($path === '/upload/chunk') {
        $r = upload_chunk($up, (int) ($_GET['offset'] ?? -1));
        json_out($r, isset($r['error']) ? 409 : 200);
    }
    if ($path === '/upload/finish') {
        $r = upload_finish($up);
        json_out($r, isset($r['error']) ? 400 : 200);
    }
    json_out(['error' => 'Unknown'], 404);
}

function order_thread(array $order): array
{
    $versions = rows('SELECT v.*, f.orig_name, f.mime, f.size FROM versions v JOIN files f ON f.id = v.file_id WHERE v.order_id = ? ORDER BY v.number DESC', [$order['id']]);
    $messages = rows('SELECT * FROM messages WHERE order_id = ? ORDER BY id', [$order['id']]);
    return ['versions' => $versions, 'messages' => $messages];
}
