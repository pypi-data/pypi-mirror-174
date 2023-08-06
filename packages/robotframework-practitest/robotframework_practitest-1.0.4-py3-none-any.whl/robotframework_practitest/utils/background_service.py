import logging
from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread, Event
from time import sleep
from typing import Callable
from concurrent.futures import ThreadPoolExecutor
from robotframework_practitest.utils.misc_utils import get_error_info
from robotframework_practitest.utils.singleton import Singleton
from robotframework_practitest.utils.logger import LOGGER as logger, register_thread_to_logger


class Task:
    def __init__(self, callback: Callable, *args, **kwargs):
        self._callback = callback
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        return self._callback.__name__

    def __call__(self):
        return self._callback(*self._args, **self._kwargs)


class _BackGroundAbstract(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def put(self, task: Task):
        pass

    def join(self):
        pass


@Singleton
class BackgroundSyncService(Thread, _BackGroundAbstract):
    def __init__(self, maxsize=0, thread_interval=0.2):
        _BackGroundAbstract.__init__(self)
        self._event = Event()
        self._active = Event()
        self._queue = Queue(maxsize)
        self._thread_interval = thread_interval
        Thread.__init__(self, target=self._worker, name=self.__class__.__name__, daemon=True)
        register_thread_to_logger(self.__class__.__name__)
        logger.info(f"Starting {self.__class__.__name__}...")
        self.start()

    def _worker(self):
        logger.info(f"{self.__class__.__name__}::_worker started")
        while not self._event.is_set():
            try:
                task_obj = self._queue.get()
                logger.debug(f"{self.__class__.__name__}::Task '{task_obj}' start")
                task_obj()
                logger.debug(f"{self.__class__.__name__}::Task '{task_obj}' done")
            except Exception as e:
                f, li = get_error_info()
                logger.info(f"Error: {e}; File: {f}:{li}")
            finally:
                sleep(self._thread_interval)
        logger.info(f"{self.__class__.__name__}::_worker ended")

    def put(self, item: Task):
        if not self._active.is_set():
            self._queue.put(item)
            logger.debug(f"Task '{item}' added")
        else:
            logger.warn("Service ending awaiting; New task adding not possible now")

    def join(self, timeout=None):
        self._active.set()
        logger.debug(f'Join; Remains {self._queue.qsize()} tasks')
        while not self._queue.empty():
            sleep(0.2)
        logger.debug(f'All tasks completed')
        self._event.set()
        logger.info(f"Stopped {self.__class__.__name__}...")


@Singleton
class BackgroundAsyncService(_BackGroundAbstract):
    def __init__(self):
        self.executor = ThreadPoolExecutor(thread_name_prefix=self.__class__.__name__)
        register_thread_to_logger(self.__class__.__name__)
        self.active = True

    def put(self, task: Task):
        if not self.active:
            logger.warn("Service ending awaiting; New task adding not possible now")
            return
        self.executor.submit(task)

    def join(self):
        self.executor.shutdown(wait=True)


BackgroundSync = BackgroundSyncService()
BackgroundAsync = BackgroundAsyncService()


__all__ = [
    'BackgroundAsync',
    'BackgroundSync',
    'Task'
]
