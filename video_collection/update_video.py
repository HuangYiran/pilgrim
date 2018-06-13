#! /usr/bin/env python3

import requests
import re
import subprocess
import time


def sniffing(url):
    try:
        r = requests.get(url)
        return r

    except:
        print("sniffing fail")
        return None


def get_ts_adds(txt):
    li = txt.split('\n')
    pattern1 = '(^#EXT-X-MEDIA-SEQUENCE:)(\d+)'
    pattern2 = '^https'
    cnt = 0
    adds = []

    for record in li:
        result1 = re.match(pattern1, record)
        result2 = re.match(pattern2, record)
        if result1 is not None:
            cnt = result1.groups()[1]

        if result2 is not None:
            adds.append(result2.string)

    return cnt, [adds[-1]]


def downloader(li, f, name, dire='./data/', postfix='mp4'):
    for i, line in enumerate(li):
        filename = dire+name+'.'+postfix
        cmd = 'ffmpeg -i '+line+' -c copy '+filename+' -y'
        print(cmd)
        f.write("file '"+filename+"'\n")
        subprocess.call(cmd, shell=True)


def concat(name, dire='./data/', postfix='mp4', fn='adds.txt'):
    out = dire+name+'.'+postfix
    cmd = 'ffmpeg -f concat -i '+fn+' -c copy -bsf:a aac_adtstoasc '+out
    print(cmd)
    subprocess.call(cmd, shell=True)


def update(url, update_time=0.1):
    pre = 0
    cnt2 = 0
    while True:
        # cnt2 = cnt2 % 2
        dire = './data/'
        r = sniffing(url)
        cnt, adds = get_ts_adds(r.text)
        print(cnt2,cnt,pre)
        if cnt == pre:
            continue
        else:
            pre = cnt
        cmd = 'mkdir '+dire
        time.sleep(0.5)
        subprocess.call(cmd, shell=True)
        with open('adds.txt', 'w') as f:
            downloader(adds, f, str(cnt2), dire)

        time.sleep(update_time)
        cnt2 += 1

def requests_extract(url):
    response = requests.get(url)
    pattern = "(')(https.*?m3u8.*?)(')"
    result = re.search(pattern, response.text)
    ret = result.groups()[1].encode('utf-8').strip()
    return ret


if __name__ == '__main__':
    url = 'https://www.skylinewebcams.com/en/webcam/israel/jerusalem-district/jerusalem/western-wall.html'
    url = requests_extract(url)
    update(url)
