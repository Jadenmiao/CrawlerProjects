import requests
import os
from urllib.request import urlretrieve
img_url = 'https://morvanzhou.github.io/' \
          'static/img/description/learning_step_flowchart.png'
os.makedirs('./img/', exist_ok=True)
# the first way
img = urlretrieve(img_url, './img/img1.jpg')
# the second way
response = requests.get(img_url)
with open('./img/img2.jpg','wb') as f:
    f.write(response.content)
# 以上都是先把东西下载到内存里，完成后，再进行数据的写入硬盘操作
# the third way：边下边存,size=32byte/次
response2 = requests.get(img_url, stream=True)
with open('./img/img3.jpg', 'wb') as f2:
    for chunk in response2.iter_content(chunk_size=32):
        f2.write(chunk)
