# Projeto Backend

## Arquivo requirements.txt

O arquivo requirements.txt lista as dependências Python necessárias para o backend do projeto. Veja o que cada pacote faz:

- **fastapi**: Framework para criar APIs web rápidas e modernas.
- **uvicorn[standard]**: Servidor ASGI recomendado para rodar aplicações FastAPI.
- **sqlalchemy>=2.0**: ORM para manipulação de bancos de dados relacionais.
- **pydantic>=2**: Validação e tipagem de dados, usado pelo FastAPI.
- **pillow**: Biblioteca para manipulação de imagens.
- **mutagen**: Manipulação de metadados de arquivos de áudio.
- **PyPDF2**: Manipulação de arquivos PDF.
- **python-multipart**: Suporte para uploads de arquivos (multipart/form-data).
- **boto3**: SDK da AWS para integração com serviços como S3.
- **python-dotenv**: Carrega variáveis de ambiente a partir de arquivos `.env`.

Esses pacotes permitem ao backend lidar com APIs, banco de dados, arquivos (imagens, áudio, PDF), uploads e integração com AWS.


## Arquivo models.py

O arquivo models.py define o modelo de dados para arquivos enviados, usando SQLAlchemy. Veja os principais pontos:

- **File(Base)**: Classe que representa a tabela `files` no banco de dados.
- **Atributos**:
  - `id`: Identificador único do arquivo (chave primária).
  - `name`: Nome do arquivo.
  - `file_url`: Caminho ou URL do arquivo armazenado.
  - `file_size`: Tamanho do arquivo em bytes.
  - `file_type`: Tipo MIME do arquivo (ex: image/png).
  - `category`: Categoria do arquivo (imagem, documento, áudio, vídeo, outro).
  - `width`, `height`: Dimensões (usado para imagens).
  - `duration`: Duração em segundos (usado para áudio/vídeo).
  - `pages`: Número de páginas (usado para PDFs).
  - `created_at`: Data/hora de criação do registro, preenchida automaticamente.

Esse modelo permite armazenar informações detalhadas sobre arquivos enviados, facilitando consultas e organização no banco de dados.

## Arquivo schemas.py

O arquivo schemas.py define um esquema de dados usando Pydantic para representar arquivos enviados na API.

- **FileRead(BaseModel)**:  
  Classe que representa como os dados de um arquivo serão retornados pela API.
  - **Atributos**:  
    - `id`, `name`, `file_url`, `file_size`, `file_type`, `category`: Informações básicas do arquivo.
    - `width`, `height`: Dimensões (opcional, para imagens).
    - `duration`: Duração (opcional, para áudio/vídeo).
    - `pages`: Número de páginas (opcional, para PDFs).
    - `created_at`: Data/hora de criação do registro.
  - **model_config = {"from_attributes": True}**:  
    Permite criar o modelo Pydantic diretamente a partir de objetos ORM (como os do SQLAlchemy).

Esse esquema serve para garantir que os dados retornados pela API estejam validados e estruturados conforme esperado.

## Arquivo database.py

O arquivo database.py configura a conexão com o banco de dados usando SQLAlchemy. Veja os principais pontos:

- **DATABASE_URL**:  
  Define o caminho do banco de dados SQLite (`files.db`).

- **engine**:  
  Cria o mecanismo de conexão com o banco, permitindo operações SQL.

- **SessionLocal**:  
  Cria sessões para interagir com o banco, sem autocommit e sem autoflush.

- **Base**:  
  Classe base para os modelos ORM (como o modelo `File`).

- **get_db()**:  
  Função geradora que fornece uma sessão de banco de dados para uso em rotas FastAPI. Garante que a sessão seja fechada após o uso.

  
Esse arquivo prepara tudo que é necessário para os modelos e rotas acessarem e manipularem o banco de dados SQLite de forma segura e eficiente.

## Arquivo storage.py

