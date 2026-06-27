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

# checa se o frontend está disponível. O frontend depende do back e do bd no docker-compose, então fica disponível por último
until curl -sf http://localhost:5002/ > /dev/null
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

echo "Executando testes no container backend..."
docker compose exec -T backend bash -c "PYTHONPATH=/app python -m pytest"

echo "Deploy concluído"
echo "Tempo de deploy: $DEPLOY_TIME segundos"