<?php
declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    http_response_code(404);
    exit;
}

require __DIR__ . '/bootstrap.php';

$command = $argv[1] ?? 'list';
if ($command === 'list') {
    $comments = db()->query(
        'SELECT id, page_slug, display_name, body, created_at
         FROM comments WHERE status = "pending" ORDER BY created_at ASC LIMIT 100'
    )->fetchAll();
    foreach ($comments as $comment) {
        echo sprintf(
            "[%d] %s | %s | %s\n%s\n\n",
            $comment['id'],
            $comment['page_slug'],
            $comment['display_name'],
            $comment['created_at'],
            $comment['body']
        );
    }
    exit;
}

if (!in_array($command, ['approve', 'reject'], true) || !isset($argv[2]) || !ctype_digit($argv[2])) {
    fwrite(STDERR, "Usage: php moderate.php [list|approve ID|reject ID]\n");
    exit(2);
}

$status = $command === 'approve' ? 'approved' : 'rejected';
$statement = db()->prepare('UPDATE comments SET status = ?, moderated_at = CURRENT_TIMESTAMP WHERE id = ?');
$statement->execute([$status, (int)$argv[2]]);
echo "Updated {$statement->rowCount()} comment(s) to $status.\n";
