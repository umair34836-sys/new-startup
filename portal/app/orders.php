<?php
// Orders, questionnaire, pricing, versions, messages and the bridge event outbox.
declare(strict_types=1);

const ORDER_STATUSES = [
    'draft' => 'Draft',
    'submitted' => 'Received',
    'in_progress' => 'In editing',
    'delivered' => 'Ready to review',
    'revision' => 'Changes requested',
    'approved' => 'Approved',
];

/** The questionnaire. type: select | text | number | date | checkbox. */
function questions(): array
{
    return [
        'video_type' => ['label' => 'What kind of video is this?', 'type' => 'select', 'required' => true, 'options' => [
            'Promo / Ad', 'Reel / Short / TikTok', 'YouTube video', 'Tutorial / Screen recording', 'Explainer',
            'Wedding / Event', 'Gaming', 'Podcast / Talking head', 'Product showcase', 'Other']],
        'platform' => ['label' => 'Where will it be posted?', 'type' => 'select', 'required' => true, 'options' => [
            'Instagram / Facebook', 'TikTok', 'YouTube', 'YouTube Shorts', 'WhatsApp', 'Website', 'Other']],
        'aspect' => ['label' => 'Shape of the video', 'type' => 'select', 'required' => true, 'options' => [
            '9:16 vertical (phone)', '16:9 wide (YouTube)', '1:1 square', '4:5 portrait', 'Not sure']],
        'style' => ['label' => 'Editing style', 'type' => 'select', 'required' => true, 'options' => [
            'Energetic / fast cuts', 'Cinematic', 'Clean / minimal', 'Funny / memes', 'Emotional',
            'Corporate / professional', 'Not sure, you decide']],
        'music' => ['label' => 'Music mood', 'type' => 'select', 'required' => false, 'options' => [
            'Upbeat', 'Calm', 'Epic', 'Romantic', 'Hip-hop / phonk', 'No music', 'You decide']],
        'voice' => ['label' => 'Voice', 'type' => 'select', 'required' => false, 'options' => [
            'Keep the voice in my footage', 'Add a voiceover from my script', 'No voice', 'You decide']],
        'captions' => ['label' => 'Captions / subtitles', 'type' => 'select', 'required' => false, 'options' => [
            'No captions', 'English', 'Urdu', 'Roman Urdu', 'Hindi', 'Other (write in ideas)']],
        'language' => ['label' => 'Language spoken in the video', 'type' => 'text', 'required' => false, 'max' => 60],
        'brand' => ['label' => 'Business / channel name (if any)', 'type' => 'text', 'required' => false, 'max' => 120],
        'cta' => ['label' => 'What should viewers do at the end? (call, visit website, subscribe...)', 'type' => 'text', 'required' => false, 'max' => 200],
        'references' => ['label' => 'Example videos you like (links)', 'type' => 'text', 'required' => false, 'max' => 1000],
        'deadline' => ['label' => 'When do you need it?', 'type' => 'date', 'required' => false],
    ];
}

function clean_answers(array $in, bool $strict): array
{
    $out = [];
    $errors = [];
    foreach (questions() as $key => $q) {
        $v = $in[$key] ?? '';
        $v = is_string($v) ? trim($v) : '';
        if ($q['type'] === 'select' && $v !== '' && !in_array($v, $q['options'], true)) {
            $v = '';
        }
        if ($q['type'] === 'date' && $v !== '' && !preg_match('/^\d{4}-\d{2}-\d{2}$/', $v)) {
            $v = '';
        }
        if ($q['type'] === 'text') {
            $v = mb_substr($v, 0, $q['max'] ?? 200);
        }
        if ($strict && $q['required'] && $v === '') {
            $errors[] = 'Please answer: ' . $q['label'];
        }
        $out[$key] = $v;
    }
    return [$out, $errors];
}

/** Rate per second for this client in their currency (client override, else the default). */
function rate_for(array $user, string $currency): float
{
    if (($user['rate'] ?? null) !== null && $user['rate'] !== '' && $currency === $user['currency']) {
        return (float) $user['rate'];
    }
    return currencies()[$currency] ?? 0.0;
}

function estimate(int $seconds, float $rate): float
{
    return round(max(0, $seconds) * $rate, 2);
}

function order_for_user(int $orderId, array $user): array
{
    $o = row('SELECT * FROM orders WHERE id = ?', [$orderId]);
    if (!$o || ($user['role'] !== 'admin' && (int) $o['user_id'] !== (int) $user['id'])) {
        abort(404);
    }
    return $o;
}

function create_draft(array $user): int
{
    $rate = rate_for($user, $user['currency']);
    return insert('orders', [
        'user_id' => $user['id'],
        'title' => 'New video',
        'status' => 'draft',
        'answers' => json_encode([]),
        'currency' => $user['currency'],
        'rate' => $rate,
        'created_at' => now(),
        'updated_at' => now(),
    ]);
}

