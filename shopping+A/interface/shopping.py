from db import db_handler
from interface import bank
from lib import common

shop_logger=common.get_logger('shopping')

def shopping_interface(name,cost,shoppingcart):
    flag,msg=bank.consume_interface(name,cost)
    if flag:
        user_dic=db_handler.select(name)
        user_dic['shoppingcart']=shoppingcart
        db_handler.save(user_dic)
        shop_logger.info('%s购买商品成功'%name)
        return True,'购买成功'
    else:
        return False,msg


def check_shoppingcart_interface(name):
    user_dic=db_handler.select(name)
    return user_dic['shoppingcart']