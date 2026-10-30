<?php
// Plain-text email through PHP mail() (cPanel sends it with the account's mail server).
// Tests set config 'mail_log' to write emails to a file instead.
declare(strict_types=1);

/** Absolute links (emails, signed app links) use the fixed site address from config.php, never the request's
 *  Host header (a forged Host would otherwise put an attacker's domain into password-reset emails). */
function site_url(string $path = ''): string
{
    $base = rtrim((string) config('site_url', ''), '/');
    if ($base === '') {
        $base = 'https://' . preg_replace('/[^a-z0-9.:-]/i', '', (string) ($_SERVER['SERVER_NAME'] ?? 'localhost'));
    }
    return $base . base_url($path);
}

function send_mail(string $to, string $subject, string $body): bool
{
    $to = trim(str_replace(["\r", "\n"], '', $to));
    $subject = trim(str_replace(["\r", "\n"], ' ', $subject));
    if (!filter_var($to, FILTER_VALIDATE_EMAIL)) {
        return false;
    }
    if ($log = config('mail_log')) {
        return (bool) file_put_contents($log, json_encode(['to' => $to, 'subject' => $subject, 'body' => $body]) . "\n", FILE_APPEND | LOCK_EX);
    }
    $from = trim(str_replace(["\r", "\n"], '', setting('mail_from')));
    if (!filter_var($from, FILTER_VALIDATE_EMAIL)) {
        return false;
    }
    $brand = preg_replace('/[^\p{L}\p{N} ._-]/u', '', setting('brand_name'));
    $headers = "From: $brand <$from>\r\nReply-To: $from\r\nContent-Type: text/plain; charset=UTF-8\r\nX-Mailer: portal";
    return @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $from);
}

/** Emails the owner about new work, and the client about a new version. Never blocks the request on failure. */
function notify_event(int $orderId, string $type): void
{
    $o = row('SELECT o.*, u.name, u.email FROM orders o JOIN users u ON u.id = o.user_id WHERE o.id = ?', [$orderId]);
    if (!$o) {
        return;
    }
    $owner = setting('owner_email');
    $what = ['order_submitted' => 'New order', 'revision_requested' => 'Changes requested', 'approved' => 'Order approved',
        'client_message' => 'New client message'][$type] ?? $type;
    if ($owner !== '') {
        send_mail($owner, "$what: #{$o['id']} {$o['title']}", "$what from {$o['name']} ({$o['email']}).\n" . site_url('admin/orders/' . $o['id']));
    }
}

function notify_delivery(int $orderId, int $number): void
{
    $o = row('SELECT o.*, u.name, u.email FROM orders o JOIN users u ON u.id = o.user_id WHERE o.id = ?', [$orderId]);
    if ($o) {
        send_mail($o['email'], "Your video is ready: {$o['title']} (version $number)",
            "Hi {$o['name']},\n\nVersion $number of \"{$o['title']}\" is ready. Watch it and tell us if you want any changes:\n" .
            site_url('orders/' . $o['id']) . "\n\n" . setting('brand_name'));
    }
}
