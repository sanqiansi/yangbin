from core import src
from conf import settings
import logging.config
def auth(func):
    def inner(*args,**kwargs):
        if src.user_info['name']:
            res=func(*args,**kwargs)
            return res
        else:
            src.login()
    return inner


def get_logger(name):
    logging.config.dictConfig(settings.LOGGING_DIC)
    my_logger=logging.getLogger(name)
    return my_logger