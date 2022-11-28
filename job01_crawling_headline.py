from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100' # 정치
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101' # 경제

# 네이버 뉴스 url 주소는 마지막 1자리에 따라 카테고리가 결정됨. => for문 사용





headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
# headers를 주지 않을 경우, 네이버 내에서 크롤링하는 것으로 인식하여 작동하지 않음.
# headers는 관리자 도구-> Networks -> Request headers -> User-Agent부터 ~까지 적용.

df_titles = pd.DataFrame()
# requests : 서버에 특정 행동을 요청
# print(list(resp))

for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # print(soup)
    title_tags = soup.select('.cluster_text_headline')
    titles = []
    for title_tag in title_tags:
        title = title_tag.text
       # titles.append(title_tag.text)
        title = re.compile('[^가-힣0-9a-zA-z ]').sub(' ', title)   #[가-힣].sub('', 대상) : 가-힣 범위에 있는 문자를 제거. => [가-힣]을 제외한 나머지를 지우고 싶은 경우, [^가-힣]으로 범위를 지정해주면 됨.
        titles.append(title)
# cluster_text_headline 내에 title_tag (제목) 데이터를 가지고 있음. => soup.select()로 () 안의 내용 지정.
# for문 사용하여 각 title_tag 출력
    df_section_titles = pd.DataFrame(titles, columns=['title'])
    df_section_titles ['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
print(df_titles)
print(df_titles.category.value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)
