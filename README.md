# Ristorante_menu
### Cервис меню ресторана

Включает в себя позиции из нескольких меню, которые состоят из подменю, а те в свою очередь - из блюд.  

---

### Стек
- Python 3.11.2
- FastAPI 0.95.0
- SQLAlchemy 1.4.41
- PostgreSQL 15.1
- Docker
- Pytest 7.4.0

---

### Запуск проекта в контейнерах Docker

Клонировать проект

```commandline
git clone https://github.com/mikepavlos/ristorante_menu.git
```

Создать `.env` файл, либо изменить образец `.env.example` в директории проекта, улалив `.example`.  

Запустить контейнеры командой

```commandline
 docker compose up -d --build
```

Документация к API `localhost:8000/` либо `localhost:8000/docs#`

---

### Запуск тестирования эндпоинтов

Тесты эндпоинтов собираются в отдельный контейнер командой

```commandline
docker compose -f docker-compose_test.yml up --build
```

Необходимо дождаться сборки контейнеров.  
При этом контейнер с тестами автоматически собирается, прогоняет тесты и останавливается.  
Результаты тестов выводятся в консоль вместе с логами.

----

### Автор
Михаил Павлов  
https://github.com/mikepavlos