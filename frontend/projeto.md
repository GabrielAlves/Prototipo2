# Projeto Frontend

## Arquivo requirements.txt

O arquivo requirements.txt da pasta frontend lista as dependências necessárias para o frontend do projeto:

- **flask**: Framework web leve para construir aplicações web em Python.
- **python-dotenv**: Permite carregar variáveis de ambiente a partir de arquivos `.env`, facilitando a configuração do ambiente.

Esses pacotes são suficientes para criar e configurar uma aplicação web simples com Flask.

## Arquivo app.py

O arquivo app.py é o ponto de entrada do frontend Flask. Veja o que ele faz:

- **Carrega variáveis de ambiente** usando `python-dotenv`.
- **Cria uma instância Flask** para a aplicação web.
- **Obtém a URL da API do backend** da variável de ambiente `BACKEND_API_BASE` (com valor padrão `http://localhost:8000`).
- **Define a rota `/`**:
  - Renderiza o template `index.html`, passando a variável `api_base` para uso no template.
- **Executa o servidor Flask** na porta 5001 e no modo debug quando o arquivo é executado diretamente.
 
Esse arquivo inicializa o frontend, configura a comunicação com o backend e serve a página principal usando Flask.

## Arquivo static/app.js

O arquivo app.js implementa a lógica do frontend para um gerenciador de arquivos. Aqui está um resumo das principais partes:

### 1. **Helpers**
- `formatBytes(bytes)`: Converte bytes em KB, MB, etc., para exibir tamanhos legíveis.
- `formatSeconds(s)`: Formata segundos em minutos:segundos.

### 2. **Upload de Arquivos**
- Elementos DOM são selecionados para upload (dropzone, input, barra de progresso).
- O usuário pode arrastar arquivos ou selecionar via input.
- `uploadFiles(files)`: Envia arquivos via AJAX (`XMLHttpRequest`) para o backend. Mostra barra de progresso e trata erros de rede.
- Após upload, atualiza a galeria de arquivos.

### 3. **Galeria de Arquivos**
- `fetchFiles()`: Busca lista de arquivos do backend via `fetch`.
- `renderGallery(files)`: Filtra e exibe os arquivos conforme o filtro selecionado (imagem, áudio, vídeo, documento, todos).
- `renderCard(f)`: Monta o HTML de cada arquivo, mostrando prévia, metadados e ações (baixar/abrir).
- `renderPreview(f)`: Mostra prévia do arquivo (imagem, áudio, vídeo, PDF).

### 4. **Filtros**
- Botões de filtro permitem mostrar apenas arquivos de uma categoria.
- O filtro selecionado é destacado e usado para filtrar a galeria.

### 5. **URLs de Arquivos**
- `fileUrl(u)`: Gera URL absoluta para acessar arquivos no backend, considerando ambiente de desenvolvimento ou produção.

### 6. **Inicialização**
- Ao carregar, chama `fetchFiles()` para mostrar os arquivos existentes.

O código permite ao usuário enviar arquivos, visualizar e filtrar arquivos enviados, e baixar ou abrir cada arquivo. Tudo é feito dinamicamente, sem recarregar a página.
