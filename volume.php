<?php
// public/volume.php
header('Content-Type: application/json; charset=utf-8');
$file = __DIR__ . '/volume.txt';

// Handle POST request: save the new volume level
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $level = isset($_POST['level']) ? intval($_POST['level']) : 50;
    if ($level < 0) $level = 0;
    if ($level > 100) $level = 100;
    file_put_contents($file, $level);
    echo json_encode(['status' => 'ok', 'level' => $level]);
    exit;
}

// Handle GET request with mode=get: return the current volume level
if (isset($_GET['mode']) && $_GET['mode'] === 'get') {
    if (file_exists($file)) {
        $level = intval(file_get_contents($file));
    } else {
        $level = 50;  // default volume level
    }
    echo json_encode(['level' => $level]);
    exit;
}

// Invalid request: return an error response
http_response_code(400);
echo json_encode(['error' => 'Invalid request']);
