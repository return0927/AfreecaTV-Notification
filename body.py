#-*- coding: utf-8 -*- Python3
# Created By Eunhak Lee
# Created At 2017.09.16 11:29 PM
# https://github.com/return0927
#


import time, bs4, requests, json
from settings import _SETTING

setting = _SETTING()

stationURL = "http://live.afreecatv.com:8079/app/index.cgi?szBjId=%s"


# Now, only one person can be looked up
# 아직 한 명의 아프리카티비 방송국만을ㅇ 확인합니다.
_ID, webhookURL = setting.lookupIDS[0]['id'], setting.lookupIDS[0]['hook']



class Avatar:
    username = "# Webhook Profile Name #"
    avatar_url = "# Webohok Profile Picture URL #"
    tts = False


def _live_check(_URL):
    soup = bs4.BeautifulSoup(
        requests.get(
            _URL,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Whale/0.10.36.14 Safari/537.36"
            }
        ).text,

        'html.parser'
    )
    _LIVE = soup.select("body > div.mybs_wrap > div.content_area > div.aside > div.app_area > div > div.player_area2 > button")[0]

    _RETURN = False
    try:
        if _LIVE['onclick']:
            return True, _get_thumbnail(_URL)
    except:
        return False, ''


def _get_thumbnail(_URL):
    soup = bs4.BeautifulSoup(
        requests.get(
            _URL,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Whale/0.10.36.14 Safari/537.36"
            }
        ).text,

        'html.parser'
    )
    _THUMB = soup.select("#broadImg")

    return _THUMB[0]['src']


def _send_webhook(goto_url, thumb_img, url=webhookURL, type="broadcast_started"):
    data = {
        "username": Avatar.username,
        "avatar_url": Avatar.avatar_url,
        "tts": Avatar.tts,
        "content": setting.textArr['ContentMsg'][type]%goto_url,
        "author": {
            "name": "한숨이절로TV",
            "icon_url": Avatar.avatar_url,
        },
        "image": {
            "url": thumb_img,
            "height": 180,
            "width": 240
        },
        "embeds": [
            {
                "color": setting.textArr['ColorCode'][type],
                "title": setting.textArr['TitleMsg'][type],
                "description": setting.textArr['DescriptionMsg'][type],
                "image": {
                    "url": thumb_img
                },
                "url": goto_url,
                "fields": [
                    {"name": "/ 문의하기 /", "value": "# HOW TO CONTACT Message #", "inline": False}
                ],
                "footer": {
                    'text': "ⓒ 이은학 (이은학#9299) \\ Github @R3turn0927 \\ KakaoTalk @bc1916"
                }
            }
        ]
    }

    return requests.post(url, data=json.dumps(data), headers={"Content-type":"multipart/form-data"}).text


_BEFORE = 0
_CASTING = False

while True:
    if time.time() - _BEFORE > 60:
        _BEFORE = time.time()

        _LIVE, _THUMB = _live_check(stationURL%_ID)

        if _CASTING != _LIVE:
            if _LIVE:
                _send_webhook("http://afree.ca/%s"%_ID, _THUMB)
            else:
                _send_webhook("http://afreeca.com/%s"%_ID, "# PlaceHolder Thumbnail #", type="broadcast_stopped")
            _CASTING = _LIVE