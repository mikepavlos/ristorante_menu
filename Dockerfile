FROM python:3.11.2-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip &&  \
    pip install -r requirements.txt --no-cache-dir

COPY . .

#CMD ["uvicorn", "menu_app.main:app", "--host", "0.0.0.0", "--reload"]