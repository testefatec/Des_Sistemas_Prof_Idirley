// Exemplo ativo: uso inseguro de `eval` em Node.js (detectável pelo CodeQL em JS)
// NÃO execute este código em produção. Use apenas em laboratório isolado.

const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
  const q = url.parse(req.url, true).query;
  const code = q.code || '2+2';

  // Vulnerabilidade: executar entrada do usuário com eval() - code injection
  try {
    const result = eval(code); // <- intencionalmente inseguro
    res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Resultado: ' + String(result));
  } catch (e) {
    res.writeHead(500);
    res.end('Erro ao executar código');
  }
});

server.listen(3000, () => {
  console.log('Servidor rodando em http://localhost:3000');
  console.log('Teste: http://localhost:3000/?code=1+1');
});

// Observação pedagógica: mitigar removendo eval(), usando parsers seguros ou whitelists.
