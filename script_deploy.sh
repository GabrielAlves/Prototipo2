#!/bin/bash

set -e

docker compose up -d --build

# checa se o frontend está disponível. O frontend depende do back e do bd no docker-compose, então fica disponível por último
until curl -sf http://localhost:5002/ > /dev/null
do
    sleep 1
done

echo "Executando testes..."

docker compose exec -T backend python -m pytest --disable-warnings

echo "Tela da aplicação: http://127.0.0.1:5002"
echo "Status do backend: http://127.0.0.1:8001/health"