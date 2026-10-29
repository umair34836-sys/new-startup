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
    // A password change or reset logs out every other device.
    if ($cache && (int) $cache['session_version'] !== (int) ($_SESSION['sv'] ?? -1)) {
        $_SESSION = [];
        $cache = null;
    }
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
        // Only paid clients use the portal (owner, 2026-10-29): new accounts wait for the owner's approval.
        'status' => setting('signup_approval') === '1' ? 'pending' : 'active',
        'currency' => $currency,
        'created_at' => now(),
    ]);
    return ['id' => $id];
}

/** Returns 'ok', 'bad' (wrong email or password) or 'pending' (right password, not approved yet). */
function attempt_login(string $email, string $pw): string
{
    $u = row('SELECT * FROM users WHERE email = ?', [strtolower(trim($email))]);
    // Verify against a dummy hash of the same algorithm when the user is missing, so timing does not reveal accounts.
    $hash = $u['password_hash'] ?? dummy_hash();
    $ok = password_verify($pw, $hash);
    if (!$u || !$ok || $u['status'] === 'blocked') {
        return 'bad';
    }
    if ($u['status'] !== 'active') {
        return 'pending';
    }
    if (password_needs_rehash($u['password_hash'], defined('PASSWORD_ARGON2ID') ? PASSWORD_ARGON2ID : PASSWORD_BCRYPT)) {
        update('users', ['password_hash' => hash_password($pw)], 'id = ?', [$u['id']]);
    }
    session_regenerate_id(true);
    $_SESSION['uid'] = (int) $u['id'];
    $_SESSION['sv'] = (int) $u['session_version'];
    unset($_SESSION['csrf']);
    update('users', ['last_login_at' => now()], 'id = ?', [$u['id']]);
    return 'ok';
}

/** New password: bumps session_version so every other device is logged out; keeps this device logged in. */
function set_password(int $userId, string $pw, bool $keepThisSession): void
{
    q('UPDATE users SET password_hash = ?, session_version = session_version + 1 WHERE id = ?', [hash_password($pw), $userId]);
    if ($keepThisSession) {
        session_regenerate_id(true);
        $_SESSION['sv'] = (int) row('SELECT session_version FROM users WHERE id = ?', [$userId])['session_version'];
    }
}

/** Starts a reset: stores only the token's sha256, valid 1 hour, and emails the link. Silent if the email is unknown. */
function start_password_reset(string $email): void
{
    $u = row("SELECT * FROM users WHERE email = ? AND status = 'active'", [strtolower(trim($email))]);
    if (!$u) {
        return;
    }
    $token = bin2hex(random_bytes(32));
    insert('password_resets', ['user_id' => $u['id'], 'token_hash' => hash('sha256', $token),
        'expires_at' => gmdate('Y-m-d H:i:s', time() + 3600)]);
    $link = site_url('reset?token=' . $token);
    send_mail($u['email'], 'Reset your password', "Hi {$u['name']},\n\nOpen this link within 1 hour to set a new password:\n$link\n\nIf you did not ask for this, ignore this email.\n\n" . setting('brand_name'));
}

function find_reset(string $token): ?array
{
    if (!preg_match('/^[a-f0-9]{64}$/', $token)) {
        return null;
    }
    return row('SELECT * FROM password_resets WHERE token_hash = ? AND used_at IS NULL AND expires_at > ?', [hash('sha256', $token), now()]);
}

function dummy_hash(): string
{
    $h = setting('dummy_hash');
    if ($h === '') {
        $h = hash_password(bin2hex(random_bytes(16)));
        set_setting('dummy_hash', $h);
    }
    return $h;
}

function logout(): void
{
    $_SESSION = [];
    session_regenerate_id(true);
}
