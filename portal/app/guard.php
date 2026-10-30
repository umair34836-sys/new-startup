<?php
// Blocked-term guard for client-visible text from the bridge (studio messages, version notes, file names).
// Owner rule 2026-10-30: clients only see "Edited by MrCopper804", never the tools or process behind an edit.
// Mirror of portal/bridge/client_text_guard.py (same list; tests/guard_test.py checks they agree). Reasons for each
// choice are written there.
declare(strict_types=1);

const GUARD_BLOCKED = [
    '\\bclaude\\b', '\\banthropic\\b', '\\ba\\.?i\\b', '\\bartificial\\s+intelligence\\b',
    '\\bmachine\\s+learning\\b', '\\bneural\\b', '\\bchat\\s*gpt\\b', '\\bgpt\\b', '\\bopen\\s*ai\\b', '\\bllms?\\b',
    '\\bprompt\\w*', '\\bsessions?\\b', '\\b(?:chat)?bots?\\b', '\\bautomat\\w*', '\\bgenerated\\b',
    '\\bgenerator\\b', '\\btts\\b', '\\btext[\\s-]*to[\\s-]*speech\\b', '\\bvoxcpm\\w*', '\\bvoice\\s*studio\\b',
    '\\bhyper\\s*frames?\\b', '\\bffmpeg\\b', '\\bffprobe\\b', '\\bwhisper\\b', '\\bace[\\s-]*step\\b',
    '\\bskills?\\b', '\\btemplates?\\b', '\\bgithub\\b', '\\brepo(?:s|sitory|sitories)?\\b', '\\bpython\\b',
    '\\w+\\.py\\b', '\\beleven\\s*labs\\b', '\\bmidjourney\\b', '\\bstable\\s+diffusion\\b', '\\bplaywright\\b',
    '\\bkokoro\\b', 'session_[A-Za-z0-9]{6,}', '\\bpb_[0-9a-f]{8,}', '\\btrig_[A-Za-z0-9]{6,}',
    '\\benv_[A-Za-z0-9]{6,}', '\\bgen\\s*ai\\b', '\\bml\\s+models?\\b', '\\bgemini\\b', '\\bsuno\\b', '\\budio\\b',
    '\\bkling\\b', '\\bdall\\W?e\\b', '\\bcanva\\b', '\\bcap\\s*cut\\b', '\\bcopilot\\b', '\\bgrok\\b',
    '\\b(?:synthetic|cloned|clone)\\s+voices?\\b', '\\bvoice\\s+clon\\w*', '\\b11\\s*labs\\b', 'github\\w*',
    '\\bgit\\.io\\b', 'एआई', 'आर्टिफिशियल', 'कृत्रिम\\s*बुद्धि', 'اے\\s*آئی', 'مصنوعی\\s*ذہانت',
];
const GUARD_SQUASHED = ['claude', 'anthropic', 'chatgpt', 'openai', 'voxcpm', 'hyperframes', 'ffmpeg', 'elevenlabs', 'acestep', 'artificialintelligence', 'midjourney', 'voicestudio', 'github'];
const GUARD_CONFUSABLE = [
    'а' => 'a', 'е' => 'e', 'о' => 'o', 'р' => 'p', 'с' => 'c', 'у' => 'y', 'х' => 'x', 'і' => 'i', 'ј' => 'j', 'ԁ' => 'd',
    'А' => 'A', 'В' => 'B', 'Е' => 'E', 'К' => 'K', 'М' => 'M', 'Н' => 'H', 'О' => 'O', 'Р' => 'P', 'С' => 'C', 'Т' => 'T', 'Х' => 'X',
    'α' => 'a', 'ο' => 'o', 'ι' => 'i', 'ε' => 'e', 'Α' => 'A', 'Ι' => 'I', 'Ο' => 'O', 'Ε' => 'E',
];

function guard_normalise(string $text): string
{
    if (class_exists('Normalizer')) {
        $text = (string) Normalizer::normalize($text, Normalizer::FORM_KC);
        // Only the Latin combining accents (U+0300-036F) are dropped ("Claudé" -> "Claude").
        $text = (string) Normalizer::normalize((string) preg_replace('/[\x{0300}-\x{036F}]/u', '',
            (string) Normalizer::normalize($text, Normalizer::FORM_KD)), Normalizer::FORM_C);
    }
    $text = (string) preg_replace('/[\x{00AD}\x{200B}-\x{200F}\x{2060}-\x{2064}\x{FEFF}]/u', '', $text);
    return strtr($text, GUARD_CONFUSABLE);
}

/** Blocked terms found in $text; empty = fine for a client to see. */
function guard_find(string $text): array
{
    $t = guard_normalise($text);
    $hits = [];
    // Without the intl extension there is no NFKC: refuse full-width / math-alphabet / accented look-alike letters
    // rather than let them slip past the list.
    if (!class_exists('Normalizer') && preg_match('/[\x{FF00}-\x{FFEF}\x{1D400}-\x{1D7FF}\x{0300}-\x{036F}]/u', $t)) {
        $hits[] = 'unusual letters';
    }
    foreach (GUARD_BLOCKED as $p) {
        if (preg_match('/' . $p . '/iu', $t, $m)) {
            $hits[] = $m[0];
        }
    }
    $squashed = (string) preg_replace('/[^a-z]/', '', strtr(strtolower($t), '0134578@$', 'oleastbas'));
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
    'Puppeteer', 'Playwright', 'ffmpeg', 'FFmpeg', 'VoxCPM', 'Claude', 'claude', 'Anthropic', 'c2pa', 'jumb', '<x:xmpmeta',
    "Exif\0\0", 'trainedAlgorithmicMedia'];

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
