<?php
// PDO connection (MySQL on the hosting, SQLite for local tests) and the schema.
declare(strict_types=1);

function db(): PDO
{
    static $pdo = null;
    if ($pdo) {
        return $pdo;
    }
    $driver = config('db_driver', 'mysql');
    $opts = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ];
    if ($driver === 'sqlite') {
        $pdo = new PDO('sqlite:' . config('db_path'), null, null, $opts);
        $pdo->exec('PRAGMA foreign_keys = ON');
        $pdo->exec('PRAGMA journal_mode = WAL');
    } else {
        $dsn = sprintf('mysql:host=%s;port=%d;dbname=%s;charset=utf8mb4',
            config('db_host', 'localhost'), (int) config('db_port', 3306), config('db_name'));
        $pdo = new PDO($dsn, config('db_user'), config('db_pass'), $opts);
    }
    return $pdo;
}

function q(string $sql, array $params = []): PDOStatement
{
    $st = db()->prepare($sql);
    $st->execute($params);
    return $st;
}

function row(string $sql, array $params = []): ?array
{
    $r = q($sql, $params)->fetch();
    return $r === false ? null : $r;
}

function rows(string $sql, array $params = []): array
{
    return q($sql, $params)->fetchAll();
}

function insert(string $table, array $data): int
{
    $cols = array_keys($data);
    $sql = 'INSERT INTO ' . $table . ' (' . implode(',', $cols) . ') VALUES (' .
        implode(',', array_fill(0, count($cols), '?')) . ')';
    q($sql, array_values($data));
    return (int) db()->lastInsertId();
}

function update(string $table, array $data, string $where, array $params): void
{
    $set = implode(',', array_map(fn($c) => "$c = ?", array_keys($data)));
    q("UPDATE $table SET $set WHERE $where", [...array_values($data), ...$params]);
}

function schema_sql(string $driver): array
{
    $pk = $driver === 'sqlite' ? 'INTEGER PRIMARY KEY AUTOINCREMENT' : 'BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY';
    $fk = $driver === 'sqlite' ? 'INTEGER' : 'BIGINT UNSIGNED';
    $end = $driver === 'sqlite' ? '' : ' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci';
    return [
        "CREATE TABLE IF NOT EXISTS users (
            id $pk,
            email VARCHAR(190) NOT NULL UNIQUE,
            name VARCHAR(120) NOT NULL,
            phone VARCHAR(40) NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(10) NOT NULL DEFAULT 'client',
            status VARCHAR(10) NOT NULL DEFAULT 'active',
            currency VARCHAR(3) NOT NULL DEFAULT 'PKR',
            rate_pkr DECIMAL(12,4) NULL,
            rate_usd DECIMAL(12,4) NULL,
            claude_session VARCHAR(120) NULL,
            session_version INT NOT NULL DEFAULT 0,
            admin_note TEXT NULL,
            created_at DATETIME NOT NULL,
            last_login_at DATETIME NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS settings (
            name VARCHAR(64) NOT NULL PRIMARY KEY,
            value TEXT NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS orders (
            id $pk,
            user_id $fk NOT NULL,
            title VARCHAR(160) NOT NULL,
            status VARCHAR(24) NOT NULL DEFAULT 'draft',
            answers TEXT NULL,
            script TEXT NULL,
            ideas TEXT NULL,
            length_sec INT NOT NULL DEFAULT 0,
            currency VARCHAR(3) NOT NULL DEFAULT 'PKR',
            rate DECIMAL(12,4) NOT NULL DEFAULT 0,
            estimate DECIMAL(14,2) NOT NULL DEFAULT 0,
            final_price DECIMAL(14,2) NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            submitted_at DATETIME NULL,
            approved_at DATETIME NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )$end",
        "CREATE TABLE IF NOT EXISTS files (
            id $pk,
            order_id $fk NOT NULL,
            kind VARCHAR(10) NOT NULL,
            orig_name VARCHAR(255) NOT NULL,
            stored_name VARCHAR(64) NOT NULL,
            mime VARCHAR(120) NOT NULL,
            size BIGINT NOT NULL,
            sha256 CHAR(64) NULL,
            uploaded_by VARCHAR(10) NOT NULL,
            created_at DATETIME NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )$end",
        "CREATE TABLE IF NOT EXISTS uploads (
            id $pk,
            token CHAR(40) NOT NULL UNIQUE,
            order_id $fk NOT NULL,
            kind VARCHAR(10) NOT NULL,
            uploaded_by VARCHAR(10) NOT NULL,
            orig_name VARCHAR(255) NOT NULL,
            size BIGINT NOT NULL,
            received BIGINT NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS versions (
            id $pk,
            order_id $fk NOT NULL,
            number INT NOT NULL,
            file_id $fk NOT NULL,
            note TEXT NULL,
            created_at DATETIME NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (file_id) REFERENCES files(id)
        )$end",
        "CREATE TABLE IF NOT EXISTS messages (
            id $pk,
            order_id $fk NOT NULL,
            sender VARCHAR(10) NOT NULL,
            kind VARCHAR(16) NOT NULL DEFAULT 'note',
            body TEXT NOT NULL,
            version_id $fk NULL,
            created_at DATETIME NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )$end",
        "CREATE TABLE IF NOT EXISTS events (
            id $pk,
            order_id $fk NOT NULL,
            type VARCHAR(32) NOT NULL,
            created_at DATETIME NOT NULL,
            taken_at DATETIME NULL,
            done_at DATETIME NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )$end",
        "CREATE TABLE IF NOT EXISTS app_tokens (
            id $pk,
            user_id $fk NOT NULL,
            token_hash CHAR(64) NOT NULL UNIQUE,
            device VARCHAR(80) NULL,
            created_at DATETIME NOT NULL,
            last_used_at DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )$end",
        "CREATE TABLE IF NOT EXISTS password_resets (
            id $pk,
            user_id $fk NOT NULL,
            token_hash CHAR(64) NOT NULL UNIQUE,
            expires_at DATETIME NOT NULL,
            used_at DATETIME NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )$end",
        "CREATE TABLE IF NOT EXISTS rate_limits (
            rkey VARCHAR(190) NOT NULL PRIMARY KEY,
            window_start INT NOT NULL,
            hits INT NOT NULL
        )$end",
        "CREATE INDEX idx_orders_user ON orders(user_id)",
        "CREATE INDEX idx_files_order ON files(order_id)",
        "CREATE INDEX idx_events_done ON events(done_at)",
        "CREATE INDEX idx_messages_order ON messages(order_id)",
    ];
}

function migrate(): void
{
    $driver = config('db_driver', 'mysql');
    foreach (schema_sql($driver) as $sql) {
        try {
            db()->exec($sql);
        } catch (PDOException $ex) {
            // Indexes already exist on a second run (MySQL has no CREATE INDEX IF NOT EXISTS).
            if (!str_starts_with($sql, 'CREATE INDEX')) {
                throw $ex;
            }
        }
    }
}
