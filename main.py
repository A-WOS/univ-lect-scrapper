import csv
import os
import requests
from numpy import random
from time import sleep
from bs4 import BeautifulSoup

os.system("cls")

# env_var
loginType = os.environ['LOGIN_TYPE']
loginKind = os.environ['LOGIN_KIND']
user = os.environ['USERID']
password = os.environ['PASSWORD']
login_url = os.environ['LOGIN_URL2']
lec_address = os.environ['lec_address']
course_param1 = os.environ['COURSE_PARAM1']
course_param2 = os.environ['COURSE_PARAM2']

login = {
    'loginType': loginType,
    'loginKind': loginKind,
    'j_username': user,
    'j_password': password
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/93.0.4577.63 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9 "
}

session = requests.session()
# 로그인을 해서 스크래핑이 가능함.
session.post(url=login_url, data=login)

lects = []


# csv파일로 저장 
def save_to_file(lects):
    file = open("univ_all_lec.csv", mode="w", newline='')
    writer = csv.writer(file)
    writer.writerow(["index", "univ_lec_address", "subject_title", "profess_name"])
    for lec in lects:
        writer.writerow(list(lec.values())[0:4])
    file.close()
    return


# 소스코드가 길어져서 함수로 만들어버림.
def convert_readable_text(c):
    return c.get_text().strip().replace(u'\xa0', u' ')


def reader_writer_csv(file_name, obj):
    with open(file_name, mode='w', newline='') as writer:
        with open('univ_all_lec.csv', mode='r') as reader:
            for line in reader:
                if obj in line:
                    writer.write(line)
                else:
                    continue
    reader.close()
    writer.close()
    return


# 교수명으로 검색하여 다른 파일에 저장
def search_profess(profess_name):
    file_name = "searched_profess.csv"
    reader_writer_csv(file_name, profess_name)
    return


# 과목명으로 검생
def search_subject(subject):
    file_name = "searched_subject.csv"
    reader_writer_csv(file_name, subject)
    return


for i in range(170, 176):
    # 과도한 요청으로 차단 방지
    sleep_time = random.uniform(2, 4)
    sleep(sleep_time)

    # 스크래핑 할 URL 일단 지정범위만..
    univ_url = f"{lec_address}&{course_param1}=2483191&{course_param2}=44{i:03}"

    url = session.get(url=univ_url, headers=headers)
    soup = BeautifulSoup(url.content, "html.parser")

    try:
        title = convert_readable_text(soup.find("div", {"class": "sub"}))
        pf_name = convert_readable_text(soup.find("ul", {"class": "info"}).find_all("li")[2])
        # print(i, univ_url, title, pf_name)
        print(title, pf_name)
        lects.append({
            "index": i,
            "univ_lec_address": univ_url,
            "subject_title": title,
            "profess_name": pf_name
        })

    except:
        continue

save_to_file(lects)
print("csv 파일로 저장 완료")

print("교수명 입력 : ")
profs_name = input()
search_profess(profs_name)

print("과목명 입력 : ")
sbj_name = input()
search_subject(sbj_name)
