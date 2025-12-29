# Remover Secrets relacionados ao SendGrid (instruções)

Se deseja remover os secrets relacionados ao SendGrid (`SENDGRID_API_KEY`, `SENDER_EMAIL`) do seu repositório, siga uma das opções abaixo.

1) Via interface web GitHub (mais simples)
- Vá para seu fork no GitHub → Settings → Secrets and variables → Actions
- Encontre `SENDGRID_API_KEY` e `SENDER_EMAIL` na lista e clique em **Remove** para cada um.

2) Via `gh` CLI (linha de comando)

```bash
# autentique-se primeiro, se necessário
gh auth login

# remover secrets do repositório
gh secret remove SENDGRID_API_KEY --repo <seu-usuario>/Des_Sistemas_Prof_Idirley
gh secret remove SENDER_EMAIL --repo <seu-usuario>/Des_Sistemas_Prof_Idirley
```

3) Remover secrets em um Environment específico
- Vá para Settings → Environments → selecione o Environment (ex.: `UAT`) → Secrets
- Remova os secrets conforme necessário.

Observações de segurança:
- Depois de removidos do GitHub, as chaves não estarão mais disponíveis para os workflows, mas elas podem ter sido usadas antes — rotacione a chave no SendGrid se for o caso.
- Nunca commit suas chaves em código fonte.
