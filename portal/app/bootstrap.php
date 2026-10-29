<?php
// Loads config, opens the database, starts the session and defines small helpers.
declare(strict_types=1);

ini_set('display_errors', '0');
ini_set('log_errors', '1');
set_exception_handler(function (Throwable $ex): void {
    error_log('portal: ' . $ex);
    if (!headers_sent()) {
        http_response_code(500);
        header('Content-Type: text/plain; charset=utf-8');
    }
    echo 'Something went wrong. Please try again in a minute.';
});

define('APP_ROOT', dirname(__DIR__));
define('APP_DIR', __DIR__);

$configFile = getenv('PORTAL_CONFIG') ?: APP_ROOT . '/config.php';
$GLOBALS['config'] = is_file($configFile) ? require $configFile : null;

require APP_DIR . '/db.php';
require APP_DIR . '/security.php';
require APP_DIR . '/auth.php';
require APP_DIR . '/settings.php';
require APP_DIR . '/orders.php';
require APP_DIR . '/files.php';

function config(string $key, $default = null)
{
    $c = $GLOBALS['config'] ?? [];
    return $c[$key] ?? $default;
}

function storage_dir(): string
{
    return rtrim((string) config('storage_dir', APP_ROOT . '/storage'), '/');
}

function now(): string
{
    return gmdate('Y-m-d H:i:s');
}

function e($v): string
{
    return htmlspecialchars((string) $v, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function base_url(string $path = ''): string
{
    $base = rtrim((string) config('base_path', ''), '/');
    return $base . '/' . ltrim($path, '/');
}

function redirect(string $path): never
{
    header('Location: ' . base_url($path), true, 303);
    exit;
}

function flash(?string $msg = null, string $type = 'ok'): ?array
{
    if ($msg !== null) {
        $_SESSION['flash'] = ['msg' => $msg, 'type' => $type];
        return null;
    }
    $f = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    return $f;
}

function view(string $name, array $vars = [], string $layout = 'layout'): void
{
    extract($vars, EXTR_SKIP);
    ob_start();
    require APP_DIR . '/views/' . $name . '.php';
    $content = ob_get_clean();
    require APP_DIR . '/views/' . $layout . '.php';
}

function json_out($data, int $code = 200): never
{
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

function abort(int $code, string $msg = ''): never
{
    http_response_code($code);
    $titles = [400 => 'Bad request', 403 => 'Not allowed', 404 => 'Not found', 413 => 'Too large', 429 => 'Too many requests'];
    view('error', ['code' => $code, 'title' => $titles[$code] ?? 'Error', 'msg' => $msg]);
    exit;
}

function post(string $key, string $default = ''): string
{
    $v = $_POST[$key] ?? $default;
    return is_string($v) ? trim($v) : $default;
}

function fmt_money(float $amount, string $currency): string
{
    $dec = $currency === 'PKR' ? 0 : 2;
    return $currency . ' ' . number_format($amount, $dec);
}

function fmt_bytes(int $b): string
{
    $u = ['B', 'KB', 'MB', 'GB', 'TB'];
    $i = 0;
    $f = (float) $b;
    while ($f >= 1024 && $i < 4) {
        $f /= 1024;
        $i++;
    }
    return round($f, $i ? 1 : 0) . ' ' . $u[$i];
}

function fmt_date(?string $utc): string
{
    if (!$utc) {
        return '';
    }
    $tz = new DateTimeZone((string) config('timezone', 'Asia/Karachi'));
    return (new DateTime($utc, new DateTimeZone('UTC')))->setTimezone($tz)->format('d M Y, H:i');
}
