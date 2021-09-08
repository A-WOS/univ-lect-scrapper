import os
import requests
from numpy import random
from time import sleep
from bs4 import BeautifulSoup

os.system("cls")

loginType = os.environ['LOGIN_TYPE']
loginKind = os.environ['LOGIN_KIND']
user = os.environ['USERID']
password = os.environ['PASSWORD']

# print(sess)
login = {
    'loginType': loginType,
    'loginKind': loginKind,
    'j_username': user,
    'j_password': password
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

login_url = os.environ['LOGIN_URL']
session = requests.session()
# 로그인을 해야 스크래핑이 가능함.
session.post(url=login_url, data=login)

for i in range(170, 190):
    # 과도한 요청으로 차단 방지
    sleep_time = random.uniform(2, 4)
    sleep(sleep_time)

    # 스크래핑 할 URL 일단 지정범위만..
    univ_url = f"https://hive.cju.ac.kr/usr/classroom/main.do?currentMenuId=&courseApplySeq=2483191&courseActiveSeq=44{i:03}"

    url = session.get(url=univ_url, headers=headers)
    soup = BeautifulSoup(url.content, "html.parser")

    try:
        title = soup.find("div", {"class": "sub"}).get_text().strip()
        print(i, univ_url, title)

    except:
        print(f"{i} {univ_url} 정보 없음")
        continue
