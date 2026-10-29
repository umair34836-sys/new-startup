<?php
// Owner's admin panel: orders, clients and their rates, settings, bridge token.
declare(strict_types=1);

function route_admin(string $m, string $path): void
{
    $admin = require_admin();

    if ($path === '/admin') {
        $status = (string) ($_GET['status'] ?? '');
        $where = isset(ORDER_STATUSES[$status]) ? 'WHERE o.status = ?' : "WHERE o.status <> 'draft'";
        $params = isset(ORDER_STATUSES[$status]) ? [$status] : [];
        $orders = rows("SELECT o.*, u.name AS client_name, u.email AS client_email FROM orders o JOIN users u ON u.id = o.user_id $where ORDER BY o.updated_at DESC LIMIT 300", $params);
        $counts = [];
        foreach (rows('SELECT status, COUNT(*) AS c FROM orders GROUP BY status') as $r) {
            $counts[$r['status']] = (int) $r['c'];
        }
        $pending = (int) row('SELECT COUNT(*) AS c FROM events WHERE done_at IS NULL')['c'];
        view('admin/orders', compact('admin', 'orders', 'counts', 'status', 'pending'));
        exit;
    }

    if (preg_match('#^/admin/orders/(\d+)$#', $path, $mm)) {
        $order = row('SELECT o.*, u.name AS client_name, u.email AS client_email, u.phone AS client_phone, u.claude_session FROM orders o JOIN users u ON u.id = o.user_id WHERE o.id = ?', [(int) $mm[1]]);
        if (!$order) {
            abort(404);
        }
        $files = rows('SELECT * FROM files WHERE order_id = ? ORDER BY id', [$order['id']]);
        $events = rows('SELECT * FROM events WHERE order_id = ? ORDER BY id DESC', [$order['id']]);
        view('admin/order', ['admin' => $admin, 'order' => $order, 'files' => $files, 'events' => $events] + order_thread($order));
        exit;
    }

    if (preg_match('#^/admin/orders/(\d+)/(status|message|price|deliver)$#', $path, $mm) && $m === 'POST') {
        $order = row('SELECT * FROM orders WHERE id = ?', [(int) $mm[1]]) ?? abort(404);
        $id = (int) $order['id'];
        switch ($mm[2]) {
            case 'status':
                $s = post('status');
                if (isset(ORDER_STATUSES[$s])) {
                    update('orders', ['status' => $s, 'updated_at' => now()], 'id = ?', [$id]);
                }
                break;
            case 'message':
                if (post('body') !== '') {
                    add_message($id, 'studio', post('body'));
                }
                break;
            case 'price':
                $p = post('final_price');
                update('orders', ['final_price' => $p === '' ? null : max(0, (float) $p), 'updated_at' => now()], 'id = ?', [$id]);
                break;
            case 'deliver':
                $f = row("SELECT * FROM files WHERE id = ? AND order_id = ? AND kind = 'output'", [(int) post('file_id'), $id]);
                if (!$f) {
                    flash('Upload the finished video first.', 'err');
                    redirect("admin/orders/$id");
                }
                add_version($id, (int) $f['id'], post('note'));
                q('UPDATE events SET done_at = ? WHERE order_id = ? AND done_at IS NULL', [now(), $id]);
                break;
        }
        flash('Saved.');
        redirect("admin/orders/$id");
    }

    if ($path === '/admin/clients') {
        $clients = rows("SELECT u.*, (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id AND o.status <> 'draft') AS order_count FROM users u WHERE u.role = 'client' ORDER BY u.created_at DESC");
        view('admin/clients', compact('admin', 'clients'));
        exit;
    }

    if (preg_match('#^/admin/clients/(\d+)$#', $path, $mm) && $m === 'POST') {
        $c = row("SELECT * FROM users WHERE id = ? AND role = 'client'", [(int) $mm[1]]) ?? abort(404);
        $num = fn(string $k) => post($k) === '' ? null : max(0, (float) post($k));
        update('users', [
            'rate_pkr' => $num('rate_pkr'),
            'rate_usd' => $num('rate_usd'),
            'currency' => in_array(post('currency'), ['PKR', 'USD'], true) ? post('currency') : $c['currency'],
            'status' => post('status') === 'blocked' ? 'blocked' : 'active',
            'claude_session' => preg_match('/^[A-Za-z0-9_-]{0,120}$/', post('claude_session')) ? (post('claude_session') ?: null) : $c['claude_session'],
            'admin_note' => mb_substr(post('admin_note'), 0, 2000),
        ], 'id = ?', [$c['id']]);
        flash('Client saved.');
        redirect('admin/clients');
    }

    if ($path === '/admin/settings') {
        $newToken = null;
        if ($m === 'POST') {
            if (post('action') === 'token') {
                $newToken = 'pb_' . bin2hex(random_bytes(24));
                set_setting('bridge_token_hash', hash('sha256', $newToken));
            } else {
                foreach (['brand_name' => 80, 'brand_tagline' => 160, 'support_contact' => 200] as $k => $max) {
                    set_setting($k, mb_substr(post($k), 0, $max));
                }
                foreach (['rate_pkr', 'rate_usd'] as $k) {
                    set_setting($k, (string) max(0, (float) post($k)));
                }
                set_setting('max_file_mb', (string) min(20480, max(10, (int) post('max_file_mb'))));
                set_setting('max_files_per_order', (string) min(500, max(1, (int) post('max_files_per_order'))));
                flash('Settings saved.');
                redirect('admin/settings');
            }
        }
        $events = rows('SELECT e.*, o.title FROM events e JOIN orders o ON o.id = e.order_id ORDER BY e.id DESC LIMIT 30');
        view('admin/settings', ['admin' => $admin, 'newToken' => $newToken, 'events' => $events,
            'chunk' => chunk_bytes(), 'ini' => ['upload_max_filesize' => ini_get('upload_max_filesize'),
            'post_max_size' => ini_get('post_max_size'), 'memory_limit' => ini_get('memory_limit'),
            'max_execution_time' => ini_get('max_execution_time')]]);
        exit;
    }
}
