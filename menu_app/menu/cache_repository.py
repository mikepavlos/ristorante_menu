import json

from fastapi.encoders import jsonable_encoder

from menu_app.cache import cache


class CacheResponse:
    @staticmethod
    def search(arg):
        return cache.keys(f'*{arg}*')

    def set(self, key, value):
        cache.set(key, json.dumps(jsonable_encoder(value)))

    def get(self, arg):
        if key := self.search(arg):
            return json.loads(cache.get(*key))

    def clear(self, *args):
        for arg in args:
            if keys := self.search(arg):
                cache.delete(*keys)
