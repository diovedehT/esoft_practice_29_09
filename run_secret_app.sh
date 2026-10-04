#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Использование: $0 <API_TOKEN>"
  exit 1
fi

DIR="$(dirname "$(realpath "$0")")"

docker rm -f secret-app >/dev/null 2>&1 || true

docker run -d --name secret-app \
  -p 8081:8000 \
  -e APP_API_TOKEN="$1" \
  -v "$DIR/app.py:/app/app.py:ro" \
  python:alpine \
  python /app/app.py

echo "Контейнер secret-app запущен на порту 8081"
