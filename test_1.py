from bs4 import BeautifulSoup
from urllib.request import urlopen

response = urlopen('https://morvanzhou.github.io/static/scraping/basic-structure.html')
html = response.read().decode('utf-8')
# print(html)
soup = BeautifulSoup(html, features='lxml')
# print(soup.h1)
# print(soup.p)
all_href = soup.find_all('a')
for each in all_href:
    print(each['href'])
