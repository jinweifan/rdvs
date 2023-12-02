"""
Name:    pro
Author:  ReddyFan
Date:    2023/2/16 17:28
Desc:  
"""
import requests

orderId = "O23021617150653964291"
pwd = "hiker2023"
host = "flow.hailiangip.com"
port = "14223"
user = orderId
password = 'pwd=' + pwd + "&pid=18" + "&cid=188" + "&uid=" + "&sip=0" + "&nd=1"
targetUrl = "http://api.hailiangip.com:8422/api/myIp"


def httpProxyWithPassRequest(targetUrl):
    proxyUrl = "http://" + user + ":" + password + "@" + host + ":" + port
    proxy = {"http": proxyUrl, "https": proxyUrl}
    r = requests.get(targetUrl, proxies=proxy)
    print("status Code : " + str(r.status_code))
    print(r.text)
    # print(r.json())
    return


if __name__ == '__main__':
    httpProxyWithPassRequest(targetUrl)
