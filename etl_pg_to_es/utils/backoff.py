import time
from functools import wraps

from logger import get_logger

RETRIES_EXCEPTION = (
    'Повторный запуск. Функция: {function}, ',
    'завершила рабобу с ошибкой: {exceprion}',
)
FINALLY_EXCEPTION = (
    'Превышено максимальное время ожидания выполнения функции: {function},',
    'приложение завершило работу с ошибкой {exceprion}',
)


def backoff(
    start_sleep_time=0.1, factor=2, border_sleep_time=10, logger=get_logger,
):
    def func_wrapper(func):
        logging = logger(func.__name__)

        @wraps(func)
        def inner(*args, **kwargs):
            retries = 0
            while True:
                sleep_time = start_sleep_time * factor ** retries
                try:
                    return func(*args, **kwargs)
                except Exception as exception:
                    if sleep_time > border_sleep_time:
                        error_message = FINALLY_EXCEPTION.format(
                            function=func.__name__,
                            exception=exception,
                        )
                        logging.error(error_message)
                        raise TimeoutError(error_message)
                    logging.info(RETRIES_EXCEPTION.format(
                        function=func.__name__,
                        exception=exception,
                    ))
                    time.sleep(sleep_time)
                    retries += 1
        return inner
    return func_wrapper
