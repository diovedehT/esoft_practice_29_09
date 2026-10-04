# Docker-практика: стек web + db

## Запуск
1. Скопировать пример переменных окружения и задать свой пароль БД:
   cp .env.example .env
   nano .env
2. Убедиться, что образ web собран:
   docker build -t my-nginx-practice:v1 .
3. Запустить стек:
   docker compose up -d
   (в старой версии: docker-compose up -d)
4. Проверить:
   docker compose ps
   curl localhost:8080

## Остановка
   docker compose down        # данные БД сохраняются в томе db_data
   docker compose down -v     # вместе с томом (данные БД удалятся)

## Безопасность
- Порт БД не проброшен на хост, она доступна только сервису web.
- Пароль БД хранится в .env, а не в docker-compose.yml.
- .env добавлен в .gitignore и в репозиторий не попадает.
- Данные БД лежат в именованном томе db_data.
