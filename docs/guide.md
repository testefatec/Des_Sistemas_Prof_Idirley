# Guia passo-a-passo para alunos — Projeto FATEC

Este guia explica, de forma simples, como configurar o GitHub, fazer fork do repositório `Des_Sistemas_Prof_Idirley` (conta `testefatec`), configurar ambientes (DEV/UAT/PRD), executar PRs e como publicar a página estática na AWS.

Índice
- Configurar Git pela primeira vez
- Fazer fork e clonar o repositório
- Configurar Git para usar seu nome/e-mail
- Criar branches e usar ambientes (DEV/UAT/PRD)
- Como criar PRs para UAT / PRD
- Workflow: o que cada etapa faz (CodeQL, gitleaks, deploy)
- Configurar AWS (IAM, S3, CloudFront) e secrets no GitHub

See também: passos detalhados de deploy S3 em `docs/s3-deploy.md`.
- Como a professora receberá notificações por e-mail
- Roteiro de duas aulas (2x30min)

---

## 1) Configurar Git pela primeira vez

1. Instale Git (Windows): https://git-scm.com/downloads
2. Abra o terminal (Git Bash ou PowerShell)
3. Configure seu nome e e-mail (substitua pelos seus dados):

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@provedor.com"
```

Esses dados aparecem em commits e PRs — assegure que são os seus.

## 2) Fazer fork e clonar o repositório

1. Acesse: https://github.com/testefatec/Des_Sistemas_Prof_Idirley
2. Clique em **Fork** (canto superior direito) — isso cria uma cópia na sua conta.
3. Clone o fork localmente:

```bash
git clone https://github.com/<seu-usuario>/Des_Sistemas_Prof_Idirley.git
cd Des_Sistemas_Prof_Idirley
```

4. Adicione o repositório upstream (opcional, para sincronizar com a origem do professor):

```bash
git remote add upstream https://github.com/testefatec/Des_Sistemas_Prof_Idirley.git
git fetch upstream
```

## 3) Garantir deploys com seu nome / e-mail

- Commits e PRs feitos por você (localmente) já aparecerão com seu nome/e-mail.
- Se um workflow do GitHub fizer commits automáticos e você quiser que eles sejam atribuídos a você, crie um Personal Access Token (PAT) e adicione como `PERSONAL_TOKEN` no seu fork (Settings > Secrets).
- O workflow pode usar esse PAT para fazer commits com `git config user.name` / `user.email` antes de commitar.

## 4) Branches e Environments (DEV / UAT / PRD)

- Usaremos 3 branches na prática: `dev` (desenvolvimento), `uat` (teste) e `main` (produção/PRD).
- No GitHub (Settings > Environments) crie 3 *Environments*: `DEV`, `UAT`, `PRD`. Cada environment pode ter secrets e regras de proteção.

Fluxo simples:
- Trabalhe na branch `dev` localmente e abra PR para `uat` quando estiver pronto para teste.
- Após validação em `uat`, abra PR de `uat` para `main` para promover para produção.

## 5) Como fazer PRs para UAT / PRD
Este passo-a-passo é para quem nunca usou o GitHub — explicações claras e comandos exatos.

Fluxo resumido:
- Trabalhe em uma branch nova a partir de `dev`.
- Abra um PR do seu branch para `uat` (teste).
- Após merge em `uat`, abra um PR de `uat` para `main` (produção).

Passo-a-passo detalhado (FOR DUMMIES):

1) Preparar o repositório local (já clonou seu fork?):

```bash
# entre na pasta do repositório
cd Des_Sistemas_Prof_Idirley

# verifique branches e troque para dev
git fetch origin
git checkout dev
git pull origin dev
```

2) Criar sua branch nova (sempre um nome claro):

```bash
git checkout -b feat/meu-nome
```

3) Fazer alterações (edite arquivos no editor, ex.: adicione seu nome em `index.html`).

4) Salvar, adicionar e commitar:

```bash
git add .
git commit -m "Adiciona nome do aluno: Seu Nome"
```

5) Enviar sua branch para o GitHub (push):

```bash
git push origin feat/meu-nome
```

6) Abrir o Pull Request na interface web (passo a passo):

- Acesse `https://github.com/<seu-usuario>/Des_Sistemas_Prof_Idirley` (substitua `<seu-usuario>` pelo seu usuário GitHub).
- Clique em **Pull requests** → **New pull request**.
- Em **base repository / base**, selecione `uat`.
- Em **compare**, selecione `feat/meu-nome` (sua branch).
- Escreva um título claro (ex.: "Adiciona nome do aluno") e uma descrição curta.
- Clique em **Create pull request**.

7) Se o revisor pedir mudanças:

- Faça as correções localmente na mesma branch `feat/meu-nome`.
- `git add` → `git commit` → `git push origin feat/meu-nome` novamente.
- O PR será atualizado automaticamente com seus novos commits.

8) Merge e deploy para UAT:

- Quando o PR for aprovado, clique em **Merge pull request** → **Confirm merge**.
- Após o merge, o workflow `ci-cd.yml` executará CodeQL, gitleaks e deploy para o bucket S3 de UAT. Verifique em **Actions** se houve sucesso.

9) Promover UAT → PRD (main):

- No GitHub, abra um novo PR onde **base** = `main` e **compare** = `uat`.
- Escreva a descrição (ex.: "Promove alterações testadas em UAT para produção").
- Após aprovação e merge, o workflow rodará para a `main` e fará deploy para PRD.

Dicas extras para iniciantes:
- Para criar a branch no site: abra o repositório no GitHub, clique em **main/dev**, digite `feat/meu-nome` e pressione Enter (cria a branch a partir da selecionada).
- Se o `git push` pedir senha, use o `gh auth login` ou crie um Personal Access Token (PAT) e use como sua senha HTTPS.
- Sempre dê nomes claros para as branches (`feat/`, `fix/`, `docs/`) e mensagens de commit descritivas.

Quer que eu gere um `PR_CHECKLIST.md` imprimível com estes passos? (Posso criar agora.)

## 6) O que faz o pipeline (`.github/workflows/ci-cd.yml`)

- CodeQL: analisa código para vulnerabilidades conhecidas (varredura estática).
- gitleaks: procura segredos/acessos expostos no repositório.
- Deploy: sincroniza os arquivos do repositório para um bucket S3 (site estático). O job de deploy usa secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET).

Cada job é sequencial: primeiro CodeQL, depois secret-scan e por fim deploy.

## 7) Configurar AWS (steps fáceis)

Passo-a-passo mínimo para criar recursos na AWS e gerar as credenciais que o workflow usará.

1) Criar um usuário IAM com permissão de deploy (console AWS > IAM > Users > Add user):
   - Nome: `git-deploy-<seu-nome>`
   - Tipo de credenciais: Programmatic access

2) Criar policy customizada (JSON) para permitir S3 e CloudFront (exemplo mínimo):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::{BUCKET_NAME}",
        "arn:aws:s3:::{BUCKET_NAME}/*"
      ]
    }
  ]
}
```

3) Anexe a policy ao usuário criado. Copie o `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` gerados.

4) Criar o bucket S3 (Console > S3 > Create bucket):
   - Nome único (ex: `fatec-curso-sec-<seu-nome>-uat`)
   - Desmarque "Block all public access" apenas se for usar hospedagem pública (ou configure CloudFront).
   - Em Properties > Static website hosting: habilite e defina `index.html`.

5) (Opcional) Criar distribuição CloudFront apontando para o bucket S3 para HTTPS e cache.

## 8) Secrets no GitHub (repositório / environment)

No seu fork > Settings > Secrets and variables > Actions > New repository secret (ou adicionar a um Environment específico):
- `AWS_ACCESS_KEY_ID` — do usuário IAM
- `AWS_SECRET_ACCESS_KEY` — do usuário IAM
- `AWS_REGION` — ex: `us-east-1`
- `S3_BUCKET` — nome do bucket

Observação: o projeto não utiliza notificações por e-mail automáticas via workflow. Não é necessário criar keys do SendGrid para este repositório.

## 9) Roteiro de aulas (2 x 30 min)

Aula 1 (30 min) — Fundamentos e Git
- 0–5min: Apresentação do objetivo da atividade
- 5–15min: Configurar Git local (user.name, user.email) e criar conta GitHub
- 15–25min: Fazer fork do repositório `testefatec/Des_Sistemas_Prof_Idirley`, clonar e executar alteração simples no `index.html` (adicionar nome)
- 25–30min: Pushing e abrir PR para `uat`

Aula 2 (30 min) — CI/CD e deploy
- 0–5min: Revisar fluxo de PR e branches (dev → uat → main)
- 5–15min: Explicar workflow: CodeQL, gitleaks, deploy
- 15–25min: Criar AWS IAM + bucket S3 (ou guiar com pré-configuração do professor)
- 25–30min: Merge do PR em `uat`, acompanhar execução do workflow e validar página publicada

Observações pedagógicas:
- Para turmas iniciantes é recomendável que o professor pre-crie o bucket S3 e IAM, e compartilhe as credenciais via secrets de turma (ou guiar passo-a-passo com alunos em pares).

---

Arquivos principais criados neste repositório:
- [index.html](index.html)
- [README.md](README.md)
- [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)
- [.github/workflows/pr_notify.yml](.github/workflows/pr_notify.yml)
- [.github/dependabot.yml](.github/dependabot.yml)