O arquivo storage.py define classes para salvar arquivos enviados, permitindo diferentes tipos de armazenamento:

### 1. **StorageBackend**
- Classe base abstrata.  
- Método `save` deve ser implementado pelas subclasses.

### 2. **LocalStorage**
- Salva arquivos localmente no servidor.
- **Construtor**: Cria o diretório base (`uploads`) se não existir.
- **save**:  
  - Recebe um arquivo e um nome de destino.
  - Salva o arquivo em partes (chunks) no diretório local.
  - Retorna a URL local para acessar o arquivo.

### 3. **S3Storage**
- Salva arquivos em um bucket S3 da AWS.
- **Construtor**:  
  - Recebe dados do bucket, região e credenciais AWS.
  - Cria um cliente S3 usando `boto3`.
- **save**:  
  - Faz upload do arquivo para o S3.
  - Retorna a URL pública do arquivo no S3.
 
O arquivo permite escolher entre armazenamento local ou na nuvem (S3), facilitando a extensão do sistema para diferentes necessidades de infraestrutura.

## Arquivo utils.py

O arquivo utils.py contém funções utilitárias para categorizar arquivos e extrair metadados:

### 1. **categorize(mime: str) -> str**
- Recebe o tipo MIME do arquivo.
- Retorna uma categoria:  
  - `"image"` para imagens  
  - `"audio"` para áudios  
  - `"video"` para vídeos  
  - `"document"` para documentos (PDF, Word, Excel, etc.)  
  - `"other"` para tipos não reconhecidos

---

### 2. **extract_metadata(file_path: str, mime: str) -> Tuple[Optional[int], Optional[int], Optional[float], Optional[int]]**
- Recebe o caminho do arquivo e seu tipo MIME.
- Retorna uma tupla: `(width, height, duration, pages)`
  - Para imagens: retorna largura e altura usando Pillow.
  - Para PDFs: retorna número de páginas usando PyPDF2.
  - Para áudio/vídeo: retorna duração usando Mutagen.
  - Se não conseguir extrair, retorna `None` para os campos.

---

Essas funções ajudam a identificar o tipo do arquivo e a extrair informações relevantes para cada categoria, facilitando o processamento e organização dos arquivos enviados.

## Arquivo main.py

O arquivo main.py implementa a API principal do gerenciador de arquivos usando FastAPI. Veja os principais pontos:

---

### **Configuração Inicial**
- Carrega variáveis de ambiente com `load_dotenv()`.
- Cria as tabelas do banco de dados com `Base.metadata.create_all(bind=engine)`.
- Instancia o app FastAPI e configura CORS (origens permitidas).

---

### **Backend de Armazenamento**
- Seleciona entre armazenamento local (`LocalStorage`) ou S3 (`S3Storage`) conforme variável de ambiente.
- Se for local, monta a rota `/uploads` para servir arquivos estáticos.

---

### **Rotas da API**
- **`/health`**: Retorna status "ok" para verificação de saúde.
- **`/api/files`**: Lista todos os arquivos cadastrados, ordenados por data de criação.
- **`/api/files/{file_id}`**: Retorna os dados de um arquivo específico pelo ID.
- **`/api/upload`**:  
  - Recebe um ou mais arquivos enviados.
  - Gera nome único para cada arquivo.
  - Salva o arquivo no backend escolhido.
  - Extrai metadados (tamanho, dimensões, duração, páginas) se possível.
  - Salva as informações no banco de dados.
  - Retorna a lista atualizada de arquivos.

---
 
Esse arquivo é o núcleo da API, permitindo upload, consulta e detalhamento de arquivos, além de servir os arquivos locais e suportar diferentes backends de armazenamento.

## Observação

  Para o ambiente de testes é possível visualizar os arquivos diretamente pelo navegador: 

  http://127.0.0.1:8000/uploads/78e11ecf7f0d4e25ad616582d574749d.png