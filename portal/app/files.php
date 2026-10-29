<?php
// Chunked uploads (the host allows 2 MB per file / 8 MB per request in PHP forms),
// type checks, private storage and downloads with HTTP Range.
declare(strict_types=1);

/** extension => allowed MIME types reported by finfo for that extension. */
const ALLOWED_TYPES = [
    'mp4' => ['video/mp4', 'video/quicktime', 'video/x-m4v', 'application/octet-stream'],
    'm4v' => ['video/mp4', 'video/x-m4v'],
    'mov' => ['video/quicktime', 'video/mp4'],
    'mkv' => ['video/x-matroska', 'video/webm', 'application/octet-stream'],
    'webm' => ['video/webm', 'video/x-matroska'],
    'avi' => ['video/x-msvideo', 'video/avi'],
    '3gp' => ['video/3gpp', 'video/mp4'],
    'jpg' => ['image/jpeg'], 'jpeg' => ['image/jpeg'], 'png' => ['image/png'], 'webp' => ['image/webp'],
    'gif' => ['image/gif'], 'heic' => ['image/heic', 'image/heif'], 'heif' => ['image/heif', 'image/heic'],
    'mp3' => ['audio/mpeg', 'audio/mp3'], 'wav' => ['audio/x-wav', 'audio/wav', 'audio/vnd.wave'],
    'm4a' => ['audio/x-m4a', 'audio/mp4', 'video/mp4'], 'aac' => ['audio/aac', 'audio/x-hx-aac-adts'],
    'ogg' => ['audio/ogg', 'video/ogg'], 'opus' => ['audio/ogg'],
    'pdf' => ['application/pdf'], 'txt' => ['text/plain'], 'srt' => ['text/plain', 'application/x-subrip'],
    'docx' => ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/zip'],
    'zip' => ['application/zip'],
];

/** Types a browser may show inline; everything else is sent as a download. */
function inline_safe(string $mime): bool
{
    return (bool) preg_match('#^(video/(mp4|webm|quicktime|ogg)|image/(jpeg|png|webp|gif)|audio/[a-z0-9.+-]+|application/pdf)$#', $mime);
}

function file_ext(string $name): string
{
    return strtolower(pathinfo($name, PATHINFO_EXTENSION));
}

function safe_name(string $name): string
{
    $name = basename(str_replace('\\', '/', $name));
    $name = preg_replace('/[^\p{L}\p{N} ._()-]+/u', '_', $name) ?? 'file';
    return mb_substr(trim($name, ' .') ?: 'file', 0, 200);
}

function upload_init(int $orderId, string $kind, string $by, string $name, int $size): array
{
    $name = safe_name($name);
    $ext = file_ext($name);
    if (!isset(ALLOWED_TYPES[$ext])) {
        return ['error' => "This file type (.$ext) is not allowed. Send videos, images, audio, PDF, TXT, DOCX or ZIP."];
    }
    $max = (int) setting('max_file_mb') * 1024 * 1024;
    if ($size < 1 || $size > $max) {
        return ['error' => 'File is empty or bigger than ' . setting('max_file_mb') . ' MB.'];
    }
    $count = (int) row('SELECT COUNT(*) AS c FROM files WHERE order_id = ?', [$orderId])['c'];
    if ($count >= (int) setting('max_files_per_order')) {
        return ['error' => 'This order already has the maximum number of files.'];
    }
    // Drop upload sessions nobody finished within 2 days.
    foreach (rows('SELECT token FROM uploads WHERE updated_at < ?', [gmdate('Y-m-d H:i:s', time() - 172800)]) as $old) {
        @unlink(chunk_path($old['token']));
        q('DELETE FROM uploads WHERE token = ?', [$old['token']]);
    }
    $token = bin2hex(random_bytes(20));
    insert('uploads', [
        'token' => $token, 'order_id' => $orderId, 'kind' => $kind, 'uploaded_by' => $by,
        'orig_name' => $name, 'size' => $size, 'received' => 0, 'created_at' => now(), 'updated_at' => now(),
    ]);
    touch(chunk_path($token));
    return ['token' => $token, 'chunk' => chunk_bytes(), 'received' => 0];
}

function chunk_path(string $token): string
{
    return storage_dir() . '/chunks/' . preg_replace('/[^a-f0-9]/', '', $token) . '.part';
}

