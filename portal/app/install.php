<?php
// One-time installer. Runs only while config.php does not exist.
// To prove the visitor is the hosting owner, it asks for a key it writes into storage/install-key.txt
// (readable only through cPanel File Manager).
declare(strict_types=1);

security_headers();
start_session();

$keyFile = APP_ROOT . '/storage/install-key.txt';
if (!is_file($keyFile)) {
    @file_put_contents($keyFile, bin2hex(random_bytes(8)) . "\n");
    @chmod($keyFile, 0600);
}
$installKey = trim((string) @file_get_contents($keyFile));
if (strlen($installKey) < 16) {
    http_response_code(500);
    exit('Could not create storage/install-key.txt. Make the storage folder writable and reload.');
}

$checks = [
    'PHP 8.1 or newer' => version_compare(PHP_VERSION, '8.1', '>='),
    'PDO MySQL extension' => extension_loaded('pdo_mysql'),
    'fileinfo extension (file type checks)' => extension_loaded('fileinfo'),
    'mbstring extension' => extension_loaded('mbstring'),
    'storage/ folder is writable' => is_writable(APP_ROOT . '/storage'),
    'portal folder is writable (to create config.php)' => is_writable(APP_ROOT),
];
$errors = [];
$done = false;

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    csrf_check();
    $f = fn($k) => trim((string) ($_POST[$k] ?? ''));
    if (!hash_equals($installKey, $f('install_key'))) {
        $errors[] = 'Install key is wrong. Open storage/install-key.txt in cPanel File Manager and copy it.';
    }
    if (!filter_var($f('admin_email'), FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'Admin email is not valid.';
    }
    if ($e = validate_password((string) ($_POST['admin_password'] ?? ''))) {
        $errors[] = $e;
    }
    if (in_array(false, $checks, true)) {
        $errors[] = 'Fix the red checks first.';
    }
    if (!$errors) {
        $cfg = [
            'db_driver' => 'mysql',
            'db_host' => $f('db_host') ?: 'localhost',
            'db_port' => 3306,
            'db_name' => $f('db_name'),
            'db_user' => $f('db_user'),
            'db_pass' => (string) ($_POST['db_pass'] ?? ''),
            'base_path' => '',
            'timezone' => 'Asia/Karachi',
        ];
        $GLOBALS['config'] = $cfg;
        try {
            db();
            migrate();
            if (!row("SELECT id FROM users WHERE role = 'admin'")) {
                insert('users', [
                    'email' => strtolower($f('admin_email')), 'name' => $f('admin_name') ?: 'Admin',
                    'password_hash' => hash_password((string) $_POST['admin_password']), 'role' => 'admin',
                    'status' => 'active', 'currency' => 'PKR', 'created_at' => now(),
                ]);
            }
            if ($f('brand_name') !== '') {
                set_setting('brand_name', mb_substr($f('brand_name'), 0, 80));
            }
            $php = "<?php\n// Written by the installer. Keep this file private; never put it in git.\nreturn " . var_export($cfg, true) . ";\n";
            if (file_put_contents(APP_ROOT . '/config.php', $php) === false) {
                throw new RuntimeException('Could not write config.php');
            }
            @chmod(APP_ROOT . '/config.php', 0600);
            @unlink($keyFile);
            $done = true;
        } catch (Throwable $ex) {
            $GLOBALS['config'] = null;
            $errors[] = 'Database error: ' . $ex->getMessage();
        }
    }
}
?><!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Install portal</title><link rel="stylesheet" href="assets/app.css"></head>
<body class="auth"><main class="card narrow">
<h1>Install the portal</h1>
<?php if ($done): ?>
  <p class="notice ok">Done. The portal is installed.</p>
  <p><a class="btn primary" href="login">Go to login</a></p>
<?php else: ?>
  <ul class="checks"><?php foreach ($checks as $label => $ok): ?>
    <li class="<?= $ok ? 'ok' : 'bad' ?>"><?= $ok ? '✓' : '✗' ?> <?= e($label) ?></li><?php endforeach; ?>
  </ul>
  <?php foreach ($errors as $er): ?><p class="notice err"><?= e($er) ?></p><?php endforeach; ?>
  <form method="post" class="form">
    <?= csrf_field() ?>
    <label>Install key <small>(file storage/install-key.txt)</small><input name="install_key" required autocomplete="off"></label>
    <fieldset><legend>MySQL database (cPanel → MySQL Databases)</legend>
      <label>Host<input name="db_host" value="localhost"></label>
      <label>Database name<input name="db_name" required></label>
      <label>Database user<input name="db_user" required></label>
      <label>Database password<input name="db_pass" type="password"></label>
    </fieldset>
    <fieldset><legend>Your admin account</legend>
      <label>Name<input name="admin_name" value="Admin"></label>
      <label>Email<input name="admin_email" type="email" required></label>
      <label>Password (8+ characters)<input name="admin_password" type="password" required minlength="8"></label>
      <label>Brand name shown to clients<input name="brand_name" placeholder="Your studio name"></label>
    </fieldset>
    <button class="btn primary">Install</button>
  </form>
<?php endif; ?>
</main></body></html>
