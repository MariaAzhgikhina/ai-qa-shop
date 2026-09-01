# AI QA Shop

AI QA Shop — небольшой учебный интернет-магазин на FastAPI с серверным HTML-интерфейсом, REST API и постоянными данными в SQLite.

## Возможности

- каталог из 9 детерминированных товаров;
- страницы с подробной информацией о товарах;
- фильтрация по категории и сортировка по цене;
- корзина с изменением количества, удалением позиций и расчётом суммы;
- проверка количества относительно остатка товара;
- checkout с проверкой имени, email и адреса;
- создание и просмотр заказов, автоматическое уменьшение остатков;
- интерактивная документация REST API;
- baseline-набор API- и браузерных тестов.

## Структура

```text
ai-qa-shop/
├── app/
│   ├── api/             # REST endpoints
│   ├── models/          # схемы входных данных
│   ├── services/        # операции магазина
│   ├── static/          # CSS
│   ├── templates/       # HTML-шаблоны
│   ├── database.py
│   └── main.py
├── requirements/
│   └── product_requirements.md
├── tests/
│   ├── api/
│   └── e2e/
├── Dockerfile
├── Makefile
├── docker-compose.yml
├── pytest.ini
└── requirements.txt
```

## Требования

Для локального запуска нужны:

- Python 3.10 или новее;
- `pip`;
- `make` для запуска сокращённых команд;
- для E2E-тестов — возможность установить браузер Playwright.

Альтернативный вариант запуска требует Docker Desktop или Docker Engine с плагином Docker Compose.

## Локальная установка

Выполните команды из корня репозитория:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

В Windows активация окружения выполняется командой:

```powershell
.venv\Scripts\activate
```

## Локальный запуск

После установки и активации виртуального окружения:

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу <http://127.0.0.1:8000>. При первом запуске каталог `data/` и база `data/shop.db` создаются автоматически.

Остановить сервер можно сочетанием `Ctrl+C`.

## Make-команды

После локальной установки зависимостей доступны сокращённые команды:

| Команда | Назначение |
|---|---|
| `make up` | Собрать и запустить приложение через Docker Compose в фоновом режиме |
| `make down` | Остановить и удалить контейнеры текущего окружения |
| `make api` | Запустить API-тесты из локального `.venv` с подробным статусом каждого теста |
| `make e2e` | Запустить E2E-тесты из локального `.venv` с подробным статусом каждого теста |

Для `make api` и `make e2e` виртуальное окружение активировать не обязательно. Если зависимости установлены в другом окружении, путь к pytest можно переопределить, например: `make api PYTEST=pytest`.

После `make up` в консоли выводятся ссылки на каталог и Swagger UI.

## Запуск через Docker Compose

```bash
make up
```

Откройте <http://localhost:8000>. SQLite-база хранится в Docker volume `shop_data` и сохраняется между перезапусками контейнера.

Эквивалентная команда без Make:

```bash
docker compose up --build -d
```

Для остановки используйте:

```bash
make down
```

Эквивалентная команда: `docker compose down`.

## API-тесты

При активированном виртуальном окружении:

```bash
make api
```

Тесты используют отдельную временную SQLite-базу и не изменяют локальные данные приложения.

Эквивалентная команда: `pytest tests/api`.

## E2E-тесты

Один раз установите браузеры Playwright:

```bash
playwright install
```

Затем запустите тесты:

```bash
make e2e
```

E2E-набор самостоятельно запускает приложение на свободном локальном порту и использует изолированную временную базу.

Эквивалентная команда: `pytest tests/e2e`.

## Основные URL

| Назначение | URL |
|---|---|
| Каталог | <http://127.0.0.1:8000/> |
| Корзина | <http://127.0.0.1:8000/cart> |
| Checkout | <http://127.0.0.1:8000/checkout> |
| Swagger UI | <http://127.0.0.1:8000/docs> |
| OpenAPI JSON | <http://127.0.0.1:8000/openapi.json> |

Основные API endpoints:

```text
GET    /api/products
GET    /api/products/{id}
GET    /api/cart
POST   /api/cart/items
PATCH  /api/cart/items/{id}
DELETE /api/cart/items/{id}
POST   /api/orders
GET    /api/orders/{id}
```
