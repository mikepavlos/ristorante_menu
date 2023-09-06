from redis import Redis

from menu_app.settings import settings

cache = Redis(host=settings.REDIS, port=6379, decode_responses=True)
