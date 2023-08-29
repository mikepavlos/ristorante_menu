import json

from fastapi.encoders import jsonable_encoder
from redis import Redis

from menu_app.settings import settings

r = Redis(host=settings.REDIS, port=6379, decode_responses=True)


def set_cache(key, value):
    r.set(key, json.dumps(jsonable_encoder(value)))


def get_cache(key):
    value = r.get(key)
    return json.loads(value) if value else None


def clear_cache(key):
    keys = r.keys(f'{key}*')
    if keys:
        r.delete(*keys)
