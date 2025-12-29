<?php
// Exemplo didático de SQL Injection (A1: Injection)
// ATENÇÃO: este código é intencionalmente inseguro — não usar em produção.

// Simula conexão PDO (ajuste DSN/credenciais para seu ambiente de laboratório)
$dsn = 'mysql:host=localhost;dbname=lab_db;charset=utf8mb4';
$user = 'labuser';
$pass = 'labpass';

try {
    $pdo = new PDO($dsn, $user, $pass);
} catch (PDOException $e) {
    echo "Erro de conexão: " . $e->getMessage();
    exit;
}

// Vulnerabilidade: entrada do usuário concatenada diretamente na query
$id = isset($_GET['id']) ? $_GET['id'] : '1';

$sql = "SELECT id, username, email FROM users WHERE id = $id"; // <- vulnerável
$stmt = $pdo->query($sql);

if ($stmt) {
    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    if ($row) {
        echo "ID: " . htmlspecialchars($row['id']) . "<br>";
        echo "User: " . htmlspecialchars($row['username']) . "<br>";
        echo "Email: " . htmlspecialchars($row['email']) . "<br>";
    } else {
        echo "Nenhum usuário encontrado.";
    }
} else {
    echo "Erro na query: " . implode(" - ", $pdo->errorInfo());
}

// Observação pedagógica: a correção seria usar prepared statements com bindParam.
?>
