# PR Checklist (imprimível) — Passo a passo para alunos iniciantes

Use este checklist durante a aula. Marque cada item quando concluído.

1) Preparação local
- [ ] Clonei meu fork e entrei na pasta do projeto:

```bash
git clone https://github.com/<seu-usuario>/Des_Sistemas_Prof_Idirley.git
cd Des_Sistemas_Prof_Idirley
```

- [ ] Configurei `user.name` e `user.email` (se ainda não fez):

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@provedor.com"
```

2) Criar branch para a atividade
- [ ] Criei uma branch nova a partir de `dev`:

```bash
git fetch origin
git checkout dev
git pull origin dev
git checkout -b feat/meu-nome
```

3) Fazer alterações e commitar
- [ ] Editei os arquivos necessários (ex.: `index.html`) e salvei.
- [ ] Adicionei os arquivos e fiz commit:

```bash
git add .
git commit -m "Adiciona nome do aluno: Seu Nome"
```

4) Enviar para o GitHub
- [ ] Enviei a branch para o GitHub:

```bash
git push origin feat/meu-nome
```

5) Abrir Pull Request (PR)
- [ ] No navegador, abra seu fork: `https://github.com/<seu-usuario>/Des_Sistemas_Prof_Idirley`
- [ ] Clique em **Pull requests** → **New pull request**.
- [ ] Configure o PR:
  - **Base**: `uat`
  - **Compare**: `feat/meu-nome`
- [ ] Escreva um título e descrição claros.
- [ ] Clique em **Create pull request**.

6) Se o revisor pedir mudanças
- [ ] Faça correções localmente na mesma branch.
- [ ] `git add` → `git commit` → `git push origin feat/meu-nome` (o PR atualiza automaticamente).

7) Quando aprovado — Merge em UAT
- [ ] Confirme que o PR foi aprovado.
- [ ] Clique em **Merge pull request** → **Confirm merge**.
- [ ] Verifique em **Actions** se o workflow `ci-cd.yml` rodou e o deploy para UAT foi bem-sucedido.

8) Promover UAT → PRD (main)
- [ ] Abra um PR com **base** = `main` e **compare** = `uat`.
- [ ] Peça aprovação e, após merge, verifique deploy em produção (PRD).

9) Troubleshooting rápido
- [ ] Push falhando: execute `gh auth login` ou verifique seu PAT.
- [ ] Workflow falhando: abra Actions → clique no job → veja o log do passo com erro.
- [ ] Erro de permissão S3: confirme `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` nos `secrets` do repositório/environment.

10) Observações finais
- Use nomes de branch claros (`feat/`, `fix/`, `docs/`).
- Não coloque senhas ou chaves em commits.
- Se quiser, cole este checklist em papel e entregue ao professor ao finalizar a atividade.
