<?php
declare(strict_types=1);

const SITE_ROOT = __DIR__ . '/..';
const DB_PATH_DEFAULT = '/var/lib/gamerankhub/community.sqlite';
const SECRET_PATH = '/etc/gamerankhub/app-secret';
const ADMIN_TOKEN_PATH = '/etc/gamerankhub/admin-token';

function json_response(array $payload, int $status = 200): never
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($payload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function app_secret(): string
{
    $secret = @file_get_contents(SECRET_PATH);
    if ($secret === false || strlen(trim($secret)) < 32) {
        json_response(['error' => 'Community service is not configured.'], 503);
    }
    return trim($secret);
}

function db(): PDO
{
    static $pdo;
    if ($pdo instanceof PDO) {
        return $pdo;
    }

    $path = getenv('GAMEHUB_DB_PATH') ?: DB_PATH_DEFAULT;
    $pdo = new PDO('sqlite:' . $path, null, null, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ]);
    $pdo->exec('PRAGMA journal_mode=WAL');
    $pdo->exec('PRAGMA foreign_keys=ON');
    $pdo->exec('PRAGMA busy_timeout=5000');
    $pdo->exec(
        'CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_slug TEXT NOT NULL,
            display_name TEXT NOT NULL,
            body TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT "pending" CHECK(status IN ("pending", "approved", "rejected")),
            visitor_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            moderated_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_comments_page_status ON comments(page_slug, status, created_at DESC);
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_slug TEXT NOT NULL,
            score INTEGER NOT NULL CHECK(score BETWEEN 1 AND 5),
            visitor_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(page_slug, visitor_hash)
        );
        CREATE INDEX IF NOT EXISTS idx_ratings_page ON ratings(page_slug);
        CREATE TABLE IF NOT EXISTS rate_limits (
            identity_hash TEXT NOT NULL,
            action TEXT NOT NULL,
            window_start INTEGER NOT NULL,
            request_count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY(identity_hash, action, window_start)
        );'
    );
    return $pdo;
}

function valid_slug(string $value): string
{
    $slug = strtolower(trim($value));
    if (!preg_match('/^[a-z0-9][a-z0-9-]{1,79}$/', $slug)) {
        json_response(['error' => 'Invalid page identifier.'], 400);
    }
    return $slug;
}

function review_index(): array
{
    static $index = null;
    if ($index === null) {
        $decoded = json_decode((string)@file_get_contents(SITE_ROOT . '/assets/search-index.json'), true);
        $index = is_array($decoded) ? $decoded : [];
    }
    return $index;
}

function review_title(string $slug): ?string
{
    foreach (review_index() as $item) {
        if (($item['url'] ?? '') === "reviews/$slug.html") {
            return preg_replace('/ Review:.*$/', '', (string)($item['title'] ?? $slug)) ?: $slug;
        }
    }
    return null;
}

function review_exists(string $slug): bool
{
    return review_title($slug) !== null;
}

function client_identity(): string
{
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    return hash_hmac('sha256', $ip, app_secret());
}

function visitor_hash(): string
{
    $visitor = $_COOKIE['gh_visitor'] ?? '';
    if (!preg_match('/^[a-f0-9]{32}$/', $visitor)) {
        $visitor = bin2hex(random_bytes(16));
        setcookie('gh_visitor', $visitor, [
            'expires' => time() + 31536000,
            'path' => '/',
            'secure' => true,
            'httponly' => true,
            'samesite' => 'Lax',
        ]);
    }
    return hash_hmac('sha256', $visitor, app_secret());
}

function csrf_token(): string
{
    $token = $_COOKIE['gh_csrf'] ?? '';
    if (!preg_match('/^[a-f0-9]{64}$/', $token)) {
        $token = bin2hex(random_bytes(32));
        setcookie('gh_csrf', $token, [
            'expires' => time() + 7200,
            'path' => '/',
            'secure' => true,
            'httponly' => true,
            'samesite' => 'Strict',
        ]);
    }
    return $token;
}

function require_csrf(array $input): void
{
    $cookie = $_COOKIE['gh_csrf'] ?? '';
    $provided = (string)($input['csrf'] ?? '');
    if ($cookie === '' || $provided === '' || !hash_equals($cookie, $provided)) {
        json_response(['error' => 'Your session expired. Refresh and try again.'], 403);
    }
}

