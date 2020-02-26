import requests
from bs4 import BeautifulSoup


# r1 = requests.get(
#     url='https://dig.chouti.com/',
#     headers={
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
#                       "537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
#     }
# )
# 爬取信息
# soup = BeautifulSoup(r1.text, 'html.parser')
# content_list = soup.find(name='div', attrs={'class': 'link-con'})
#
# item_list = content_list.find_all(name='div', attrs={'class': 'link-item'})
#
# for item in item_list:
#     a = item.find(name='a', attrs={'class': 'link-title link-statistics'})
#     print(a.text.strip())

# 点赞
r2 = requests.post(
    url='https://dig.chouti.com/login',
    headers={
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                      "537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    },
    data={
        'phone': '+8618362882538',
        'password': 'cky159',
        'loginType': 2,
    }
)
print(r2.text)
