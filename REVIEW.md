# Project review — alterações aplicadas

Resumo das mudanças feitas para melhorar Docker, Gunicorn, observabilidade, performance, userdata e segurança de rede.

Principais alterações

- `app/app.py`
  - Adicionado `logging` básico, endpoint `/health`, e tratamento estruturado de erros.

- `app/Dockerfile`
  - Criação de usuário não-root `appuser`.
  - Instalação de dependências com `pip --no-cache-dir` e melhor uso de camadas de build.
  - Copia do projeto com `--chown` e exposição da porta `5000`.
  - Usa `entrypoint.sh` para computar dinamicamente `gunicorn` workers.

- `app/entrypoint.sh`
  - Script de entrypoint que calcula `GUNICORN_WORKERS` por CPU se variável não configurada.
  - Executa `gunicorn` com logs para stdout/stderr.

- `app/requirements.txt`
  - Versões fixadas: `Flask==2.2.5`, `gunicorn==20.1.0`.

- `app/.dockerignore`
  - Ignora artefatos e arquivos sensíveis para reduzir contexto de build.

- `docker-compose.yml`
  - Versão `3.8`, publica porta `5000`, adiciona `healthcheck` para `/health`, e expõe variáveis de tuning.

- `terraform/modules/security-group/main.tf`
  - Restrição de ingress HTTP para `var.allowed_ip` (melhora segurança de rede). Verifique `dev.tfvars` para fornecer IP real.

- `terraform/userdata.sh`
  - Tornado idempotente, melhor gestão de pacotes e instalação do CloudWatch agent com limpeza.

- `.gitignore`
  - Adicionados padrões para evitar commit de `terraform.tfstate`, venv, e outros artefatos.

Recomendações adicionais (não aplicadas automaticamente)

- Atualizar `README.md` com instruções de execução e notas de segurança.
- Adicionar CI (GitHub Actions) para: lint, testes, `terraform fmt/validate/plan`.
- Revisar se a restrição de HTTP para `allowed_ip` é desejada; se a aplicação precisa ser pública, ajuste a regra.
- Considerar adotar multi-stage builds ou imagens mais leves (distroless) para produção.

Como testar localmente

1. Buildar imagem e subir serviços:

```bash
docker compose build
docker compose up
```

2. Verificar saúde do app:

```bash
curl http://localhost:5000/health
```