function request_json(): array
{
    $raw = file_get_contents('php://input');
    if ($raw === false || strlen($raw) > 4096) {
        json_response(['error' => 'Invalid request body.'], 400);
    }
    try {
        $input = json_decode($raw, true, 16, JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        json_response(['error' => 'Invalid JSON.'], 400);
    }
    if (!is_array($input)) {
        json_response(['error' => 'Invalid request body.'], 400);
    }
    return $input;
}

function enforce_rate_limit(string $action, int $limit, int $windowSeconds): void
{
    $pdo = db();
    $identity = client_identity();
    $window = intdiv(time(), $windowSeconds) * $windowSeconds;
    $pdo->beginTransaction();
    try {
        $statement = $pdo->prepare(
            'INSERT INTO rate_limits(identity_hash, action, window_start, request_count)
             VALUES(?, ?, ?, 1)
             ON CONFLICT(identity_hash, action, window_start)
             DO UPDATE SET request_count = request_count + 1'
        );
        $statement->execute([$identity, $action, $window]);
        $count = (int)$pdo->query(
            'SELECT request_count FROM rate_limits
             WHERE identity_hash = ' . $pdo->quote($identity) .
            ' AND action = ' . $pdo->quote($action) .
            ' AND window_start = ' . $window
        )->fetchColumn();
        $pdo->commit();
    } catch (Throwable $error) {
        $pdo->rollBack();
        throw $error;
    }
    if ($count > $limit) {
        json_response(['error' => 'Too many requests. Please try again later.'], 429);
    }
    if (random_int(1, 100) === 1) {
        $cutoff = time() - 86400;
        $pdo->exec('DELETE FROM rate_limits WHERE window_start < ' . $cutoff);
    }
}

function clean_text(string $value): string
{
    return trim(preg_replace('/\s+/u', ' ', strip_tags($value)) ?? '');
}

function comment_is_spam(string $name, string $body, string $website, int $startedAt): bool
{
    if ($website !== '' || $startedAt <= 0 || $startedAt > time() - 3) {
        return true;
    }
    $combined = strtolower($name . ' ' . $body);
    if (preg_match_all('/https?:\/\//i', $body) > 1) {
        return true;
    }
    if (preg_match('/(.)\1{9,}/u', $combined)) {
        return true;
    }
    return (bool)preg_match('/\b(casino|payday loan|crypto giveaway|buy followers)\b/i', $combined);
}

function rating_summary(string $slug): array
{
    $statement = db()->prepare('SELECT ROUND(AVG(score), 1) AS average, COUNT(*) AS count FROM ratings WHERE page_slug = ?');
    $statement->execute([$slug]);
    $row = $statement->fetch() ?: ['average' => null, 'count' => 0];
    return ['average' => $row['average'] === null ? null : (float)$row['average'], 'count' => (int)$row['count']];
}

function approved_comments(string $slug, int $limit = 20): array
{
    $statement = db()->prepare(
        'SELECT id, display_name, body, created_at FROM comments
         WHERE page_slug = ? AND status = "approved"
         ORDER BY created_at DESC LIMIT ?'
    );
    $statement->bindValue(1, $slug);
    $statement->bindValue(2, $limit, PDO::PARAM_INT);
    $statement->execute();
    return $statement->fetchAll();
}

function recommendations(string $slug, int $limit = 4): array
{
    $index = review_index();
    $reviews = array_values(array_filter($index, static fn(array $item): bool =>
        str_starts_with((string)($item['url'] ?? ''), 'reviews/') &&
        basename((string)$item['url'], '.html') !== $slug
    ));
    $current = null;
    foreach ($index as $item) {
        if (($item['url'] ?? '') === "reviews/$slug.html") {
            $current = $item;
            break;
        }
    }
    $terms = array_filter(explode(' ', strtolower((string)($current['keywords'] ?? ''))));
    foreach ($reviews as &$review) {
        $haystack = strtolower((string)($review['keywords'] ?? ''));
        $review['_score'] = array_sum(array_map(static fn(string $term): int => str_contains($haystack, $term) ? 1 : 0, $terms));
    }
    unset($review);
    usort($reviews, static fn(array $a, array $b): int => $b['_score'] <=> $a['_score'] ?: strcmp((string)$a['title'], (string)$b['title']));
    return array_map(static fn(array $item): array => [
        'title' => $item['title'],
        'url' => '/' . $item['url'],
        'description' => $item['description'],
    ], array_slice($reviews, 0, $limit));
}
