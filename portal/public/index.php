<?php
// Front controller: every request that is not a static file lands here.
declare(strict_types=1);

$appDir = is_dir(__DIR__ . '/../app') ? __DIR__ . '/../app' : __DIR__ . '/../portal/app';

// PHP's built-in server (tests): let it serve real static files itself.
if (PHP_SAPI === 'cli-server') {
    $p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    if ($p !== '/' && is_file(__DIR__ . $p) && !str_ends_with($p, '.php')) {
        return false;
    }
}

require $appDir . '/bootstrap.php';

if (!$GLOBALS['config']) {
    require APP_DIR . '/install.php';
    exit;
}

$path = '/' . trim((string) parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH), '/');
$base = rtrim((string) config('base_path', ''), '/');
if ($base !== '' && str_starts_with($path, $base)) {
    $path = '/' . trim(substr($path, strlen($base)), '/');
}
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

if (str_starts_with($path, '/api/bridge')) {
    require APP_DIR . '/routes_api.php';
    route_api($method, substr($path, strlen('/api/bridge')) ?: '/');
    exit;
}

security_headers();
start_session();
if ($method === 'POST') {
    csrf_check();
}

require APP_DIR . '/routes_web.php';
require APP_DIR . '/routes_admin.php';

if (str_starts_with($path, '/admin')) {
    route_admin($method, $path);
} else {
    route_web($method, $path);
}
abort(404);
