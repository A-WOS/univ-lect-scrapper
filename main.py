import csv
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

lec_address = os.environ['lec_address']
course_param1 = os.environ['COURSE_PARAM1']
course_param2 = os.environ['COURSE_PARAM2']

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

lec_list = []


def save_to_file(list_lec):
    file = open("univ_all_lec.csv", mode="w", newline='')
    writer = csv.writer(file)
    writer.writerow(["index", "univ_lec_address", "subject_title"])
    for lec in list_lec:
        writer.writerow(list(lec.values())[0:3])
    return


for i in range(170, 180):
    # 과도한 요청으로 차단 방지
    sleep_time = random.uniform(2, 4)
    sleep(sleep_time)

    # 스크래핑 할 URL 일단 지정범위만..
    univ_url = f"{lec_address}&{course_param1}=2483191&{course_param2}=44{i:03}"

    url = session.get(url=univ_url, headers=headers)
    soup = BeautifulSoup(url.content, "html.parser")

    try:
        title = soup.find("div", {"class": "sub"}).get_text().strip().replace(u'\xa0', u' ')
        print(i, univ_url, title)

        lec_list.append({
            "index": i,
            "univ_lec_address": univ_url,
            "subject_title": title
        })

    except:
        print(f"{i} {univ_url} 정보 없음")
        continue

save_to_file(lec_list)
