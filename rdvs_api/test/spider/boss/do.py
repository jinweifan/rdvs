"""
Name:    do
Author:  ReddyFan
Date:    2023/2/10 10:06
Desc:  
"""
import requests

if __name__ == '__main__':
    resp = requests.get("https://www.zhipin.com",
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                        },

                        )
    # resp = requests.get(
    #     "https://www.zhipin.com/web/geek/job?query=&city=100010000&position=100109")
    # print(resp.text)
    print(resp.cookies.__dict__)
    print(resp.text)
    print(resp.json())
    # print(resp.json())
    # print(resp.json())
    # for k in resp.cookies.keys():
    #     print(k, "：", resp.cookies.get(k))
    # print(resp.json())
