from eth_account import Account


hex = "8888888888888888888888888888888888888888888888888888888888888888"
acct = Account.from_key(hex)
print(acct.address)
