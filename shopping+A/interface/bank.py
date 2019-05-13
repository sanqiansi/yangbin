from db import db_handler
from lib import common

bank_logger=common.get_logger('bank')
def check_balance_interface(name):
    user_dic = db_handler.select(name)
    return user_dic['balance']


def withdraw_interface(name, balance):
    user_dic = db_handler.select(name)
    if user_dic['balance'] >= balance * 1.05:
        user_dic['balance'] -= balance * 1.05
        user_dic['bankflow'].append('%s 取款 %s'%(name,balance))
        db_handler.save(user_dic)
        bank_logger.info('%s 取款 %s'%(name,balance))
        return True, '取款成功'
    else:
        return False, '余额不足'


def repay_interface(name, balance):
    user_dic = db_handler.select(name)
    user_dic['balance'] += balance
    user_dic['bankflow'].append('%s 还款 %s' % (name, balance))
    db_handler.save(user_dic)
    bank_logger.info('%s 还款 %s' % (name, balance))
    return True, '还款成功，当前额度为%s' % user_dic['balance']


def transfer_interface(from_user, to_user, balance):
    to_user_dic = db_handler.select(to_user)
    if to_user_dic:
        from_user_dic = db_handler.select(from_user)
        if from_user_dic['balance'] >= balance:
            from_user_dic['balance'] -= balance
            to_user_dic['balance'] += balance

            from_user_dic['bankflow'].append('您给 %s 转账 %s' % (to_user, balance))
            to_user_dic['bankflow'].append(' %s 给您转账 %s' % (from_user, balance))

            db_handler.save(to_user_dic)
            db_handler.save(from_user_dic)
            bank_logger.info(' %s 给 %s 转账 %s' % (from_user,to_user, balance))
            return True, '转账成功'
        else:
            return False, '余额不足'
    else:
        return False, '对方账户不存在'


def check_records_interface(name):
    user_dic = db_handler.select(name)
    return user_dic['bankflow']


#消费接口
def consume_interface(name,account):
    user_dic=db_handler.select(name)
    if user_dic['balance']>=account:
        user_dic['balance']-=account

        user_dic['bankflow'].append('您消费%s'%account)
        db_handler.save(user_dic)
        bank_logger.info('您消费%s'%account)
        return True,'付款成功'
    else:
        return False,'余额不足'
