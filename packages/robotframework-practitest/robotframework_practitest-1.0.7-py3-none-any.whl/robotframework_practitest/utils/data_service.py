import json
import logging
import time
from threading import RLock
from time import sleep
from typing import Mapping, Any, Iterator, Callable

from robotframework_practitest.utils.misc_utils import get_error_info
from robotframework_practitest.utils.singleton import Singleton

logger = logging.getLogger(__name__)

DEFAULT_ITEM_WAIT = 0.2


class CacheItem:
    def __init__(self, area, key, formatter: Callable = None):
        self.Area = area
        self.Key = key
        self.Formatter = formatter

    def __eq__(self, other):
        try:
            assert isinstance(other, CacheItem)
            assert self.Area == other.Area
            assert self.Key == self.Key
        except AssertionError:
            return False
        else:
            return True

    def __hash__(self):
        return hash(json.dumps(self.__dict__))

    def __str__(self):
        return f"{self.Area}::{self.Key}"


@Singleton
class CacheLibraryService(Mapping[CacheItem, Any]):
    def __init__(self):
        self.__lock = RLock()
        self._cache = dict()

    @property
    def cache(self):
        return self._cache

    def __len__(self) -> int:
        return len(self.cache)

    def __iter__(self) -> Iterator[Any]:
        return self.cache.__iter__()

    def __setitem__(self, item: CacheItem, argument):
        with self.__lock:
            try:
                self.cache.setdefault(item.Area, dict())
                value = item.Formatter(argument) if item.Formatter else argument
                self.cache[item.Area][item.Key] = value
                logger.debug(f"Update in cache: {item} -> {value}")
            except Exception as e:
                f, li = get_error_info()
                logger.error(f"Cannot add key '{item}:{argument}': {e}; File: {f}:{li}")

    def __getitem__(self, item):
        with self.__lock:
            if isinstance(item, str):
                value = self.cache[item]
            else:
                value = self.cache[item.Area][item.Key]
            logger.debug(f"Retrieve from cache: {item} -> {value}")
            return value

    def __delitem__(self, key):
        del self._cache[key]

    def keys(self):
        return self._cache.keys()

    def wait(self, item, timeout=None):
        timeout = timeout or DEFAULT_ITEM_WAIT
        start_ts = time.perf_counter()
        while (time.perf_counter() - start_ts) < timeout:
            try:
                return self[item]
            except KeyError:
                sleep(DEFAULT_ITEM_WAIT)
            finally:
                logger.debug(f"Result got in {time.perf_counter() - start_ts}s.")
        raise KeyError(f"Key '{item}' not found")


DEFAULT_CACHE_TIMEOUT = 65


__all__ = [
    'CacheLibraryService',
    'CacheItem',
    'DEFAULT_ITEM_WAIT'
]
