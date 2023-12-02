"""
Name:    爬取图片
Author:  ReddyFan
Date:    2023/1/27 17:21
Desc:  
"""

import requests

params = {"type": 5, "interval_id": "90:80", "action": None, "start": 5, "limit": 20}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
url = "https://movie.douban.com/j/chart/top_list"

resp = requests.get(url=url, params=params, headers=headers)
content = resp.json()

# print(type(content), content[0], '\n', content)
# print(json.loads(json.dumps(content))[0])

# for data in content:
#     # print(data)
#     print(json.dumps(data, indent=4, ensure_ascii=False, separators=(',', ':')))

if __name__ == '__main__':
    print(resp.headers)
    print(resp.encoding)
    # with open("电影.txt", mode="w", encoding="utf-8") as fp:
    #     index = 1
    #     for data in content:
    #         title = data["title"]
    #         score = data["score"]
    #         # fp.write(str(index) + " " + title + " " + score + "\n")
    #         fp.writelines(str(index) + " " + title + " " + score )
    #         index += 1
