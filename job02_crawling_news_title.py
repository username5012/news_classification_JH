from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
pages = [101, 101, 101, 71, 94, 73]    # 데이터의 불균형. => 적은 쪽을 중복 데이터로 늘린다 or 큰 쪽을 줄인다.
# 중간 단위에 맞춰 많은 쪽을 100페이지로 데이터 양을 축소하고, 맨 마지막 장에는 20개가 다 차 있지 않을 수 있으니, 마지막 페이지는 제외한다.


options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver', options=options)
df_title = pd.DataFrame()

for i in range(4, 6):     # section
    titles = []
    for j in range(1, pages[i]):  # page
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i,j)
        driver.get(url)
        time.sleep(0.2)
        for k in range(1, 5): #x_path
            for l in range(1, 6): #x_path
                x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l)

                try:
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣]').sub(' ', title)
                    titles.append(title)

                except NoSuchElementException as e:
                    try:
                        x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)
                        title = driver.find_element('xpath', x_path).text
                        title = re.compile('[^가-힣]').sub(' ', title)
                        titles.append(title)
                    except:
                        print('error')

                except:
                    print('error')


        if j % 10 == 0:
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_section_title['category'] = category[i]
            df_title = pd.concat([df_title, df_section_title], ignore_index=True)
            df_title.to_csv('./crawling_data/crawling_data_{}_To_{}.csv'.format(category[i], j),
                            index = False)
            titles = []

