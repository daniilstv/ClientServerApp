'''
Декораторы
'''
import sys
import logging
import traceback
import inspect
import logs.config_server_log
import logs.config_client_log


# def cl_srv_detector():
"""
Метод определения модуля, источника запуска.
Метод find () возвращает индекс первого вхождения искомой подстроки,
если он найден в данной строке.
Если его не найдено, - возвращает -1
"""
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    LOGGER = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    LOGGER = logging.getLogger('client')
    # return LOGGER

def log(logging_function):
    '''
    Декоратор - логгер параметров функций
    :param logging_function:
    :return:
    '''
    # cl_srv_detector()
    def logger_func(*args, **kwargs):
        back_func_plus_args = logging_function(*args, **kwargs)
        # call.__doc__ = func.__doc__
        # call.__name__ = func.__name__
        # call.__dict__.update(func.__dict__)
        LOGGER.debug(f'Была вызвана функция {logging_function.__name__} c параметрами \
{args}, {kwargs}.'
                     # f'Документация: {logging_function.__doc__}'        
                     f' Вызов из модуля {logging_function.__module__}. Вызов из'
                     f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f' Вызов из функции {inspect.stack()[1][3]}'
                     )
        return back_func_plus_args
    return logger_func

# def wrap(func):
#     @wraps(func)
#     def call(*args, **kwargs):
#         return func(*args, **kwargs)
# return call
