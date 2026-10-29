<?php
// Accounts: register, login, logout, roles.
declare(strict_types=1);

function current_user(): ?array
{
    static $cache = false;
    if ($cache !== false) {
        return $cache;
    }
    $id = $_SESSION['uid'] ?? null;
    $cache = $id ? row("SELECT * FROM users WHERE id = ? AND status = 'active'", [$id]) : null;
    return $cache;
}

function require_login(): array
{
    $u = current_user();
    if (!$u) {
        redirect('login');
    }
    return $u;
}

function require_admin(): array
{
    $u = require_login();
    if ($u['role'] !== 'admin') {
        abort(403);
    }
    return $u;
}

function hash_password(string $pw): string
{
    return password_hash($pw, defined('PASSWORD_ARGON2ID') ? PASSWORD_ARGON2ID : PASSWORD_BCRYPT);
}

function validate_password(string $pw): ?string
{
    if (strlen($pw) < 8) {
        return 'Password must be at least 8 characters.';
    }
    if (strlen($pw) > 200) {
        return 'Password is too long.';
    }
    return null;
}

function register_user(string $name, string $email, string $phone, string $pw, string $currency): array
{
    $errors = [];
    if ($name === '' || mb_strlen($name) > 120) {
        $errors[] = 'Enter your name.';
    }
    if (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 190) {
        $errors[] = 'Enter a valid email.';
    }
    if (mb_strlen($phone) > 40) {
        $errors[] = 'Phone number is too long.';
    }
    if ($e = validate_password($pw)) {
        $errors[] = $e;
    }
    if (!in_array($currency, ['PKR', 'USD'], true)) {
        $currency = 'PKR';
    }
    if (!$errors && row('SELECT id FROM users WHERE email = ?', [strtolower($email)])) {
        $errors[] = 'An account with this email already exists. Log in instead.';
    }
    if ($errors) {
        return ['errors' => $errors];
    }
    $id = insert('users', [
        'email' => strtolower($email),
        'name' => $name,
        'phone' => $phone ?: null,
        'password_hash' => hash_password($pw),
        'role' => 'client',
        'status' => 'active',
        'currency' => $currency,
        'created_at' => now(),
    ]);
    return ['id' => $id];
}

function attempt_login(string $email, string $pw): bool
{
    $u = row('SELECT * FROM users WHERE email = ?', [strtolower(trim($email))]);
    // Verify against a dummy hash when the user is missing, so timing does not reveal accounts.
    $hash = $u['password_hash'] ?? '$2y$10$usesomesillystringfore7hnbRJHxXVLeakoG8K30oukPsA.ztMG';
    $ok = password_verify($pw, $hash);
    if (!$u || !$ok || $u['status'] !== 'active') {
        return false;
    }
    if (password_needs_rehash($u['password_hash'], defined('PASSWORD_ARGON2ID') ? PASSWORD_ARGON2ID : PASSWORD_BCRYPT)) {
        update('users', ['password_hash' => hash_password($pw)], 'id = ?', [$u['id']]);
    }
    session_regenerate_id(true);
    $_SESSION['uid'] = (int) $u['id'];
    unset($_SESSION['csrf']);
    update('users', ['last_login_at' => now()], 'id = ?', [$u['id']]);
    return true;
}

function logout(): void
{
    $_SESSION = [];
    session_regenerate_id(true);
}
