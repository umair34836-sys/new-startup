<?php
// Test helper: creates a fresh SQLite portal with an admin account and a bridge token.
// Usage: PORTAL_CONFIG=/path/config.php php tests/seed.php <admin_email> <admin_password> <bridge_token>
declare(strict_types=1);
require __DIR__ . '/../app/bootstrap.php';
migrate();
[$_, $email, $pw, $token] = $argv;
if (!row('SELECT id FROM users WHERE email = ?', [$email])) {
    insert('users', ['email' => $email, 'name' => 'Owner', 'password_hash' => hash_password($pw), 'role' => 'admin',
        'status' => 'active', 'currency' => 'PKR', 'created_at' => now()]);
}
set_setting('bridge_token_hash', hash('sha256', $token));
set_setting('brand_name', 'MrCopper804');
echo "seeded\n";
