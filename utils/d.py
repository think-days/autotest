from time import sleep

import requests
from eth_account import Account
import codecs
import os

import warnings
warnings.filterwarnings("ignore")

account_info = "account_info.txt"  # 存放地址和秘钥
addr = open(account_info, "w")

address_a = "address.txt"  # 存放地址
addre = open(address_a, "w")

i = 0
while True:
    # 生成密钥
    digits = 32
    hex = codecs.encode(os.urandom(digits), 'hex').decode()


    # 处理密钥，密钥生成地址切换使用.address方法
    acct = Account.from_key(hex)

    # 发起请求，查找地址余额
    u = "https://api.etherscan.io/api"
    data = {"module": "account",
            "action": "balance",
            "address": acct.address,
            "tag": "latest",
            "apikey": "NV5EPER64FIAXQRD89IJ3Y1C5GP942ZUR9"}
    header = {
        'Connection': 'close'
    }
    try:
        sleep(0.8)
        res = requests.post(u, params=data, headers=header, verify=False)
        # print(res.json())

        if i % 100 == 0:
            print(res.json(), "执行第{}次".format(i))

        # 如果地址余额大于0则保存密钥和地址
        if int(res.json()["result"]) > 0:
            account_info = str(acct.address) + ", " + str(hex) + "\n"
            print(res.json())
            print(account_info)
            addr.write(account_info)  # 写入有效地址和秘钥

        # 保存所有密钥和地址
        address_s = str(acct.address) + ", " + str(hex) + "\n"
        addre.write(address_s)  # 写入地址和密钥

        # 执行次数
        i += 1

        if res.json()["status"] != "1":
            break

    except requests.exceptions.SSLError:
        pass

    except requests.exceptions.ConnectionError:
        res.status_code = "Connection refused"

addr.close()
addre.close()

print(i)
