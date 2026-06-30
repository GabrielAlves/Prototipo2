# Prototipo2

Este protótipo é parte de um TCC e implementa uma aplicação web de gerenciamento de arquivos multimídia (imagens, áudios e vídeos) utilizando conteinerização para separar os componentes da aplicação em serviços independentes. É a versão conteinerizada do [Prototipo1](https://github.com/GabrielAlves/Prototipo1/). O diretório  [arquivos_exemplo](https://github.com/GabrielAlves/Prototipos/tree/main/arquivos_exemplo) contém exemplos de arquivos (<10 MB) de diversos formatos que são aceitos na aplicação (mp3, mp4, mkv, aac, png, jpeg, gif). 

O objetivo deste protótipo é automatizar o deploy e reduzir dependências do ambiente local.

Para permitir a execução simultânea dos diferentes protótipos durante os experimentos, foram definidos mapeamentos distintos de portas entre o host e os serviços da aplicação. Os serviços internos mantem a mesma configuração do Prototipo1 (backend escutando na porta 8000, frontend na porta 5001, banco de dados na porta 3306) para demonstrar que não há modificação do código base entre os protótipos, mas cada protótipo expõe seus serviços em portas diferentes pra evitar conflito de alocação de portas e permitir que eles possam ser acessados ao mesmo tempo (em abas diferentes, por exemplo). Por isso, o Prototipo2 expoe (Backend 8001, Frontend 5001, Banco de dados 3307).


![Interface de usuário da aplicação](https://raw.githubusercontent.com/GabrielAlves/Prototipos/refs/heads/main/screenshots/interface_usuario_prototipo2.png)
Figura 1. Interface de usuário da aplicação

## Funcionalidades
- Inserção de arquivos multimídia (imagem, áudio e vídeo) de até 10 MB
- Listagem dos arquivos armazenados
- Visualização e reprodução dos arquivos enviados
- Remoção de arquivos
- Persistência de metadados em banco relacional e arquivos de upload
- Testes unitários com Pytest

## Tecnologias utilizadas
- HTML, CSS e JavaScript
- Python 3.11
- Flask 3.1
- MySQL 8.0
- Pytest 9.0
- Docker 29.5 e Docker Compose 5.1
- Bash 5.2

## Como configurar automaticamente

Os 2 scripts abaixo foram criados para auxiliar os avaliadores.

O `script_pacotes.sh` deve ser executado na primeira vez para instalar com o apt-get os pacotes que são utilizados pelo `script_deploy.sh`. Esses pacotes são docker-ce, docker-ce-cli, containerd.io, docker-buildx-plugin, docker-compose-plugin (e pacotes auxiliares à instalação do docker).

1. Execute `sudo bash script_pacotes.sh`

O `script_deploy.sh` executa automaticamente os passos de configuração descritos logo abaixo e também executa os testes unitários no final da execução.

1. Execute `sudo bash script_deploy.sh`

![Saída esperada para o arquivo de deploy](https://raw.githubusercontent.com/GabrielAlves/Prototipos/refs/heads/main/screenshots/script_deploy_executado_prototipo2.png)
Figura 2. Resultado do `script_deploy.sh`

## Como executar o projeto

Na raiz do projeto (Prototipo2/) onde está o arquivo docker-compose.yml:

1. Execute: `docker compose up --build`
2. Espere os contêineres ficarem `Started` (Backend e Frontend) e `Healhty` (Banco de dados)
3. Acesse `http://127.0.0.1:5002` para a interface de usuário no navegador.
4. Acesse `http://127.0.0.1:8001` para o status do backend.

## Como executar os testes unitários diretamente

1. Execute `sudo docker compose exec -T backend python -m pytest --disable-warnings`

## Como executar os testes de tempo de deploy

1. Execute `sudo bash script_tempo.sh`

ou

1. Execute `sudo bash executar_varios_script_tempo.sh` (default: 10 execuções. O número pode ser modificado no for do script `executar_varios_script_tempo.sh`)

## Resultados de tempo de deploy

Os resultados se encontram em `resultado_tempo_deploy.txt`. O arquivo usado para calcular as médias e desvio padrões pode ser acessado [aqui](github.com/GabrielAlves/Prototipos/blob/main/desvio_padrao.py).
