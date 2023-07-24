# Ristorante_menu
### Упрощенный сервис меню ресторана

### Стек
- python 3.11.2
- FastAPI 0.95.0
- SQLAlchemy 1.4.41
- PostgreSQL 15.1
- Docker

### Запуск проекта в контейнере Docker

Клонировать проект

```commandline
git clone https://github.com/mikepavlos/ristorante_menu.git
```

Создать `.env` файл, либо изменить образец `.env.example` файла в директории проекта, улалив `.example`.  

Запустить контейнеры командой

```commandline
 docker compose up -d --build
```

Документация к API `app/v1/docs#`

----

### Автор
Михаил Павлов  
https://github.com/mikepavlos