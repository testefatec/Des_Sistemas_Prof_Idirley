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

1. Crie branch local baseada em `dev`:

```bash
git checkout -b feat/minha-alteracao dev
# editar arquivos
git add .
git commit -m "Minha alteração"
git push origin feat/minha-alteracao
```

2. No GitHub (seu fork), abra um Pull Request para `uat` (base: `uat`, compare: `feat/minha-alteracao`).
3. Quando o PR for aprovado e mergeado para `uat`, a pipeline definida em `.github/workflows/ci-cd.yml` executará CodeQL + gitleaks e fará deploy para o bucket S3 configurado para `uat`.
4. Para promover para produção, abra PR de `uat` para `main`.

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

Para o envio de e-mails pelo workflow PR, crie também:
- `SENDGRID_API_KEY` — chave API do SendGrid (ou outro serviço SMTP)
- `SENDER_EMAIL` — e-mail remetente autorizado no SendGrid

## 9) Notificações por e-mail para o professor

O workflow `.github/workflows/pr_notify.yml` envia um e-mail ao professor (idirley.soares@fatec.sp.gov.br) quando um PR for criado/atualizado, usando SendGrid. O responsável pela turma deve adicionar `SENDGRID_API_KEY` e `SENDER_EMAIL` como secrets no repositório.

## 10) Roteiro de aulas (2 x 30 min)

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