/** Appends one chunk read from the raw request body. Offset must equal what we already have (resumable). */
function upload_chunk(array $up, int $offset): array
{
    if ($offset !== (int) $up['received']) {
        return ['error' => 'offset_mismatch', 'received' => (int) $up['received']];
    }
    $in = fopen('php://input', 'rb');
    $out = fopen(chunk_path($up['token']), 'ab');
    if (!$in || !$out) {
        return ['error' => 'Server could not store the chunk.'];
    }
    $limit = chunk_bytes() + 1024;
    $wrote = 0;
    while (!feof($in)) {
        $buf = fread($in, 65536);
        if ($buf === false) {
            break;
        }
        $wrote += strlen($buf);
        if ($wrote > $limit || (int) $up['received'] + $wrote > (int) $up['size']) {
            fclose($out);
            ftruncate_to(chunk_path($up['token']), (int) $up['received']);
            return ['error' => 'Chunk too large.'];
        }
        fwrite($out, $buf);
    }
    fclose($out);
    fclose($in);
    $received = (int) $up['received'] + $wrote;
    update('uploads', ['received' => $received, 'updated_at' => now()], 'id = ?', [$up['id']]);
    return ['received' => $received, 'done' => $received === (int) $up['size']];
}

function ftruncate_to(string $path, int $len): void
{
    $h = fopen($path, 'r+b');
    if ($h) {
        ftruncate($h, $len);
        fclose($h);
    }
}

/** Checks the assembled file and moves it into private storage. Returns the files row id. */
function upload_finish(array $up): array
{
    if ((int) $up['received'] !== (int) $up['size']) {
        return ['error' => 'Upload is not complete yet.'];
    }
    $part = chunk_path($up['token']);
    clearstatcache(true, $part);
    if (!is_file($part) || filesize($part) !== (int) $up['size']) {
        return ['error' => 'Uploaded data does not match the file size.'];
    }
    $ext = file_ext($up['orig_name']);
    $mime = (new finfo(FILEINFO_MIME_TYPE))->file($part) ?: 'application/octet-stream';
    if (!in_array($mime, ALLOWED_TYPES[$ext] ?? [], true)) {
        @unlink($part);
        q('DELETE FROM uploads WHERE id = ?', [$up['id']]);
        return ['error' => "The file content ($mime) does not match its .$ext name. It was rejected."];
    }
    $stored = bin2hex(random_bytes(24));
    if (!rename($part, storage_dir() . '/files/' . $stored)) {
        return ['error' => 'Server could not save the file.'];
    }
    $sha = (int) $up['size'] <= 300 * 1024 * 1024 ? hash_file('sha256', storage_dir() . '/files/' . $stored) : null;
    $fid = insert('files', [
        'order_id' => $up['order_id'], 'kind' => $up['kind'], 'orig_name' => $up['orig_name'],
        'stored_name' => $stored, 'mime' => $mime, 'size' => $up['size'], 'sha256' => $sha,
        'uploaded_by' => $up['uploaded_by'], 'created_at' => now(),
    ]);
    q('DELETE FROM uploads WHERE id = ?', [$up['id']]);
    return ['file_id' => $fid, 'name' => $up['orig_name'], 'size' => (int) $up['size'], 'mime' => $mime];
}

function delete_file(array $f): void
{
    @unlink(storage_dir() . '/files/' . $f['stored_name']);
    q('DELETE FROM files WHERE id = ?', [$f['id']]);
}

/** Streams a stored file. Supports a single "Range: bytes=a-b" so videos can be seeked. */
function send_file(array $f, bool $download): never
{
    $path = storage_dir() . '/files/' . $f['stored_name'];
    if (!is_file($path)) {
        abort(404);
    }
    $size = filesize($path);
    $mime = inline_safe($f['mime']) ? $f['mime'] : 'application/octet-stream';
    $disp = ($download || !inline_safe($f['mime'])) ? 'attachment' : 'inline';
    $start = 0;
    $end = $size - 1;
    if (preg_match('/^bytes=(\d*)-(\d*)$/', (string) ($_SERVER['HTTP_RANGE'] ?? ''), $m)) {
        if ($m[1] === '' && $m[2] !== '') {
            $start = max(0, $size - (int) $m[2]);
        } else {
            $start = (int) $m[1];
            if ($m[2] !== '') {
                $end = min($end, (int) $m[2]);
            }
        }
        if ($start > $end || $start >= $size) {
            header("Content-Range: bytes */$size");
            http_response_code(416);
            exit;
        }
        http_response_code(206);
        header("Content-Range: bytes $start-$end/$size");
    }
    header('Content-Type: ' . $mime);
    header('Content-Length: ' . ($end - $start + 1));
    header('Accept-Ranges: bytes');
    header('Cache-Control: private, max-age=3600');
    header('Content-Disposition: ' . $disp . "; filename*=UTF-8''" . rawurlencode($f['orig_name']));
    if (session_status() === PHP_SESSION_ACTIVE) {
        session_write_close();
    }
    @set_time_limit(0);
    while (ob_get_level()) {
        ob_end_clean();
    }
    $h = fopen($path, 'rb');
    fseek($h, $start);
    $left = $end - $start + 1;
    while ($left > 0 && !feof($h) && !connection_aborted()) {
        $buf = fread($h, (int) min(262144, $left));
        echo $buf;
        flush();
        $left -= strlen($buf);
    }
    fclose($h);
    exit;
}
