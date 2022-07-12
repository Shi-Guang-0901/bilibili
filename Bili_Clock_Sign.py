from os.path import dirname
import time
import random
import requests
import os
import sys


dirname = os.path.dirname(sys.argv[0])
# print("path")
# print(dirname)
if dirname == '':
    dirname = '.'
#dirname = '/data/data/com.termux/files/home/python/'

headers = {
    'cookie': '',
    'origin': 'https://live.bilibili.com',
    'referer': 'https://www.bilibili.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': '',
}


data = {
    'color': '65532',
    'fontsize': '25',
    'mode': '1',
    'msg': '',
    'rnd': '',
    'roomid': '',
    'bubble': '0',
    'csrf_token': '',
    'csrf': '',
}

emoji = ["(⌒▽⌒)", "（￣▽￣）", "(=・ω・=)", "(｀・ω・´)",
         "(〜￣△￣)〜", "(･∀･)", "(°∀°)ﾉ", "(￣3￣)", "╮(￣▽￣)╭",
         "_(:3」∠)_", "( ´_ゝ｀)", "(>_>)", "Σ(ﾟдﾟ;)",
         "Σ( ￣□￣||)", "(´；ω；`)", "（/TДT)/", "(^・ω・^ )",
         "(｡･ω･｡)", "(●￣(ｴ)￣●)", "ε=ε=(ノ≧∇≦)ノ", "(´･_･`)",
         "（￣へ￣）", "(￣ε(#￣) Σ", "（#-_-)┯━┯", "( ♥д♥)",
         "Σ>―(〃°ω°〃)♡→", "⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄", "･*･:≡(　ε:)"]

sendurl = 'https://api.live.bilibili.com/msg/send'

roomJsonUrl = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom'

fansMedalUrl = 'https://api.live.bilibili.com/xlive/web-room/v1/fansMedal/room'

doSign = 'https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign'

# 根据房间号从JSON中获取房间信息
def getRoomJson(roomid):
    return requests.get(
        url=roomJsonUrl, params={'room_id': roomid}, headers=headers).json()


def getFanJson(uid):
    return requests.get(
        url=fansMedalUrl, params={'target_id': uid},  headers=headers).json()


def isLight(fanJson):
    return (fanJson[
        'data']['medal']['today_feed'] < 100)


def getTrueRoomId(roomJson):
    return roomJson[
        'data']['room_info']['room_id']


def getUserId(roomJson):
    return roomJson[
        'data']['room_info']['uid']


def isLive(roomJson):
    return (roomJson[
        'data']['room_info']['live_status'] == 1)


def getUserName(roomJson):
    return roomJson[
        'data']['anchor_info']['base_info']['uname']


def getMedalName(roomJson):
    return roomJson[
        'data']['anchor_info']['medal_info']['medal_name']


def isPass(roomJson):
    return (roomJson['code'] == 19002005)


def getList():
    list = []
    if os.path.exists("{}/roomid.txt".format(dirname)) and os.path.getsize("{}/roomid.txt".format(dirname)) != 0:
        file = open("{}/roomid.txt".format(dirname),
                    mode="r", encoding='utf-8')
        for index, line in enumerate(file):
            if line.strip() != "":
                list.append(line.strip().split("#")[0])
        file.close()
    else:
        input("{}不存在".format(sys.argv[1]))
    return list


def word_length(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = int((utf8_length - length)/2 + length)

    for num in range(0, 6-length):
        value += ' '

    return value


getCountURL = 'https://api.live.bilibili.com/fans_medal/v5/live_fans_medal/iApiMedal'

URL = 'https://api.live.bilibili.com/xlive/app-ucenter/v1/user/GetMyMedals?page={}&page_size={}'


def getAnti():
    list = []
    file = open("{}/不打卡.txt".format(dirname), mode="r", encoding='utf-8')
    for index, line in enumerate(file):
        if line.strip() != "":
            list.append(int(line.strip().split("#")[0]))
    file.close()
    return list


def checkeDoSign():
    response = requests.get(url=URL.format(1, 10), headers=headers).json()
    totalpages = response['data']['page_info']['total_page']
    print(totalpages)
    print("一共有{}页\n".format(totalpages))
    fansMedalList = []
    for num in range(1, totalpages+1):
        response = requests.get(url=URL.format(
            num, 10), headers=headers).json()
        temp = response['data']['items']
        fansMedalList.extend(temp)
    anti = getAnti()
    f2 = open("{}/roomid.txt".format(dirname), "w", encoding="utf-8")
    for fansMedal in fansMedalList:
        if fansMedal['roomid'] not in anti:
            f2.write("{}#{}\n".format(fansMedal['roomid'], fansMedal['uname']))


def clock():
    checkeDoSign()

    # 哔哩哔哩 1 签到
    dosign = requests.get(
        url=doSign, headers=headers)

    if dosign.status_code == 200:
        dosign = dosign.json()
        if dosign['code'] == 0:
            print('签到成功！已经签到{}天\n'.format(dosign['data']['hadSignDays']))
        elif dosign['code'] == 1011040:
            print('{}\n'.format(dosign['message']))
        elif dosign['code'] == -1:
            print('{}\n'.format(dosign['message']))
    

    list = getList()
    notDaka = open("{}/{}".format(dirname, "未打卡.txt"), "w", encoding="utf-8")
    for roomid in list:
        time.sleep(1.5)
        send_msg = random.choice(emoji)
        roomJson = getRoomJson(roomid)

        if roomJson['code'] == -412:
            input('请求被拦截')
            exit(0)

        Pass = isPass(roomJson)
        if not Pass:
            Live = isLive(roomJson)
            if not Live:
                data['rnd'] = int(time.time())
                data['roomid'] = getTrueRoomId(roomJson)
                data['msg'] = send_msg
                response = requests.post(
                    url=sendurl, data=data, headers=headers)
                if response.status_code == 200:
                    responseJson = response.json()
                    # print(responseJson)
                    if responseJson['code'] == 0:
                        print("[{}:{}]\t已打卡！".format(
                            (roomid).rjust(8, ' '), word_length(getMedalName(roomJson))))
                    elif responseJson['code'] == 11000:
                        print("[{}:{}]\t点亮失败，该直播间无法点亮".format(
                            (roomid).rjust(8, ' '), word_length(getMedalName(roomJson))))
                    elif responseJson['code'] == -111:
                        print(responseJson['message'])
                    elif responseJson['code'] == -403:
                        print("[{}:{}]\t打卡失败！{}".format((roomid).rjust(8, ' '), word_length(
                            getMedalName(roomJson)), responseJson['message']))
                    else:
                        print("错误代码为{}".format(responseJson['code']))
                else:
                    print('response.status_code = {}'.fotmat(response.status_code))
            else:
                print("[{}:{}]\t正在直播！".format(
                    (roomid).rjust(8, ' '), word_length(getMedalName(roomJson))))
                notDaka.write("{}#{}\n".format(
                    roomid, getUserName(roomJson)))


clock()
# input('Press Enter to exit...')
