# Exemplos OWASP Top10 (didático)

Esta pasta contém 5 exemplos intencionalmente vulneráveis para uso em sala de aula. Quatro dos exemplos estão comentados para evitar execução acidental.

Avisos importantes:
- NÃO implante estes arquivos em produção.
- Use apenas em ambientes controlados e isolados (VM local ou rede de laboratório).
- Assegure-se de apagar/rotacionar quaisquer credenciais usadas nos exercícios.

Arquivos:
- `01-sql-injection.php` — exemplo ativo de SQL Injection (A1: Injection)
- `02-reflected-xss.html` — exemplo comentado de XSS refletido (A7: XSS)
- `03-csrf.html` — exemplo comentado de CSRF (A08: CSRF / A5 dependendo da versão)
- `04-insecure-deserialization.py` — exemplo comentado de desserialização insegura (A8/A4 conforme versão)
- `05-hardcoded-credentials.ini` — exemplo comentado de credenciais hardcoded (A2/A9 dependendo da versão)

Use estes exemplos apenas para demonstração e exercícios guiados.
