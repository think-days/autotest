import random
from time import sleep

import requests

a = {'0341': {'640': [{'id': '495238', 'areaNo': 'IN-00-01', 'areaName': '默认', 'inventory': '默认货位(632)', 'qty': 632}]},
     '1035': {'640': [{'id': '495238', 'areaNo': 'IN-00-01', 'areaName': '默认', 'inventory': '默认货位(623)', 'qty': 623}]},
     '1255': {'640': [{'id': '495238', 'areaNo': 'IN-00-01', 'areaName': '默认', 'inventory': '默认货位(623)', 'qty': 623}]},
     '1287': {'640': [{'id': '495238', 'areaNo': 'IN-00-01', 'areaName': '默认', 'inventory': '默认货位(637)', 'qty': 637}]}}

e = []
for i, k in dict.items(a):
    for n, f in dict.items(k):
        b = {"invId": i, "rtNum": "1", "locationId": n, "locationAreaId": f[0]["id"]}
        e.append(b)
print("=====", e)

create_data = {
    "buId": 203755,
    "description": "",
    "entries": e,
    "orderType": "30-Cxx-05"
}

print(create_data)

# import os
# import urllib3
# urllib3.disable_warnings()
#
# os.environ['NO_PROXY'] = 'https://api.etherscan.io/api'
# os.environ['NO_PROXY'] = 'https://www.google.com'
#
#
# user_agent_list = [
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
#     "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
#     ]
#
#
# u = "https://api.etherscan.io/api"
# q = "https://www.baidu.com"
# data = {"module": "account",
#         "action": "balance",
#         "address": "0x47e5188894284c8aaD9e50AcF67E6DCa13cd7AeB",
#         "tag": "latest",
#         "apikey": "A25TEUBY5RJVGMDVADDZBYV5KMMCNRMMN6"}
# header = {
#     "Connection": "close",
#     "User-Agent": random.choice(user_agent_list)
# }
# session = requests.session()
# res = session.post(u, params=data, headers=header, verify=False)
# sleep(0.8)
# print(res.json())

# res2 = requests.post(q)
# print(res2.text)
