<?php
// Key/value settings stored in the database (brand, rates, limits, bridge token hash).
declare(strict_types=1);

const SETTING_DEFAULTS = [
    'brand_name' => 'MrCopper804',
    'splash_subtitle' => 'Editor',
    'brand_tagline' => 'Send your footage. Get a finished video.',
    // Owner (2026-10-29): clients only ever learn that MrCopper804 edits every video himself, by hand.
    'promise_text' => 'Every video is edited by hand by MrCopper804.',
    'support_contact' => '',
    'rate_pkr' => '50',
    'rate_usd' => '0.20',
    'max_file_mb' => '4096',
    'max_files_per_order' => '60',
    'quota_gb' => '50',
    'signup_approval' => '0',
    'owner_email' => '',
    'mail_from' => '',
    'app_version' => '0',
    'bundle_version' => '',
    'bundle_sha256' => '',
    'bundle_min_native' => '0',
    'app_secret' => '',
    'app_notes' => '',
    'privacy_text' => "We store your account details, the files you upload and the videos we deliver on our own server, only to make your videos. We do not sell or share them. Ask us any time to delete your account and files.",
    'bridge_token_hash' => '',
];

function setting(string $name): string
{
    static $cache = null;
    if ($cache === null || $name === '__reload') {
        $cache = [];
        foreach (rows('SELECT name, value FROM settings') as $r) {
            $cache[$r['name']] = (string) $r['value'];
        }
        if ($name === '__reload') {
            return '';
        }
    }
    return $cache[$name] ?? (SETTING_DEFAULTS[$name] ?? '');
}

function set_setting(string $name, string $value): void
{
    if (row('SELECT name FROM settings WHERE name = ?', [$name])) {
        update('settings', ['value' => $value], 'name = ?', [$name]);
    } else {
        insert('settings', ['name' => $name, 'value' => $value]);
    }
    setting('__reload');
}

/** Chunk size for uploads: below the host's PHP post limit (owner's host: 8 MB per request). */
function chunk_bytes(): int
{
    $toBytes = function (string $v): int {
        $v = trim($v);
        $n = (int) $v;
        return match (strtolower(substr($v, -1))) {
            'g' => $n * 1024 ** 3,
            'm' => $n * 1024 ** 2,
            'k' => $n * 1024,
            default => $n,
        };
    };
    $post = $toBytes((string) ini_get('post_max_size')) ?: 8 * 1024 ** 2;
    return (int) max(256 * 1024, min(1536 * 1024, (int) ($post * 0.75)));
}
