import time

class SimpleCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self.store = {}

    def get(self, key: str):
        entry = self.store.get(key)
        if entry:
            value, expires_at = entry
            if time.time() < expires_at:
                return value
            else:
                del self.store[key]
        return None

    def set(self, key: str, value):
        expires_at = time.time() + self.ttl
        self.store[key] = (value, expires_at)

# Instância global do cache para ser usada em qualquer lugar
cache = SimpleCache(ttl_seconds=300)  # 5 minutos
