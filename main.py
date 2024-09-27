import csv
import time

import requests

#Парсинг даты постов и количества лайков страницы ВК
def get_posts():
    token = ''           #необходимо добавить токен вк
    version = 5.92
    domain = 'python_of' #доменное имя страницы вк для парсинга
    count = 100
    offset = 0
    all_posts = []


    while offset < 1000:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'domain': domain,
                                    'count': count,
                                    'offset': offset
                                }
                                )
        date = response.json()['response']['items']
        offset += 100
        all_posts.extend(date)
        time.sleep(0.5)
    return all_posts

def write_csv(date):
    with open ('filter.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('likes', 'date'))
        for post in date:
            a_pen.writerow((post['likes']['count'], post['date']))

all_posts = get_posts()
write_csv(all_posts)


# ------------------------------------------------------------------
#преобразование в датафрейм для просмотра и редактирования данных scv файла
# import pandas as pd
# import matplotlib.pyplot as plt
#
# df = pd.read_csv('filter.csv')



