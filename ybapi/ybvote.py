#!/usr/bin/env python3
# coding=utf-8
import re
import time
import requests as r
from .yblogin import BASEURL

POETRY = [
    "把你自己放到人群中去评价，才叫客观。",
    "本来无望的事，大胆尝试，往往能成功。",
    "不悲伤，定会快乐，不犹豫，定会坚持。",
    "不论你是什么样的人都有你能走的路。",
    "诚心诚意，“诚”字的另一半就是成功。",
    "承认自己的伟大，就是认同自己的愚昧。",
    "出门走好路，出口说好话，出手做好事。",
    "从哪里跌倒就从哪里爬起来，爬起来再哭。",
    "挫折其实就是迈向成功所应缴的学费。",
    "但愿每次回忆，对生活都不感到负疚。",
    "当眼泪流尽的时候，留下的应该是坚强。",
    "凡真心尝试助人者，没有不帮到自己的。",
    "钢钎与顽石的碰撞声，是一首力的歌曲。",
    "过去是那么的荒唐，未来是那么的迷茫。",
    "行动是老子，知识是儿子，创造是孙子。",
    "好好扮演自己的角色，做自己该做的事。",
    "灰心生失望，失望生动摇，动摇生失败。",
    "家庭是合法的妓院，妓院是非法的家庭。",
    "骄傲是胜利的敌人，努力是成功的朋友。",
    "脚步怎样才能不断前时？把脚印留在身后。",
    "教育是人才的娘家，社会是人才的婆家。",
    "精力充沛的青春，是不怎么容易灭亡的。",
    "困难里包含着胜利，失败里孕育着成功。",
    "懒惰像生锈一样，比操劳更消耗身体。",
    "劳动是知识的源泉；知识是生活的指南。",
    "忙于采集的蜜蜂，无暇在人前高谈阔论。",
    "没有口水与汗水，就没有成功的泪水。",
    "没有人永远活着，没有东西可以经久。",
    "每天告诉自己一次，“我真的很不错”。",
    "每一发奋努力的背后，必有加倍的赏赐。",
    "梦想一旦被付诸行动，就会变得神圣。",
    "迷了的时候叫做-爱情，觉悟了就叫慈悲。",
    "能付出爱心就是福，能消除烦恼就是慧。",
    "你可以一无所有，但绝不能一无是处。",
    "你什么时候放下，什么时候就没有烦恼。",
    "你拥有自尊，你更能尊重别人的自尊。",
    "你真诚地爱自己，你更能真诚地爱别人。",
    "旁观者清楚的，只是旁观者自己的猜测。",
    "脾气嘴巴不好，心地再好也不能算好人。",
    "青春是在它即将逝去的时候最具有魅力。",
    "去做你害怕的事，害怕自然就会消失。",
    "人类的一切努力的目的在于获得幸福。",
    "人生风光的背后，不是沧桑，就是肮脏。",
    "人生就像奕棋，一步失误，全盘皆输。",
    "人生没有理想，生命便只是一堆空架子。",
    "人生难免不如意时，你懂得排遣就好。",
    "人生伟业的建立，不在能知，乃在能行。",
    "人因不了解而恐惧，或因不了解而胆大。",
    "人只要一息尚存，对什么都可抱有希望。",
    "任何的限制，都是从自己的内心开始的。",
    "山路曲折盘旋，但毕竟朝着顶峰延伸。",
    "善境逆境，常常就是陶铸圣贤的温床。",
    "商人的兴趣就在那些能找到财富的地方。",
    "生活充满了选择，而生活的态度就是一切。",
    "生活其实很简单，过了今天就是明天。",
    "生活中最大的目的，并不是知识而是行动。",
    "生命里没有你的日子，就好像在浪费时间。",
    "时间会改变一切，就像我已经不喜欢你。",
    "时间美化那仅有的悸动，也磨平激动。",
    "时间种下的伤害，却无法用时间来填埋。",
    "说的出来的不叫苦说，不出来的才叫苦。",
    "松驰的琴弦，永远奏不出美妙的乐曲。",
    "所有智力方面的工作都要依赖于兴趣。",
    "躺在被窝里的人，并不感到太阳的温暖。",
    "挑选朋友要慎重，更换朋友要更慎重。",
    "通过云端的道路，只亲吻攀登者的足迹。",
    "望洋兴叹的人，永远达不到成功的彼岸。",
    "我希望我是月亮，这样一辈子跟着你走。",
    "希望，只有和勤奋作伴，才能如虎添翼。",
    "先相信你自己，然后别人才会相信你。",
    "闲适和宁静，对于浪花，意味着死亡。",
    "现在的失败，是在为以后的成功铺路。",
    "相信时间的力量，可以冲淡很多东西。",
    "像孩子一样，永远相信希望，相信梦想。",
    "学问必须合乎自己的兴趣，方可得益。",
    "学习的最大动力，是对学习材料的兴趣。",
    "一个人脸上的表情比她身上穿得更重要。",
    "一切节约，归根到底都是时间的节约。",
    "应该多行善事，为了做一个幸福的人。",
    "拥有逆境，便拥有一次创造奇迹的机会。",
    "友谊活跃和青春的歌声会减轻我们的痛苦。",
    "有很多人是用青春的幸福作成功代价的。",
    "有时虚无缥缈的梦幻就是你一生的期待。",
    "雨后的彩虹更美丽，磨难的人生更辉煌。",
    "预见未来，遇见你，期待最美的时间。",
    "遇顺境，处之淡然，遇逆境，处之泰然。",
    "在人生舞台上，从不给落伍者颁发奖牌。",
    "在书本里找不到的字母，而是活的知识。",
    "战胜困难，走出困境，成功就会属于你。",
    "站在新起点，迎接新挑战，创造新成绩。",
    "珍惜时间的秘诀：少说空话，多做工作。",
    "珍惜现在所拥有的幸福，活在当下最好。",
    "知识比金子宝贵，因为金子买不到它。",
    "知识需要反复探索，土地需要辛勤耕耘。",
    "智者的梦再美，也不如愚人实干的脚印。",
    "自己打败自己的远远多于比别人打败的。",
    "做人是要开心一点的，不开心不如去死。",
]


