<?php
// Session, CSRF, rate limits and security headers.
declare(strict_types=1);

function is_https(): bool
{
    return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https'
        || (int) ($_SERVER['SERVER_PORT'] ?? 0) === 443;
}

function start_session(): void
{
    if (session_status() === PHP_SESSION_ACTIVE) {
        return;
    }
    session_name('portal_sid');
    session_set_cookie_params([
        'lifetime' => 0,
        'path' => '/',
        'secure' => is_https(),
        'httponly' => true,
        'samesite' => 'Lax',
    ]);
    ini_set('session.use_strict_mode', '1');
    ini_set('session.gc_maxlifetime', '86400');
    session_start();
    // Drop sessions idle for more than 7 days.
    $last = $_SESSION['seen'] ?? time();
    if (time() - $last > 7 * 86400) {
        $_SESSION = [];
        session_regenerate_id(true);
    }
    $_SESSION['seen'] = time();
}

function security_headers(): void
{
    header('X-Content-Type-Options: nosniff');
    header('X-Frame-Options: DENY');
    header('Referrer-Policy: same-origin');
    header('Permissions-Policy: camera=(), microphone=(), geolocation=()');
    header("Content-Security-Policy: default-src 'self'; img-src 'self' data: blob:; media-src 'self' blob:; " .
        "style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'");
    if (is_https()) {
        header('Strict-Transport-Security: max-age=31536000');
    }
}

function csrf_token(): string
{
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf'];
}

function csrf_field(): string
{
    return '<input type="hidden" name="_csrf" value="' . e(csrf_token()) . '">';
}

function csrf_check(): void
{
    $sent = $_POST['_csrf'] ?? ($_SERVER['HTTP_X_CSRF_TOKEN'] ?? '');
    if (!is_string($sent) || empty($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], $sent)) {
        abort(403, 'Your session expired. Go back, reload the page and try again.');
    }
}

function client_ip(): string
{
    return (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
}

/** Fixed-window counter. Returns false when the limit is passed. */
function rate_limit(string $key, int $max, int $windowSec): bool
{
    $now = time();
    $win = $now - ($now % $windowSec);
    $k = substr($key, 0, 190);
    $r = row('SELECT window_start, hits FROM rate_limits WHERE rkey = ?', [$k]);
    if (!$r) {
        try {
            insert('rate_limits', ['rkey' => $k, 'window_start' => $win, 'hits' => 1]);
        } catch (PDOException) {
            q('UPDATE rate_limits SET hits = hits + 1 WHERE rkey = ?', [$k]);
        }
        return true;
    }
    if ((int) $r['window_start'] !== $win) {
        update('rate_limits', ['window_start' => $win, 'hits' => 1], 'rkey = ?', [$k]);
        return true;
    }
    q('UPDATE rate_limits SET hits = hits + 1 WHERE rkey = ?', [$k]);
    return (int) $r['hits'] + 1 <= $max;
}

function rate_limit_or_abort(string $key, int $max, int $windowSec, bool $json = false): void
{
    if (!rate_limit($key, $max, $windowSec)) {
        header('Retry-After: ' . $windowSec);
        if ($json) {
            json_out(['error' => 'Too many requests, wait a moment.'], 429);
        }
        abort(429, 'Too many tries. Wait a few minutes and try again.');
    }
}
