import json
from enum import Enum
from time import sleep
from typing import Callable

import requests.packages
import requests.packages.urllib3
from requests import Session as RSession
from robot.utils import timestr_to_secs
from urllib3.exceptions import InsecureRequestWarning

from robotframework_practitest.utils.logger import LOGGER as logger
from robotframework_practitest.utils.data_service import CacheItem, CacheLibraryService, DEFAULT_ITEM_WAIT
from robotframework_practitest.utils.misc_utils import get_error_info

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class SupportedMethods(Enum):
    PUT = 'put'
    POST = 'post'
    GET = 'get'


class SessionWithCaching:
    def __init__(self, user, token, **kwargs):
        super().__init__()
        self._session = RSession()
        self._user = user
        self._token = token
        self._throttle_activated = None
        self._throttle_timeout = 0

    @property
    def active_timeout(self):
        return self._throttle_timeout if self._throttle_activated else 0

    @property
    def auth(self):
        return tuple(getattr(self, f) for f in ('_user', '_token'))

    @property
    def headers(self):
        return {'Content-type': 'application/json'}

    def _get_method(self, request_method) -> Callable:
        if request_method == SupportedMethods.PUT:
            return self._session.put
        elif request_method == SupportedMethods.POST:
            return self._session.post
        elif request_method == SupportedMethods.GET:
            return self._session.get
        else:
            raise AttributeError(f"Unsupported method: {request_method}")

    def wait_throttle_timeout(self, timeout=60):
        timeout_in_seconds = timestr_to_secs(timeout)
        self._throttle_activated = True
        self._throttle_timeout = timeout
        logger.warn(f"Retention {timeout} started")
        sleep(timeout_in_seconds)
        logger.warn("Retention ended")
        self._throttle_activated = False
        self._throttle_timeout = 0

    def run(self,  method: SupportedMethods, cache_item: CacheItem, url, payload=None,
            ignore_cache=False, enforce_result=False, timeout=DEFAULT_ITEM_WAIT):
        logger.trace(f"job start: {self}, {url}, {payload}")
        try:
            if ignore_cache:
                raise AssertionError()
            res = CacheLibraryService().wait(cache_item, timeout + self.active_timeout)
        except (ValueError, IndexError, KeyError):
            logger.trace(f"Cannot retrieve from cache {cache_item}; Access API")
        except AssertionError:
            logger.trace(f"Cache ignored enforce access API")
        else:
            logger.trace(f"Retrieving from cache {cache_item}: {res}")
            return res
        try:
            if payload is None:
                payload = dict()
            elif isinstance(payload, Callable):
                payload: dict = payload()

            res = self.request_call(method, url, payload)
            CacheLibraryService()[cache_item] = res
            if enforce_result:
                return CacheLibraryService().wait(cache_item, timeout)

            return cache_item.Key
        except AssertionError:
            raise
        except Exception as e:
            f, li = get_error_info()
            logger.error(f"Error API call: {e}; File: {f}:{li}")
            raise

    def request_call(self, method: SupportedMethods, url, payload=None):
        if payload is None:
            payload = {}
        request_method = self._get_method(method)
        while self._throttle_activated:
            sleep(0.5)
        while True:
            response = request_method(url, auth=self.auth, headers=self.headers, data=json.dumps(payload))
            res = json.loads(response.content)
            if response.status_code == 429:
                timeout = res['errors'][0]['Retry-After']
                self.wait_throttle_timeout(timeout)
                logger.warn(f"{response.status_code} got on {method.name} {url}")
            else:
                break
        assert response.status_code == 200, \
            f"Error {self} {url}:\n{response.content.decode('utf-8')}"
        return res