class vote:

    def __init__(self, token, puid, group_id):
        self.token = token
        self.puid = puid
        self.group_id = group_id
    '''
    易班发起单选双项投票
    参数: 标题, 正文, 选项1, 选项2
    '''

    def add(self, title, subjectTxt, subjectTxt_1, subjectTxt_2, subjectPic=None, voteValue=1893427200, public_type=0,
            isAnonymous=0, istop=1, sysnotice=2, isshare=1):
        payload = {
            'puid': self.puid,
            'group_id': self.group_id,
            'scope_ids': self.group_id,
            'title': title,
            'subjectTxt': subjectTxt,
            'subjectPic': subjectPic,
            'options_num': 2,
            'scopeMin': 1,
            'scopeMax': 1,
            'minimum': 1,
            'voteValue': time.strftime("%Y-%m-%d %H:%M", time.localtime(voteValue)),
            'voteKey': 2,
            'public_type': public_type,
            'isAnonymous': isAnonymous,
            "voteIsCaptcha": 0,
            'istop': istop,
            'sysnotice': sysnotice,
            'isshare': isshare,
            'subjectTxt_1': subjectTxt_1,
            'subjectTxt_2': subjectTxt_2,
            'rsa': 1,
            'dom': '.js-submit'
        }

        Add_Vote = r.post(BASEURL + 'vote/vote/add',
                          cookies=self.token, data=payload, timeout=10)
        return Add_Vote.json()

    '''
    获取投票
    返回 JSON 字典
    '''

    def get(self, size=10, page=0, status=1, sort=1, time=0):
        payload = {
            'puid': self.puid,
            'group_id': self.group_id,
            'page': page,
            'size': size,
            'status': status,
            'sort': sort,
            'time': time
        }

        Get_Vote = r.post(BASEURL + 'vote/index/getVoteList',
                          cookies=self.token, data=payload, timeout=10)
        return Get_Vote.json()["data"]["list"]


