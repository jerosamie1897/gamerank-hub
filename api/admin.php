<?php
declare(strict_types=1);

require __DIR__ . '/bootstrap.php';

$expected = trim((string)@file_get_contents(ADMIN_TOKEN_PATH));
$provided = (string)($_SERVER['HTTP_X_ADMIN_TOKEN'] ?? '');
if ($expected === '' || $provided === '' || !hash_equals($expected, $provided)) {
    json_response(['error' => 'Unauthorized.'], 401);
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $comments = db()->query(
        'SELECT id, page_slug, display_name, body, created_at
         FROM comments WHERE status = "pending" ORDER BY created_at ASC LIMIT 100'
    )->fetchAll();
    json_response(['comments' => $comments]);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = request_json();
    $id = filter_var($input['id'] ?? null, FILTER_VALIDATE_INT);
    $status = (string)($input['status'] ?? '');
    if ($id === false || !in_array($status, ['approved', 'rejected'], true)) {
        json_response(['error' => 'Invalid moderation action.'], 422);
    }
    $statement = db()->prepare('UPDATE comments SET status = ?, moderated_at = CURRENT_TIMESTAMP WHERE id = ?');
    $statement->execute([$status, $id]);
    json_response(['ok' => true, 'updated' => $statement->rowCount()]);
}

header('Allow: GET, POST');
json_response(['error' => 'Method not allowed.'], 405);