function save_order_form(array $order, array $user, array $post, bool $submit): array
{
    [$answers, $errors] = clean_answers($post['q'] ?? [], $submit);
    $title = mb_substr(trim((string) ($post['title'] ?? '')), 0, 160);
    $len = (int) ($post['length_sec'] ?? 0);
    if ($title === '') {
        $title = 'New video';
        if ($submit) {
            $errors[] = 'Give your video a name.';
        }
    }
    if ($len < 0 || $len > 36000) {
        $errors[] = 'Length must be between 1 second and 10 hours.';
        $len = 0;
    }
    if ($submit && $len < 1) {
        $errors[] = 'Tell us how long the finished video should be (in seconds).';
    }
    if ($submit && !row("SELECT id FROM files WHERE order_id = ? AND kind = 'input'", [$order['id']])) {
        $errors[] = 'Upload at least one file (video, images or script).';
    }
    $rate = rate_for($user, $order['currency']);
    $data = [
        'title' => $title,
        'answers' => json_encode($answers, JSON_UNESCAPED_UNICODE),
        'script' => mb_substr((string) ($post['script'] ?? ''), 0, 20000),
        'ideas' => mb_substr((string) ($post['ideas'] ?? ''), 0, 10000),
        'length_sec' => $len,
        'rate' => $rate,
        'estimate' => estimate($len, $rate),
        'updated_at' => now(),
    ];
    update('orders', $data, 'id = ? AND status = ?', [$order['id'], 'draft']);
    if ($submit && !$errors) {
        update('orders', ['status' => 'submitted', 'submitted_at' => now()], 'id = ?', [$order['id']]);
        add_event((int) $order['id'], 'order_submitted');
    }
    return $errors;
}

function add_event(int $orderId, string $type): void
{
    insert('events', ['order_id' => $orderId, 'type' => $type, 'created_at' => now()]);
    notify_event($orderId, $type);
}

function add_message(int $orderId, string $sender, string $body, string $kind = 'note', ?int $versionId = null): int
{
    return insert('messages', [
        'order_id' => $orderId,
        'sender' => $sender,
        'kind' => $kind,
        'body' => mb_substr($body, 0, 10000),
        'version_id' => $versionId,
        'created_at' => now(),
    ]);
}

function request_changes(array $order, string $body): ?string
{
    if ($order['status'] !== 'delivered') {
        return 'You can ask for changes after a version is ready.';
    }
    if (mb_strlen(trim($body)) < 3) {
        return 'Write what should change.';
    }
    $v = row('SELECT id FROM versions WHERE order_id = ? ORDER BY number DESC LIMIT 1', [$order['id']]);
    add_message((int) $order['id'], 'client', trim($body), 'revision', $v ? (int) $v['id'] : null);
    update('orders', ['status' => 'revision', 'updated_at' => now()], 'id = ?', [$order['id']]);
    add_event((int) $order['id'], 'revision_requested');
    return null;
}

function approve_order(array $order, string $body): ?string
{
    if ($order['status'] !== 'delivered') {
        return 'There is no version to approve yet.';
    }
    add_message((int) $order['id'], 'client', trim($body) !== '' ? trim($body) : 'Perfect, approved.', 'approved');
    update('orders', ['status' => 'approved', 'approved_at' => now(), 'updated_at' => now()], 'id = ?', [$order['id']]);
    add_event((int) $order['id'], 'approved');
    return null;
}

function client_message(array $order, string $body): ?string
{
    if (trim($body) === '') {
        return 'Write a message.';
    }
    add_message((int) $order['id'], 'client', trim($body));
    if (!in_array($order['status'], ['draft', 'approved'], true)) {
        add_event((int) $order['id'], 'client_message');
    }
    return null;
}

/** Called when a finished file is attached as a new version (by the bridge or the admin). */
function add_version(int $orderId, int $fileId, string $note): int
{
    $n = (int) (row('SELECT MAX(number) AS n FROM versions WHERE order_id = ?', [$orderId])['n'] ?? 0) + 1;
    $vid = insert('versions', ['order_id' => $orderId, 'number' => $n, 'file_id' => $fileId, 'note' => $note, 'created_at' => now()]);
    add_message($orderId, 'studio', $note !== '' ? $note : "Version $n is ready.", 'delivery', $vid);
    update('orders', ['status' => 'delivered', 'updated_at' => now()], 'id = ?', [$orderId]);
    notify_delivery($orderId, $n);
    return $vid;
}

function order_answers(array $order): array
{
    $a = json_decode((string) $order['answers'], true);
    return is_array($a) ? $a : [];
}
