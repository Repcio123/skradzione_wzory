

from typing import Optional
from weakref import WeakValueDictionary
import hashlib

class CachedRecord:
    hash_cache = WeakValueDictionary()
    hash_function = hashlib.md5

    def __init__(self, text: str):
        self.text = text
        CachedRecord.hash_cache[CachedRecord.encode(text)] = self
    
    @staticmethod
    def encode(text: str) -> str:
        return CachedRecord.hash_function(text.encode("utf-8")).hexdigest()

    @staticmethod
    def get(text) -> Optional[object]:
        return CachedRecord.hash_cache.get(CachedRecord.encode(text))