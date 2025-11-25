Hotel Booking Service

Сервис для управления номерами отелей и бронированиями.

## Требования

- Docker >= 20.10
- Docker Compose >= 2.0
- Git

## Быстрый старт

### 1. Клонирование репозитория
git clone https://github.com/Nisyas/hotel-booking-service.git
cd hotel-booking-service


### 2. Настройка конфигурации

В корне проекта переименуйте файл `config.yaml.example` в `config.yaml`:

django:
secret_key: "your-secret-key-here" <-Замените ключ на свой секретный ключ
debug: true <- Для продакшена debug: false
allowed_hosts:
- "localhost"
- "127.0.0.1"

database:
name: "hotel_booking_db"
user: "postgres"
password: "postgres123"
host: "db"
port: 5432

### 3. Запуск проекта

Запустите все сервисы (PostgreSQL + Django):
Находясь в терминале в корне проекта ..\hotel-booking-service, 
запустите команду 
docker-compose up --build

При первом запуске:
- Автоматически создастся база данных PostgreSQL
- Применятся все миграции Django
- Сервер будет доступен по адресу: http://localhost:9000

### 4. Применение миграций (если необходимо)

Если миграции не применились автоматически:

docker-compose exec app python manage.py migrate


### 5. Создание суперпользователя (опционально)

Для доступа к Django Admin:
docker-compose exec app python manage.py createsuperuser


После создания админка будет доступна по адресу: http://localhost:9000/admin

## Остановка проекта

docker-compose down

Для удаления всех данных (включая базу данных):
docker-compose down -v


## Структура проекта

hotel-booking-service/
├── bookings/ # Приложение для управления бронированиями
├── rooms/ # Приложение для управления номерами
├── hotel_booking/ # Основные настройки Django проекта
├── docker-compose.yml # Конфигурация Docker Compose
├── Dockerfile # Образ приложения
├── pyproject.toml # Зависимости Poetry
└── config.yaml # Конфигурация приложения


## API Endpoints

### Номера отеля

- `POST /rooms/create/` - Создание номера
- `GET /rooms/list/` - Список всех номеров (с сортировкой)
- `DELETE /rooms/delete/<room_id>/` - Удаление номера

### Бронирования

- `POST /bookings/create/` - Создание бронирования
- `GET /bookings/list/?room_id=<id>` - Список бронирований для номера
- `DELETE /bookings/delete/<booking_id>/` - Удаление бронирования

## Примеры запросов

### Создание номера

curl -X POST http://localhost:9000/rooms/create/
-H "Content-Type: application/json"
-d '{
"name": "Двуместный люкс",
"description": "Комфортный номер с видом на море",
"price": 5000.00
}


### Создание бронирования

curl -X POST http://localhost:9000/bookings/create/ 
  -H "Content-Type: application/json" 
  -d '{"room_id": 1, 
  "date_start": 
  "2025-12-10", 
  "date_end": 
  "2025-12-15"}'


### Получение списка номеров

curl http://localhost:9000/rooms/list/?sort_by=price&order=asc

### Получить список бронирований для комнаты
curl http://localhost:9000/bookings/list?room_id=1

### Удалить бронирование
curl -X DELETE http://localhost:9000/bookings/delete/1


## Запуск тестов

docker-compose exec app pytest

Для запуска с покрытием:
docker-compose exec app pytest --cov=. --cov-report=html


## Разработка

### Установка pre-commit хуков

docker-compose exec app pre-commit install

### Проверка кода

docker-compose exec app ruff check .