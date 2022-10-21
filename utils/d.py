import time
from time import sleep

import requests
from eth_account import Account
import codecs
import os

import warnings

warnings.filterwarnings("ignore")
os.environ['NO_PROXY'] = "https://api.etherscan.io/api"

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
    eth_url = "https://api.etherscan.io/api"
    eth_data = {"module": "account",
                "action": "balance",
                "address": acct.address,
                "tag": "latest",
                "apikey": "A25TEUBY5RJVGMDVADDZBYV5KMMCNRMMN6"}
    header = {
        'Connection': 'close'
    }

    bsc_url = "https://api.bscscan.com/api"
    bsc_data = {
        "module": "account",
        "action": "balance",
        "address": acct.address,
        "apikey": "UTIISITYAMIKN2MGBX5D2Z1MYGWKAE9MQU"
    }
    try:
        sleep(0.8)
        eth_res = requests.post(eth_url, params=eth_data, headers=header, verify=False)
        bsc_res = requests.post(bsc_url, params=bsc_data, headers=header, verify=False)
        # print(res.json())

        if i % 100 == 0:
            print(eth_res.json(), "\n", bsc_res.json(), "\n", "执行第{}次".format(i),
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")

        # 如果地址余额大于0则保存密钥和地址
        if int(eth_res.json()["result"]) > 0:
            eth_account_info = "eth: " + str(acct.address) + ", " + str(hex) + "\n"
            print(eth_res.json())
            print(eth_account_info)
            addr.write(eth_account_info)  # 写入有效地址和秘钥

        if int(bsc_res.json()["result"]) > 0:
            bsc_account_info = "eth: " + str(acct.address) + ", " + str(hex) + "\n"
            print(bsc_res.json())
            print(bsc_account_info)
            addr.write(bsc_account_info)  # 写入有效地址和秘钥

        # 保存所有密钥和地址
        eth_bsc_address = str(acct.address) + ", " + str(hex) + "\n"
        addre.write(eth_bsc_address)  # 写入地址和密钥

        # 执行次数
        i += 1

        if eth_res.json()["status"] != "1" or bsc_res.json()["status"] != "1":
            break

    except requests.exceptions.SSLError:
        pass

    except requests.exceptions.ConnectionError:
        pass
        # res.status_code = "Connection refused"
    except requests.exceptions.JSONDecodeError:
        pass

addr.close()
addre.close()
