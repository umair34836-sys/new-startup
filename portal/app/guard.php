<?php
// Blocked-term guard for client-visible text from the bridge (studio messages, version notes, file names).
// Owner rule 2026-10-30: clients only see "Edited by MrCopper804", never the tools or process behind an edit.
// Mirror of portal/bridge/client_text_guard.py (same list; tests/guard_test.py checks they agree). Reasons for each
// choice are written there.
declare(strict_types=1);

const GUARD_BLOCKED = [
    '\bclaude\b', '\banthropic\b', '\ba\.?i\b', '\bartificial\s+intelligence\b', '\bmachine\s+learning\b',
    '\bneural\b', '\bchat\s*gpt\b', '\bgpt\b', '\bopen\s*ai\b', '\bllms?\b', '\bprompt\w*', '\bsessions?\b',
    '\b(?:chat)?bots?\b', '\bautomat\w*', '\bgenerated\b', '\bgenerator\b', '\btts\b',
    '\btext[\s-]*to[\s-]*speech\b', '\bvoxcpm\w*', '\bvoice\s*studio\b', '\bhyper\s*frames?\b', '\bffmpeg\b',
    '\bffprobe\b', '\bwhisper\b', '\bace[\s-]*step\b', '\bskills?\b', '\btemplates?\b', '\bgithub\b',
    '\brepo(?:s|sitory|sitories)?\b', '\bpython\b', '\w+\.py\b', '\beleven\s*labs\b', '\bmidjourney\b',
    '\bstable\s+diffusion\b', '\bplaywright\b', '\bkokoro\b',
];
const GUARD_SQUASHED = ['claude', 'anthropic', 'chatgpt', 'openai', 'voxcpm', 'hyperframes', 'ffmpeg', 'elevenlabs',
    'acestep', 'artificialintelligence', 'midjourney'];
const GUARD_CONFUSABLE = [
    'а' => 'a', 'е' => 'e', 'о' => 'o', 'р' => 'p', 'с' => 'c', 'у' => 'y', 'х' => 'x', 'і' => 'i', 'ј' => 'j', 'ԁ' => 'd',
    'А' => 'A', 'В' => 'B', 'Е' => 'E', 'К' => 'K', 'М' => 'M', 'Н' => 'H', 'О' => 'O', 'Р' => 'P', 'С' => 'C', 'Т' => 'T', 'Х' => 'X',
    'α' => 'a', 'ο' => 'o', 'ι' => 'i', 'ε' => 'e', 'Α' => 'A', 'Ι' => 'I', 'Ο' => 'O', 'Ε' => 'E',
];

function guard_normalise(string $text): string
{
    if (class_exists('Normalizer')) {
        $text = (string) Normalizer::normalize($text, Normalizer::FORM_KC);
    }
    $text = (string) preg_replace('/[\x{00AD}\x{200B}-\x{200F}\x{2060}-\x{2064}\x{FEFF}]/u', '', $text);
    return strtr($text, GUARD_CONFUSABLE);
}

/** Blocked terms found in $text; empty = fine for a client to see. */
function guard_find(string $text): array
{
    $t = guard_normalise($text);
    $hits = [];
    foreach (GUARD_BLOCKED as $p) {
        if (preg_match('/' . $p . '/iu', $t, $m)) {
            $hits[] = $m[0];
        }
    }
    $squashed = (string) preg_replace('/[^a-z]/', '', strtolower($t));
    foreach (GUARD_SQUASHED as $w) {
        if (str_contains($squashed, $w)) {
            $covered = false;
            foreach ($hits as $h) {
                $covered = $covered || str_contains(str_replace(' ', '', strtolower($h)), $w);
            }
            if (!$covered) {
                $hits[] = $w;
            }
        }
    }
    return $hits;
}

/** Tool fingerprints that must not be inside a delivered file (container tags, encoder SEI, renderer names). */
const FILE_MARKERS = ['Lavf5', 'Lavf6', 'Lavc5', 'Lavc6', 'x264 - core', 'x265 (build', 'HyperFrames', 'hyperframes', 'HeadlessChrome',
    'Puppeteer', 'Playwright', 'ffmpeg', 'FFmpeg', 'VoxCPM', 'Claude', 'claude', 'Anthropic'];

/** Returns the first tool marker found in the first 8 MB or the last 2 MB of a file, or null. */
function guard_file_marker(string $path): ?string
{
    $size = filesize($path) ?: 0;
    $fh = fopen($path, 'rb');
    if (!$fh) {
        return null;
    }
    $parts = [fread($fh, 8 * 1024 * 1024) ?: ''];
    if ($size > 10 * 1024 * 1024) {
        fseek($fh, -2 * 1024 * 1024, SEEK_END);
        $parts[] = fread($fh, 2 * 1024 * 1024) ?: '';
    }
    fclose($fh);
    foreach ($parts as $buf) {
        foreach (FILE_MARKERS as $mk) {
            if (str_contains($buf, $mk)) {
                return $mk;
            }
        }
    }
    return null;
}
