import time
import random
import requests
import os
import shutil
import sys

dirname = os.getcwd()
#dirname = "/data/data/com.termux/files/home/python"

headers = {
    'cookie':'',
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

emoji = ["打卡"]

sendurl = 'https://api.live.bilibili.com/msg/send'

roomJsonUrl = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom'

fansMedalUrl = 'https://api.live.bilibili.com/xlive/web-room/v1/fansMedal/room'


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
    if os.path.exists("{}/未打卡.txt".format(dirname)) and os.path.getsize("{}/未打卡.txt".format(dirname)) != 0:
        file = open("{}/未打卡.txt".format(dirname), mode="r", encoding='utf-8')
        for index, line in enumerate(file):
            if line.strip() != "":
                list.append(line.strip().split("#")[0])
        file.close()
    else:
        input("{}/未打卡.txt 不存在".format(dirname))
    return list


def clock():
    list = getList()
    for roomid in list:
        time.sleep(1)
        send_msg = random.choice(emoji)
        roomJson = getRoomJson(roomid)
        Pass = isPass(roomJson)
        if not Pass:
            userid = getUserId(roomJson)
            fansMedalJson = getFanJson(userid)
            Light = isLight(fansMedalJson)
            Live = isLive(roomJson)

            if Light:
                    data['rnd'] = int(time.time())
                    data['roomid'] = getTrueRoomId(roomJson)
                    data['msg'] = send_msg
                    response = requests.post(
                        url=sendurl, data=data, headers=headers)
                    if response.status_code == 200:
                        print("[{}]:[{}],已打卡！".format(
                            roomid, getUserName(roomJson)))
            else:
                print("[{}:{}]已打卡，无需再打卡！".format(
                    roomid, getUserName(roomJson)))


clock()
