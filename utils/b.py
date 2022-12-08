import datetime
import os

import numpy as np
import time
import requests

os.environ["NO_PROXY"] = "https://api.huobi.com"

# huobi_base_url = "https://api.huobi.pro"
# huobi_base_url = "https://api.huobi.fm"
# huobi_base_url = "https://api.huobi.af"
huobi_base_url = "https://api.btcgateway.pro"
okex_base_url = "https://www.okex.com"


# okex_base_url = "https://www.okex.win"


def TD(klinedata):
    close_np = [i["close"] for i in klinedata]  # 收盘时间
    close_shift = np.empty_like(close_np)
    close_shift[:4] = 0
    close_shift[4:] = close_np[:-4]
    compare_array = close_np > close_shift
    result = np.empty(len(close_np), int)
    counting_number: int = 0
    for i in range(len(close_np)):
        if np.isnan(close_shift[i]):
            result[i] = 0
        else:
            compare_bool = compare_array[i]
            if compare_bool:
                if counting_number >= 0:
                    counting_number += 1
                else:
                    counting_number = 1
            else:
                if counting_number <= 0:
                    counting_number -= 1
                else:
                    counting_number = -1
            result[i] = counting_number
    return result[-5:]  # 校验数据，取最后5条K线对应的td值


# 获取火币现货k线数据
def get_klinedata(exchange, symbol, period):
    if exchange == "huobi":
        path = "/linear-swap-ex/market/history/kline"
        params = {
            "contract_code": symbol.replace("_", "-"),
            "period": period,
            "from": int(time.mktime((datetime.datetime.now() + datetime.timedelta(days=-10)).timetuple())),
            "to": int(time.time())
        }
        res = requests.get(huobi_base_url + path, params=params)
        kline_data = []
        for i in res.json()["data"][::-1]:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i["id"]))
            i["time_str"] = time_str
            kline_data.append(i)
        return kline_data


if __name__ == '__main__':
    symbol_list = ['BTC_USDT', 'eos_usdt', 'eth_usdt', 'bch_usdt', 'ht_usdt', 'link_usdt', 'atom_usdt', 'yfi_usdt',
                   'xrp_usdt', 'dot_usdt', 'ltc_usdt', 'bsv_usdt', 'ada_usdt', 'trx_usdt', 'xtz_usdt', 'neo_usdt',
                   'xlm_usdt', 'xmr_usdt', 'xem_usdt', 'dash_usdt', 'doge_usdt', 'etc_usdt', 'iota_usdt', 'vet_usdt',
                   'zec_usdt', 'omg_usdt', 'uni_usdt', 'fil_usdt', 'yfii_usdt', 'skl_usdt', 'sushi_usdt']
    for symbol in symbol_list:
        klinedata = get_klinedata("huobi", symbol, "4hour")
        res = TD(klinedata)
        print(symbol, res)
        time.sleep(1)
