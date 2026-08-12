<?php
declare(strict_types=1);

require __DIR__ . '/bootstrap.php';

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (($_GET['overview'] ?? '') === '1') {
        $recent = db()->query(
            'SELECT page_slug, display_name, body, created_at FROM comments
             WHERE status = "approved" ORDER BY created_at DESC LIMIT 100'
        )->fetchAll();
        $top = db()->query(
            'SELECT page_slug, ROUND(AVG(score), 1) AS average, COUNT(*) AS count
             FROM ratings GROUP BY page_slug HAVING COUNT(*) > 0
             ORDER BY average DESC, count DESC LIMIT 100'
        )->fetchAll();
        foreach ($recent as &$comment) {
            $comment['page_title'] = review_title((string)$comment['page_slug']);
        }
        unset($comment);
        foreach ($top as &$rating) {
            $rating['page_title'] = review_title((string)$rating['page_slug']);
        }
        unset($rating);
        json_response(['recentComments' => $recent, 'topRated' => $top, 'csrf' => csrf_token()]);
    }

    $slug = valid_slug((string)($_GET['page'] ?? ''));
    if (!review_exists($slug)) {
        json_response(['error' => 'Review not found.'], 404);
    }
    json_response([
        'page' => $slug,
        'rating' => rating_summary($slug),
        'comments' => approved_comments($slug),
        'recommendations' => recommendations($slug),
        'csrf' => csrf_token(),
    ]);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Allow: GET, POST');
    json_response(['error' => 'Method not allowed.'], 405);
}

$input = request_json();
require_csrf($input);
$action = (string)($input['action'] ?? '');
$slug = valid_slug((string)($input['page'] ?? ''));
if (!review_exists($slug)) {
    json_response(['error' => 'Review not found.'], 404);
}

if ($action === 'rate') {
    enforce_rate_limit('rating', 20, 3600);
    $score = filter_var($input['score'] ?? null, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 5]]);
    if ($score === false) {
        json_response(['error' => 'Rating must be between 1 and 5.'], 422);
    }
    $statement = db()->prepare(
        'INSERT INTO ratings(page_slug, score, visitor_hash) VALUES(?, ?, ?)
         ON CONFLICT(page_slug, visitor_hash)
         DO UPDATE SET score = excluded.score, updated_at = CURRENT_TIMESTAMP'
    );
    $statement->execute([$slug, $score, visitor_hash()]);
    json_response(['ok' => true, 'rating' => rating_summary($slug)]);
}

if ($action === 'comment') {
    enforce_rate_limit('comment', 2, 600);
    $name = clean_text((string)($input['name'] ?? ''));
    $body = clean_text((string)($input['body'] ?? ''));
    $website = clean_text((string)($input['website'] ?? ''));
    $startedAt = filter_var($input['startedAt'] ?? null, FILTER_VALIDATE_INT) ?: 0;

    if (mb_strlen($name) < 2 || mb_strlen($name) > 40) {
        json_response(['error' => 'Display name must be 2–40 characters.'], 422);
    }
    if (mb_strlen($body) < 10 || mb_strlen($body) > 1000) {
        json_response(['error' => 'Comment must be 10–1,000 characters.'], 422);
    }
    if (comment_is_spam($name, $body, $website, $startedAt)) {
        json_response(['ok' => true, 'message' => 'Your comment was received for moderation.'], 202);
    }

    $statement = db()->prepare(
        'INSERT INTO comments(page_slug, display_name, body, visitor_hash) VALUES(?, ?, ?, ?)'
    );
    $statement->execute([$slug, $name, $body, visitor_hash()]);
    json_response(['ok' => true, 'message' => 'Your comment was received for moderation.'], 202);
}

json_response(['error' => 'Unknown action.'], 400);
