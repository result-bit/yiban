import json
import queue
import threading
import time
import random
import ybapi.yblogin
from ybapi.ybvote import POETRY
from ybapi.yb import CONFIG_PATH

q = queue.Queue()


def read_passwd():
    with open('passwd.txt', 'r') as f:
        data = f.readlines()
        for line in data:
            odom = line.split('|')
            if f'\n' in odom[1]:
                odom[1] = odom[1].replace(f'\n', '')
                account.append(odom[0])
                passwd.append(odom[1])
            elif f'\n' not in odom[1]:
                account.append(odom[0])
                passwd.append(odom[1])


''''
发布投票
'''


def add_vote_task(account, passwd):
    try:
        yiban_user_token = ybapi.yblogin.getUserToken(account, passwd)
        token = dict(yiban_user_token=yiban_user_token)
        if token != None:
            add_vote_result = ybapi.ybvote.vote(token, puid, group_id).add("你觉得哪首诗句好", "你觉得哪首诗句好",
                                                                           POETRY[random.randint(0, 97)],
                                                                           POETRY[random.randint(0, 97)])
            if '操作成功' in add_vote_result['message']:
                vote_id = add_vote_result['data']['lastInsetId']
                q.put(vote_id)
                print('{} 发布投票成功 | 目前有{}个队列任务'.format(account, q.qsize()))
    except Exception as e:
        with open('error.txt', 'a') as f:
            f.write("发布投票出错" + str(e) + "\r\n")


''''
主线程
'''


def run(id):
    phone_it, password_it = iter(account), iter(passwd)
    while True:
        try:
            p, p0 = next(phone_it), next(password_it)
            add_vote_task(p, p0)
            while not q.empty():
                vote_id = q.get(block=False)
                for i in range(len(account)):
                    try:
                        yiban_user_token = ybapi.yblogin.getUserToken(account[i], passwd[i])
                        token = dict(yiban_user_token=yiban_user_token)
                        if token != None:
                            ready_vote_result = ybapi.ybvote.go(token, puid, group_id, actor_id, vote_id, 0, 0).vote(
                                auto=True)
                            up_vote_result = ybapi.ybvote.go(token, puid, group_id, actor_id, vote_id, 0, 0).up()
                            reply_vote_result = ybapi.ybvote.go(token, puid, group_id, actor_id, vote_id, 0, 0).reply(
                                POETRY[random.randint(0, 96)])
                            print(
                                '[{}] {} 参与投票 {} 点赞投票 {} 评论投票 {} 当前任务ID {}'.format(id, account[i], ready_vote_result,
                                                                                   up_vote_result, reply_vote_result,
                                                                                   vote_id))
                    except Exception as e:
                        with open('error.txt', 'a') as f:
                            f.write("参与投票出错" + str(e) + "\r\n")
        except StopIteration:  # 当队列执行到最后一个 重新赋值
            phone_it, password_it = iter(account), iter(passwd)


if __name__ == '__main__':
    account = []
    passwd = []
    read_passwd()
    ybapi.yb.Init(CONFIG_PATH, account[0], passwd[0])
    with open(CONFIG_PATH) as f:
        config = json.loads(f.read())
    try:
        group_id = config['group_id']
        puid = config['puid']
        channel_id = config['channel_id']
        actor_id = config['actor_id']
        nick = config['nick']
    except Exception as e:
        print(e)
        exit()
    t1 = threading.Thread(target=run, args=("线程1 ",))
    t2 = threading.Thread(target=run, args=("线程2 ",))
    t3 = threading.Thread(target=run, args=("线程3 ",))
    t1.start()
    time.sleep(3)
    t2.start()
    time.sleep(0.5)
    t3.start()
