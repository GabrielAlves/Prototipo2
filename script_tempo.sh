#!/bin/bash

set -e

sudo docker compose down -v --rmi all
sudo docker system prune -f

echo "começando a medir o tempo..."
START=$(date +%s)

sudo docker compose up -d --build

echo "Aguardando aplicação ficar disponível..."

TIMEOUT=1000
ELAPSED=0

# checa se o frontend está disponível. O frontend depende do back e do bd no docker-compose, então fica disponível por último
until curl -sf http://localhost:5002/ > /dev/null
do
    sleep 1
    ELAPSED=$((ELAPSED+1))

    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "status=falha" >> resultado_tempo_deploy.txt
        echo "motivo=timeout" >> resultado_tempo_deploy.txt
        exit 1
    fi
done

END=$(date +%s)
DEPLOY_TIME=$((END-START))

echo "Deploy concluído. Tempo de deploy: $DEPLOY_TIME segundos"

echo "status=sucesso" >> resultado_tempo_deploy.txt
echo "Tempo de deploy: $DEPLOY_TIME segundos" >> resultado_tempo_deploy.txt
echo "---------------" >> resultado_tempo_deploy.txt