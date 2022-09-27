from time import sleep

import requests
from eth_account import Account
import codecs
import os

digits = 32

txtName = "text.txt"
f = open(txtName, "w")
for i in range(1, 1000):
    hex = codecs.encode(os.urandom(digits), 'hex').decode()
    new_context = hex + '\n'
    f.write(new_context)

f.close()

sleep(1)
all_the_text = open('text.txt').read()
new3_list = all_the_text.split("\n")

acount_info = "acount_info.txt"  # 存放地址和秘钥
addr = open(acount_info, "w")

address = "address.txt"  # 存放地址
addre = open(address, "w")
for i in new3_list[:-1]:
    acct = Account.from_key(i)
    acount_info = str(acct.address) + ", " + str(i) + "\n"
    address_info = acct.address + "\n"
    addr.write(acount_info)  # 写入地址和秘钥
    addre.write(address_info)  # 写入地址

addr.close()
addre.close()

u = "https://api.etherscan.io/api"
data = {
    "module": "account",
    "action": "tokenbalance",
    "contractaddress": "0x47e5188894284c8aaD9e50AcF67E6DCa13cd7AeB",
    "address": "0x47e5188894284c8aaD9e50AcF67E6DCa13cd7AeB",
    "tag": "latest",
    "apikey": "NV5EPER64FIAXQRD89IJ3Y1C5GP942ZUR9"
}
