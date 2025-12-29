# Deploy para AWS S3 — passo-a-passo

Aviso: eu não tenho suas credenciais AWS, então não posso criar recursos diretamente. Abaixo estão comandos e exemplos que você (ou alunos) podem executar localmente ou no terminal do GitHub Actions.

## Pré-requisitos
- Ter AWS CLI instalado e configurado localmente: `aws configure` (ou usar credenciais temporárias).
- Permissão para criar usuários IAM, policies e buckets S3.

## 1) Criar bucket S3 (exemplo)

Substitua `REGION` e `BUCKET_NAME` pelos valores desejados.

```bash
# Para regiões diferentes de us-east-1
aws s3api create-bucket --bucket BUCKET_NAME --region REGION \
  --create-bucket-configuration LocationConstraint=REGION

# Se for us-east-1 (N. Virginia), use:
aws s3api create-bucket --bucket BUCKET_NAME --region us-east-1
```

## 2) Habilitar hospedagem estática (opcional: público)

```bash
aws s3 website s3://BUCKET_NAME --index-document index.html --error-document index.html
```

Se desejar disponibilizar publicamente, aplique a bucket policy (substitua BUCKET_NAME):

```bash
cat > bucket-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::BUCKET_NAME/*"
    }
  ]
}
EOF

aws s3api put-bucket-policy --bucket BUCKET_NAME --policy file://bucket-policy.json
```

> Observação: para produção recomenda-se usar CloudFront + origin access identity para evitar tornar o bucket público.

## 3) Criar usuário IAM para deploy e obter chaves

# Criar usuário com acesso programático
```bash
aws iam create-user --user-name git-deploy-USERNAME

# Criar policy (usar o arquivo docs/aws/iam-policy.json substituindo <BUCKET_NAME>)
aws iam create-policy --policy-name S3DeployPolicy --policy-document file://docs/aws/iam-policy.json

# Anexar policy ao usuário
aws iam attach-user-policy --user-name git-deploy-USERNAME --policy-arn arn:aws:iam::ACCOUNT_ID:policy/S3DeployPolicy

# Criar access key (salvar os valores retornados)
aws iam create-access-key --user-name git-deploy-USERNAME
```

Guarde `AccessKeyId` e `SecretAccessKey` — serão usados como secrets no GitHub.

## 4) Testar deploy local (sincronizar arquivos)

No diretório do repositório (onde está `index.html`):

```bash
aws s3 sync . s3://BUCKET_NAME --delete --exclude '.git/*' --exclude '.github/*'

# Opcional: definir ACL pública (se não usar bucket policy)
aws s3 sync . s3://BUCKET_NAME --delete --acl public-read --exclude '.git/*' --exclude '.github/*'
```

Abra `http://BUCKET_NAME.s3-website-REGION.amazonaws.com` (ou URL do CloudFront) para verificar.

## 5) Configurar Secrets no GitHub (repositório ou Environment UAT/PRD)

No GitHub → seu fork → Settings → Secrets and variables → Actions → New repository secret.
Adicione os seguintes secrets (exemplos):

- `AWS_ACCESS_KEY_ID` — do passo `create-access-key`
- `AWS_SECRET_ACCESS_KEY` — do passo `create-access-key`
- `AWS_REGION` — ex: `us-east-1`
- `S3_BUCKET` — nome do bucket

Se preferir usar a `gh` CLI:

```bash
gh auth login
gh secret set AWS_ACCESS_KEY_ID --body "AKIA..." --repo <seu-usuario>/Des_Sistemas_Prof_Idirley
gh secret set AWS_SECRET_ACCESS_KEY --body "..." --repo <seu-usuario>/Des_Sistemas_Prof_Idirley
gh secret set AWS_REGION --body "us-east-1" --repo <seu-usuario>/Des_Sistemas_Prof_Idirley
gh secret set S3_BUCKET --body "BUCKET_NAME" --repo <seu-usuario>/Des_Sistemas_Prof_Idirley
```

## 6) Como o GitHub Actions fará o deploy (exemplo no repo)

O workflow em `.github/workflows/ci-cd.yml` usa `aws-actions/configure-aws-credentials` com os secrets acima. O passo final executa:

```bash
aws s3 sync . s3://${{ secrets.S3_BUCKET }} --delete --exclude '.git/*' --exclude '.github/*'
```

Isso sincroniza os arquivos do repositório para o bucket configurado sempre que houver push nas branches `uat` ou `main` (conforme workflow).

## 7) Testes e troubleshooting
- Se os arquivos não aparecem: verifique se o bucket está certo e se a política permite `s3:PutObject`.
- Para permissões negadas: confirme que as credenciais usadas no workflow correspondem ao usuário IAM com policy anexada.
- Logs do workflow: Actions → job → passo `Sync to S3` mostrará saída do `aws s3 sync`.

## 8) Recomendações de segurança para a disciplina
- Prefira criar 2 buckets (ex: `...-uat` e `...-prd`) e usar users IAM separados.
- Para PRD, use CloudFront com Origin Access Identity e desabilite acesso público direto ao bucket.

---

Se quiser, eu gero os comandos exatos personalizados (substituindo `BUCKET_NAME`, `REGION`, `USERNAME`) para você copiar e executar no terminal — diga os nomes que prefere. Lembre-se: eu não posso criar recursos sem suas credenciais.
