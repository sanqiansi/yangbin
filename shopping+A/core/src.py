from interface import user, bank, shopping
from lib import common

user_info = {
    'name': None
}


def login():
    print('登录')
    if user_info['name']:
        print('您已经登录过了')
        return
    count=0
    while True:
        name = input('请输入用户名：').strip()
        password = input('请输入密码').strip()
        flag, msg = user.login_interface(name, password)
        if flag:
            print(msg)
            user_info['name'] = name
            break
        else:
            count+=1
            if count>=3:
                user.lock_user(name)
                print('账号被锁定')
                break
            print(msg)


@common.auth
def register():
    print('注册')
    if user_info['name']:
        print('您已经登录过了,不能注册')
        return
    while True:
        name = input('请输入用户名：').strip()
        password = input('请输入密码').strip()
        conf_pwd = input('请确认密码').strip()
        if password == conf_pwd:
            flag, msg = user.register_interface(name, password)
            if flag:
                print(msg)
                break
            else:
                print(msg)


@common.auth
def check_balance():
    print('查看余额')
    balance = bank.check_balance_interface(user_info['name'])
    print('您的余额为%s' % balance)


@common.auth
def transfer():
    print('转账')
    while True:
        to_user = input('请输入要转账的账户：').strip()
        balance = input('请输入转账金额：').strip()
        if balance.isdigit():
            balance = int(balance)
            flag, msg = bank.transfer_interface(user_info['name'], to_user, balance)
            if flag:
                print(msg)
                break
            else:
                print(msg)


@common.auth
def repay():
    print('还款')
    while True:
        balance = input('请输入还款金额：').strip()
        if balance.isdigit():
            balance = int(balance)
            _, msg = bank.repay_interface(user_info['name'], balance)
            print(msg)
            break
        else:
            print('当前输入格式有误')


@common.auth
def withdraw():
    print('取款')
    while True:
        balance = input('请输入取款金额：').strip()
        if balance.isdigit():
            balance = int(balance)
            flag, msg = bank.withdraw_interface(user_info['name'], balance)
            if flag:
                print(msg)
                break
            else:
                print(msg)


@common.auth
def check_records():
    print('查看流水')
    records = bank.check_records_interface(user_info['name'])
    for record in records:
        print(record)


@common.auth
def shop():
    """
    1.先循环打印出商品
    2.用户输入数字选择商品（判断是否是数字，判断输入的数字是否在范围内）
    3.取出商品名，商品价格
    4.判断用户余额是否大于商品价格
    5.余额大于商品价格时，判断此商品是否在购物车里
        在购物车里，个数加1
        不在购物车里，拼出字典放入（{’good':{'price':10,'count':1}}）
    6.用户余额减掉商品价格
    7.花费加上商品价格
    8.当输入q时，购买商品
        8.1 消费为0，直接退出
        8.2 打印购物车
        8.3 接受用户输入，是否购买 当输入y，直接调购物车接口实现购物
    :return:
    """
    print('购物')
    user_balance=bank.check_balance_interface(user_info['name'])
    cost=0
    shopping_cart={}
    goods_list=[
        ['coffee',10],
        ['chicken',50],
        ['iphone',5000],
        ['car',10000],

    ]
    while True:
        for i,good in enumerate(goods_list): #enumerate把金额迭代对象生成索引
            print('%s:%s'%(i,good))
        choice=input('请选择要购买的商品：').strip()
        if choice.isdigit():
            choice=int(choice)
            if choice>len(goods_list):continue
            good_name=goods_list[choice][0]
            good_price=goods_list[choice][1]
            if user_balance>=good_price:
                if good_name in shopping_cart:
                    shopping_cart[good_name]['count']+=1
                else:
                    shopping_cart[good_name]={'price':good_price,'count':1}
                user_balance-=good_price
                cost+=good_price
        if choice=='q':
            if cost==0:
                break
            print(shopping_cart)
            config=input('您确定购买吗？(y/n)').strip()
            if config.upper()=='Y':
                flag,msg=shopping.shopping_interface(user_info['name'],cost,shopping_cart)
                if flag:
                    print(msg)
                    break
                else:
                    print(msg)
                    break
            else:
                print('您什么都没买')
                break





@common.auth
def check_shopping_cart():
    shopping_cart=shopping.check_shoppingcart_interface(user_info['name'])
    print(shopping_cart)


def login_out():
    user_info['name']=None

func_dic = {
    '1': login,
    '2': register,
    '3': check_balance,
    '4': transfer,
    '5': repay,
    '6': withdraw,
    '7': check_records,
    '8': shop,
    '9': check_shopping_cart,
    '10':login_out,

}


def run():
    while True:
        print("""
        1.登录
        2.注册
        3.查看余额
        4.转账
        5.还款
        6.取款
        7.查看流水
        8.购物
        9.查看购买商品
        10.注销
        """)
        choice = input("请选择：").strip()
        if choice not in func_dic:
            continue
        func_dic[choice]()
