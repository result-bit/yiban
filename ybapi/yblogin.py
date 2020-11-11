import requests
import re
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3938.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
BASEURL = 'https://www.yiban.cn/'
'''
模拟 JSEncrypt 加密
加密方式为 PKCS1_v1_5
'''


# def rsaEncrypt(password, key):
#     cipher = PKCS1_v1_5.new(RSA.importKey(key))
#     return b64encode(cipher.encrypt(password.encode()))


def getUserToken(user, passwd):
    LOGIN_URL = 'https://mobile.yiban.cn/api/v2/passport/login?apn=2g&ct=1&identify=024D5128-F193-4BED-A709-9311A75F24BD&app=1&token=4e33740b%20b06d01bf%20db789d65%20778c43d3%20108acef6%20da656c17%2045d80989%202c362bfd&passwd=' + passwd + '&sversion=13.100000&account=' + user + '&device=iPhone11,8&v=4.6.11&sig=10D694188B79A54F'
    LoginURL = requests.post(LOGIN_URL).json()
    try:
        token = LoginURL['data']['token']
    except:
        token = LoginURL['message']
    return token


def getInfo(token):
    try:
        Get_Group_Info = requests.get(BASEURL + 'my/group/type/public', cookies=token, timeout=10)
        group_id = re.search(r'href="/newgroup/indexPub/group_id/(\d+)/puid/(\d+)"', Get_Group_Info.text).group(1)
        puid = re.search(r'href="/newgroup/indexPub/group_id/(\d+)/puid/(\d+)"', Get_Group_Info.text).group(2)
    except AttributeError:
        Get_Group_Info = requests.get(BASEURL + 'my/group/type/create', cookies=token, timeout=10)
        group_id = re.search(r'href="/newgroup/indexPub/group_id/(\d+)/puid/(\d+)"', Get_Group_Info.text).group(1)
        puid = re.search(r'href="/newgroup/indexPub/group_id/(\d+)/puid/(\d+)"', Get_Group_Info.text).group(2)

    payload = {
        'puid': puid,
        'group_id': group_id
    }

    Get_Channel_Info = requests.post(BASEURL + 'forum/api/getListAjax', cookies=token, data=payload, timeout=10)
    channel_id = Get_Channel_Info.json()['data']['channel_id']

    Get_User_Info = requests.post(BASEURL + 'ajax/my/getLogin', cookies=token, timeout=10)
    actor_id = Get_User_Info.json()['data']['user']['id']
    nick = Get_User_Info.json()['data']['user']['nick']

    info = {
        'group_id': group_id,
        'puid': puid,
        'channel_id': channel_id,
        'actor_id': actor_id,
        'nick': nick
    }

    return info
