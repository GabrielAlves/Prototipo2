#!/bin/bash

set -e

SENHA='123'

echo $SENHA | sudo -S docker compose down -v --rmi all
echo $SENHA | sudo -S docker system prune -f

START=$(date +%s)

echo $SENHA | sudo -S docker compose up -d --build

echo "Aguardando aplicação ficar disponível..."

TIMEOUT=1000
ELAPSED=0

until curl -sf http://localhost:8001/health > /dev/null
do
    sleep 1
    ELAPSED=$((ELAPSED+1))

    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "status=falha" >> resultado_deploy.txt
        echo "motivo=timeout" >> resultado_deploy.txt
        exit 1
    fi
done

END=$(date +%s)
DEPLOY_TIME=$((END-START))

cat >> resultado_deploy.txt << EOF
status=sucesso
tempo_deploy=$DEPLOY_TIME
timestamp=$(date)
--------
EOF

echo "Deploy concluído"
echo "Tempo de deploy: $DEPLOY_TIME segundos"