# # 不是异步的
# import time
#
#
# def job(t):
#     print('Start job ', t)
#     time.sleep(t)               # wait for "t" seconds
#     print('Job ', t, ' takes ', t, ' s')
#
#
# def main():
#     [job(t) for t in range(1, 3)]  # for循环的简写
#
#
# t1 = time.time()
# main()
# print("NO async total time : ", time.time() - t1, " 秒")
"""一般方法"""
import requests
import time

src = "https://morvanzhou.github.io"
def normal():
    for i in range(2):
        r = requests.get(src)
        ul = r.url
        print(ul)
t1 =time.time()
normal()
print('爬取两个网页需要 ' + str(time.time() - t1))
"""异步方法"""
# import aiohttp
# import time
# import asyncio
# URL = 'https://morvanzhou.github.io'
#
#
# async def job(session):
#     response = await session.get(URL)       # 等待并切换
#     return str(response.url)
#
#
# async def main(loop):
#     async with aiohttp.ClientSession() as session:      # 官网推荐建立 Session 的形式
#         tasks = [loop.create_task(job(session)) for _ in range(2)]
#         finished, unfinished = await asyncio.wait(tasks)
#         all_results = [r.result() for r in finished]    # 获取所有结果
#         print(all_results)
#
# t1 = time.time()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(loop))
# loop.close()
# print("Async total time:", time.time() - t1)