class go:
    '''
    准备投票参数
    参数: token, vote_id
    '''

    def __init__(self, token, puid, group_id, actor_id, vote_id, isOrganization=0, ispublic=0):

        self.token = token
        self.puid = puid
        self.group_id = group_id
        self.actor_id = actor_id
        self.vote_id = vote_id
        self.isOrganization = isOrganization
        self.ispublic = ispublic
        self.Get_Token = r.get(BASEURL + 'vote/vote/showDetail/vote_id/' + str(
            vote_id) + '/puid/' + self.puid + '/group_id/' + self.group_id, cookies=self.token, timeout=10)
        self.vote_token = re.search(
            r'g_config.token = "(.*)"', self.Get_Token.text).group(1)

        payload = {
            'vote_id': vote_id,
            'uid': self.actor_id,
            'puid': self.puid,
            'pagetype': 1,
            'group_id': self.group_id,
            'actor_id': self.actor_id,
            'token': self.vote_token,
            'isSchoolVerify': 1,
            'isLogin': 1,
            'isOrganization': isOrganization,
            'ispublic': ispublic
        }

        self.Get_Vote_Detail = r.post(
            BASEURL + 'vote/vote/getVoteDetail', cookies=self.token, data=payload, timeout=10)

        self.mount_id = self.Get_Vote_Detail.json(
        )['data']['vote_list']['Mount_id']

    '''
    参与单选投票
    '''

    def vote(self, auto=False, choice=0):

        if auto:
            vote_data = self.Get_Vote_Detail.json()['data']
            minimum = vote_data['vote_list']['minimum']
            scopemax = vote_data['vote_list']['scopeMax']
            voptions_id = []

            for i in range(0, int(minimum)):
                voptions_id.append(vote_data['option_list'][i]['id'])

            payload = {
                'puid': self.puid,
                'group_id': self.group_id,
                'vote_id': self.vote_id,
                'voptions_id': ','.join(voptions_id),
                'minimum': minimum,
                'scopeMax': scopemax
            }

        else:
            voptions_id = self.Get_Vote_Detail.json(
            )['data']['option_list'][choice]['id']

            payload = {
                'puid': self.puid,
                'group_id': self.group_id,
                'vote_id': self.vote_id,
                'voptions_id': voptions_id,
                'minimum': 1,
                'scopeMax': 1
            }

        Go_Vote = r.post(BASEURL + 'vote/vote/act',
                         cookies=self.token, data=payload, timeout=10)
        return Go_Vote.json()['message']

    '''
    评论投票
    参数: 正文
    '''

    def reply(self, content, comment_id=0, user_id=0):

        payload = {
            'mountid': self.mount_id,
            'msg': content,
            'group_id': self.group_id,
            'actor_id': self.actor_id,
            'vote_id': self.vote_id,
            'author_id': self.actor_id,
            'puid': self.puid,
            'reply_comment_id': comment_id,
            'reply_user_id': user_id
        }

        Go_Vote_Reply = r.post(BASEURL + 'vote/vote/addComment',
                               cookies=self.token, data=payload, timeout=10)
        return Go_Vote_Reply.json()['message']

    '''
    删除评论
    '''

    def remove(self, content, comment_id, user_id=0):

        payload = {
            'mountid': self.mount_id,
            'commentid': comment_id,
            'puid': self.puid,
            'group_id': self.group_id,
            'author_id': self.actor_id,
            'comment_author_id': self.actor_id,
            'reply_name': 'noname',
            'vote_id': self.vote_id
        }

        Del_Vote_Reply = r.post(BASEURL + 'vote/vote/addComment',
                                cookies=self.token, data=payload, timeout=10)
        return Del_Vote_Reply.json()['message']

    '''
    点赞投票
    '''

    def up(self):

        payload = {
            'group_id': self.group_id,
            'puid': self.puid,
            'vote_id': self.vote_id,
            'actor_id': self.actor_id,
            'flag': 1
        }

        Up_Vote = r.post(BASEURL + 'vote/vote/editLove',
                         cookies=self.token, data=payload, timeout=10)
        return Up_Vote.json()['message']

    '''
    取消点赞投票
    '''

    def down(self):

        payload = {
            'group_id': self.group_id,
            'puid': self.puid,
            'vote_id': self.vote_id,
            'actor_id': self.actor_id,
            'flag': 0
        }

        Down_Vote = r.post(BASEURL + 'vote/vote/editLove',
                           cookies=self.token, data=payload, timeout=10)
        return Down_Vote.json()['message']

    '''
    删除投票
    '''

    def delete(self):

        payload = {
            'group_id': self.group_id,
            'puid': self.puid,
            'vote_id': self.vote_id
        }

        Delete_Vote = r.post(BASEURL + 'vote/Expand/delVote',
                             cookies=self.token, data=payload, timeout=10)
        return Delete_Vote.json()['message']
