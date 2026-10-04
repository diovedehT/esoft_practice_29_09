# Практика Docker: безопасный запуск приложения (кейс «стажёр в DevOps»)

Nginx и простой Python-сервер запускаются в контейнерах с соблюдением базовых практик безопасности.

## Что делает каждый файл

| Файл | Назначение |
|---|---|
| index.html | Кастомная страница, которую отдаёт Nginx (задание 1.2) |
| Dockerfile | Образ my-nginx-practice:v1 на основе nginx:alpine с нашей страницей (1.2) |
| security_scan.txt | Отчёт сканирования образа nginx:alpine сканером Trivy: найдено и способы устранения (2.1) |
| scan_high_crit.txt | Сырой вывод Trivy (HIGH и CRITICAL) (2.1) |
| app.py | Python HTTP-сервер, показывает полученный APP_API_TOKEN в маскированном виде (2.2) |
| run_secret_app.sh | Запускает контейнер python:alpine, ключ принимает аргументом и передаёт через переменную окружения (2.2) |
| docker-compose.yml | Стек web (Nginx) + db (PostgreSQL 15), БД без проброса порта, том для данных (2.3) |
| .env.example | Шаблон файла с паролем БД. Настоящий .env создаётся из него и в Git не попадает (2.3) |
| .gitignore | Исключает .env, логи и nginx_logs/ из репозитория |
| Dockerfile.nonroot | Nginx от непривилегированного пользователя appuser (2.4) |
| README.md | Этот файл |

## Как запустить и проверить

### Подготовка (1.2): сборка образа
    docker build -t my-nginx-practice:v1 .
    docker run -d --name web -p 8080:80 my-nginx-practice:v1
    curl localhost:8080
    docker rm -f web

### 2.1: сканирование образа
    trivy image --severity HIGH,CRITICAL nginx:alpine
    cat security_scan.txt

### 2.2: секрет через переменную окружения
    ./run_secret_app.sh my-super-secret-key
    docker exec secret-app printenv APP_API_TOKEN
    curl localhost:8081

### 2.3: стек Docker Compose
    cp .env.example .env
    nano .env                              # задать свой пароль БД
    docker compose up -d
    docker compose ps                      # у db нет проброшенного порта
    docker volume ls                       # том docker-practice_db_data
    docker compose exec web ping -c 3 db   # web видит БД по имени
    docker compose port db 5432            # пусто: наружу не опубликован
    curl localhost:8080
    docker compose down                    # остановка (данные БД сохраняются)

### 2.4: запуск не от root
    docker build -f Dockerfile.nonroot -t my-nginx-practice:nonroot .
    docker run -d --name web-nonroot -p 8082:8080 my-nginx-practice:nonroot
    curl localhost:8082
    docker exec web-nonroot ps aux         # процессы nginx от appuser
    docker exec web-nonroot id             # uid=100(appuser)

## Очистка
    docker rm -f secret-app web-nonroot
    docker compose down

## Безопасность (кратко)
- Секреты не хранятся в коде и Dockerfile: ключ передаётся аргументом скрипта, пароль БД лежит в .env вне Git.
- БД доступна только из сети compose, порт на хост не проброшен.
- Данные БД хранятся в именованном томе.
- Образ проверен Trivy: 0 CRITICAL, 2 HIGH (с доступными исправлениями).
- Nginx в Dockerfile.nonroot работает от appuser, а не от root.
