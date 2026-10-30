<?php
// Housekeeping. cPanel → Cron Jobs, once an hour:
//   php /home/<you>/portal/app/cron.php >/dev/null 2>&1
declare(strict_types=1);
if (PHP_SAPI !== 'cli') {
    http_response_code(404);
    exit;
}
require __DIR__ . '/bootstrap.php';
if (!$GLOBALS['config']) {
    exit("not installed\n");
}
$n = 0;
foreach (rows('SELECT token FROM uploads WHERE updated_at < ?', [gmdate('Y-m-d H:i:s', time() - 21600)]) as $u) {
    @unlink(chunk_path($u['token']));
    q('DELETE FROM uploads WHERE token = ?', [$u['token']]);
    $n++;
}
q('DELETE FROM rate_limits WHERE window_start < ?', [time() - 86400]);
q('DELETE FROM password_resets WHERE expires_at < ?', [gmdate('Y-m-d H:i:s', time() - 86400)]);
// Old session files (the portal keeps its own session folder).
foreach (glob(storage_dir() . '/sessions/sess_*') ?: [] as $f) {
    if (filemtime($f) < time() - 30 * 86400) {
        @unlink($f);
    }
}
echo "cleaned uploads: $n\n";
