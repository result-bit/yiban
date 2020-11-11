import json
import os
from ybapi.yblogin import getUserToken
from ybapi import yblogin

CONFIG_PATH = 'config.json'
'''
config.json 存储键值对
user 应为 'username': 'password'
'''
def saveConfig(info):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(info, f, indent=4)


def checkUser(account, passwd):
    for i in range(len(account)):
        print('目前进度:({}/{})'.format(i, len(account)))
        try:
            if getUserToken(account[i], passwd[i]) == None:
                del account[i]
                del passwd[i]
        except IndexError:
            return account, passwd



def Init(path, user, passwd):
    if not os.path.exists(path):
        yiban_user_token = getUserToken(user, passwd)
        token = dict(yiban_user_token=yiban_user_token)
        global_info = yblogin.getInfo(token)
        saveConfig(global_info)
