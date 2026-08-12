<?php
declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    http_response_code(404);
    exit;
}

require __DIR__ . '/bootstrap.php';

$pdo = db();
$pending = $pdo->exec('DELETE FROM comments WHERE status = "pending" AND created_at < datetime("now", "-30 days")');
$rejected = $pdo->exec('DELETE FROM comments WHERE status = "rejected" AND created_at < datetime("now", "-7 days")');
$limits = $pdo->exec('DELETE FROM rate_limits WHERE window_start < ' . (time() - 86400));

echo "Removed pending=$pending rejected=$rejected rate_limits=$limits\n";
