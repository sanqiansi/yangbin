import json,os
from conf import settings

def save(user_dic):
    path = os.path.join(settings.DIR_DB, '%s.json' % user_dic['name'])
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(user_dic, f)



def select(name):
    path=os.path.join(settings.DIR_DB,'%s.json'%name)
    if not os.path.exists(path):
        return False
    with open(path,'r',encoding='utf-8') as f:
        user_dic=json.load(f)
        return user_dic