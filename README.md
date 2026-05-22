# MediaManagerAPI

É uma API REST simples desenvolvida em Python para gerenciamento de arquivos multimídia (imagens e vídeos), com upload, listagem e exclusão com suporte à integração com AWS S3 ou armazenamento local.

## Funcionalidades

- Upload de arquivos (até 10MB): (POST /upload)
- Listagem de arquivos com metadados (GET /list)
- Exclusão de arquivos (DELETE /delete/{id})
- Autenticação via API Key
- Integração com AWS S3
- Modo alternativo de armazenamento local
- Testes unitários

## Tecnologias utilizadas

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- SQLite
- AWS S3 (via boto3)
- Pytest

## Como usar (Instruções para windows)

1. Clone o repositório: `git clone https://github.com/GabrielAlves/MediaManagerAPI`
2. Entre no diretório: `cd MediaManagerAPI`
3. Crie um ambiente virtual: `virtualenv venv`
4. Ative o ambiente virtual: `venv\Scripts\activate` 
5. Instale as dependências: `pip install -r requirements.txt`
6. Copie o arquivo env de exemplo para o diretório app: `copy .env.example "app/.env"`
7. Edite as variáveis do arquivo .env
9. Execute a aplicação: `python run.py`
10. Acesse a API em `http://localhost:5000`

## Como configurar o S3 (caso desejado)

1. Crie um bucket no Amazon s3
2. Crie um usuário IAM com permissão ao S3
3. Insira as credenciais da AWS no .env
4. Altere `STORAGE_MODE=local` para `STORAGE_MODE=s3`

## Como executar os testes unitários

Execute: `python -m pytest`