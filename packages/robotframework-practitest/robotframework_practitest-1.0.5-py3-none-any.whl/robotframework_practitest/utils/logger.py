from threading import currentThread

from robot.api import logger
from robotbackgroundlogger import BackgroundLogger, BackgroundMessage

LOGGER = BackgroundLogger()


def write(self, msg, level, html=False):
    with self.lock:
        thread = currentThread().getName()
        if any([t.startswith(thread) for t in self.LOGGING_THREADS]):
            logger.write(msg, level, html)
        else:
            message = BackgroundMessage(msg, level, html)
            self._messages.setdefault(thread, []).append(message)


# setattr(LOGGER, 'write', write)


def log_background_messages(self, name=None):
    """Forwards messages logged on background to Robot Framework log.

    By default forwards all messages logged by all threads, but can be
    limited to a certain thread by passing thread's name as an argument.
    Logged messages are removed from the message storage.

    This method must be called from the main thread.
    """
    thread = currentThread().getName()
    if any([t.startswith(thread) for t in self.LOGGING_THREADS]):
        raise RuntimeError(
            "Logging background messages is only allowed from the main "
            "thread. Current thread name: %s" % thread)
    with self.lock:
        if name:
            self._log_messages_by_thread(name)
        else:
            self._log_all_messages()


# setattr(LOGGER, 'write', log_background_messages)


def register_thread_to_logger(name):
    LOGGER.LOGGING_THREADS = tuple(list(LOGGER.LOGGING_THREADS) + [name])



