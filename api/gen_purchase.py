import json
import os
import requests
from time import sleep
from requests import Response

# 绕过代理访问，否则挂代理时会报错requests.exceptions.ProxyError代理错误
os.environ["NO_PROXY"] = "dgj-staging.kzmall.cc"


# invid_info = []  # 返回全部invId列表
# invid = ""  # 取出的invId
# skuid = ""  # 取出的invId对应的skuid
# minnum = ""  # 最小起订量
# draft_id = ""  # 采购草稿单id
# order_info = {}  # 商品详情及订单信息
# submitinvpocg_response = {}  # 订单提交详情
# pretradetoken_id = ""  # 订单ID，用于支付


def inventory(s, base_url, *args, **kwargs) -> Response:
    """
    采购订单打开选择商品页面
    :param s: session对象
    :param base_url:配置参数url
    :param kwargs: inventory_data
    :return:
    """
    # global invid_info
    inventory_url = base_url + "/index.php/basedata/inventory"
    inventory_data = {
        "action": "newkzlist",
        "skey": "",
        "mBrand": "",
        "cars": "",
        "models": "",
        "mYear": "",
        "displacement": "",
        "width": 1481.6000000000001,
        "bussType": "PUO",
        "typeNumber": "all",
        "_search": "false",
        "nd": 1655264792823,
        "rows": 20,
        "page": 1,
        "sidx": "number",
        "sord": "desc"
    }
    # inventory_data.update(**kwargs)  # yaml文件传参时，自动更新inventory_data数据
    inventory_response = s.get(url=inventory_url, params=inventory_data)

    # 获取货主为001，状态为正常的商品，然后随机获取其中1个商品的invid
    # for rows_info in inventory_response.json()["data"]["rows"]:
    #     if "001" in rows_info["saleModel"] and rows_info["status"] == "1":
    #         inv = rows_info["invId"]
    #         invid_info.append(inv)  # 取出invid，添加到全局参数列表中

    # print("inventory参数是:", inventory_data)
    # print("------", invid_info)
    # print("inventory接口返回:", inventory_response.json())
    return inventory_response  # invid_info  # 返回所有商品，和商品的值


def getgoodsinfobyid(s, base_url, *args, **kwargs):
    """采购订单选择一个商品"""
    # global invid, skuid, minnum
    getgoodsinfobyid_url = base_url + "/index.php/scm/invPo/getGoodsInfoById"
    getgoodsinfobyid_data = {
        "invId": args  # 随机取出一个invid
    }
    getgoodsinfobyid_response = s.get(url=getgoodsinfobyid_url, params=getgoodsinfobyid_data)
    # print("getgoodsinfobyid_data参数是:", getgoodsinfobyid_data)
    # print("anno_mercha返回的是:", getgoodsinfobyid_response.json())
    # invid = getgoodsinfobyid_data["invId"]  # 取出的invid作为全局变量
    # skuid = getgoodsinfobyid_response.json()["skuId"]  # 取出invid对应的skuid作为全局变量
    # minnum = getgoodsinfobyid_response.json()["minNum"]  # 取出商品最小起订量
    return getgoodsinfobyid_response  # 返回单个商品，和商品的值


def quantitylimitcheck(s, base_url, minnum, *args, **kwargs):
    """采购订单确认订单，顺序调用下列接口"""
    # 提交检查接口，作用未知
    # 上个接口返回速度较慢，使用sleep延长时间
    sleep(1)
    quantitylimitcheck_url = base_url + "/index.php/scm/invPo/quantityLimitCheck"
    # *args返回值是元组，所以需要用下标取值
    quantitylimitcheck_body = [{"invId": args[0], "qty": minnum}]
    quantitylimitcheck_data = {
        "goods": json.dumps(quantitylimitcheck_body)
    }
    quantitylimitcheck_response = s.post(url=quantitylimitcheck_url, data=quantitylimitcheck_data)
    # print("quantitylimitcheck_data参数是:", quantitylimitcheck_data)
    # print("limitcheck返回的是:", quantitylimitcheck_response.json())
    return quantitylimitcheck_response


def format_interface(s, base_url, skuid, minnum, *args, **kwargs) -> Response:
    """格式化接口，作用未知"""
    format_url = base_url + "/index.php/po/Minimum/format"
    format_body = {
        "goodsData": {"skuId": skuid, "shipperCode": "001", "qty": minnum}
    }
    format_response = s.post(url=format_url, data=format_body)
    # print("format返回的是:", format_response.json())
    return format_response


def saveinvpo(s, base_url, invid, skuid, minnum, *args, **kwargs) -> Response:
    """保存草稿接口"""
    # global draft_id
    saveinvpo_url = base_url + "/index.php/scm/invPo/saveInvPo"
    str_info = {
        "action": "saveInvPo"
    }
    saveinvpo_body = {
        "orderType": "30-Cxx-07",
        "locationId": 638,
        "entries": [
            {
                "invId": invid,
                "skuId": skuid,
                "qty": minnum,
                "description": "",
                "itemCode": skuid,
                "shipperCode": "001"
            }],
        "description": ""}
    saveinvpo_data = {"postData": json.dumps(saveinvpo_body)}
    saveinvpo_response = s.post(url=saveinvpo_url, params=str_info, data=saveinvpo_data)
    # draft_id = saveinvpo_response.json()["id"]
    # print("saveinvpo的打印结果是", saveinvpo_response.json())
    return saveinvpo_response


def initpoconfrim(s, base_url, draft_id, *args, **kwargs) -> Response:
    """查询采购草稿单"""
    global order_info
    initpoconfrim_url = base_url + "/index.php/scm/invPo/initPoConfrim_"
    initpoconfrim_data = {"id": draft_id}
    initpoconfrim_response = s.post(url=initpoconfrim_url, data=initpoconfrim_data)

    # 提交订单参数，期货商品/现货商品其中一个详情，以及订单信息
    # order_info = initpoconfrim_response.json()["data"]["list"]["futures"]["order"][0] if \
    #     initpoconfrim_response.json()["data"]["list"]["stocks"]["order"] == [] else \
    #     initpoconfrim_response.json()["data"]["list"]["stocks"]["order"][0]
    # print("查询采购草稿单返回", initpoconfrim_response.json())
    return initpoconfrim_response


def submitinvpocg(s, base_url, order_info, draft_id, *args, **kwargs) -> Response:
    """采购订单提交"""
    # global submitinvpocg_response
    submitinvpocg_url = base_url + "/index.php/scm/invPo/submitInvPoCG"
    submitinvpocg_body = {"action": "submitInvPoCG"}
    submitinvpocg_data = {
        "entries": order_info,
        "orderId": draft_id,
        "cartGoods": ""
    }
    submitinvpocg_response = s.post(url=submitinvpocg_url, params=submitinvpocg_body, data=submitinvpocg_data)
    print("submit_po返回的是", submitinvpocg_response.json())
    return submitinvpocg_response


def getpayinfonew(s, base_url, order_list, *args, **kwargs) -> Response:
    """提交支付页面，获取订单信息"""
    # global pretradetoken_id
    getpayinfonew_url = base_url + "/index.php/scm/invPo/getPayInfoNew"
    getpayinfonew_data = {
        "orders": order_list,
        "subAccountId": ""
    }
    getpayinfonew_responst = s.post(url=getpayinfonew_url, data=getpayinfonew_data)
    # pretradetoken_id = getpayinfonew_responst.json()["data"]["preTradeToken"]
    print("getpayinfonew_responst返回的是:", getpayinfonew_responst.json())
    return getpayinfonew_responst


def nopagepay(s, base_url, pretradetoken_id, *args, **kwargs) -> Response:
    """订单支付"""
    nopagepay_url = base_url + "/index.php/scm/invPo/noPagePay"
    nopagepay_data = {
        "preTradeToken": pretradetoken_id
    }
    nopagepay_response = s.post(url=nopagepay_url, data=nopagepay_data)
    print("nopagepay_response返回的是:", nopagepay_response.json())
    return nopagepay_response


def invpo(s, base_url, typenumber="waitPay", skey=None, *args, **kwargs) -> Response:
    """支付完成后，返回待支付订单查询"""
    invpo_url = base_url + "/index.php/scm/invPo"
    invpo_data = {
        "action": "list",
        "typeNumber": typenumber,
        "sendMode": "",
        "transType": "170401",
        "rows": 50,
        "sord": "asc",
        "skey": skey,
        "sidx": "",
        "page": 1,
        "buId": "",
        "orderType": "",
        "begin_time": "",
        "paymentType": "",
        "buType": "",
        "end_time": "",
        "begin_pay_time": "",
        "end_pay_time": ""
    }
    invpo_response = s.post(url=invpo_url, data=invpo_data)
    print("invpo_response返回的是:", invpo_response.json())
    return invpo_response


# 未发货商品页面
def getinvpoinfo(s, base_url, skey, *args, **kwargs) -> Response:
    """未发货订单根据订单号查询"""
    getinvpoinfo_url = base_url + "/index.php/scm/InvPo/getInvPoInfo"
    getinvpoinfo_data = {
        "skey": skey,
        "category_ids": "",
        "skuStatus": 0,
        "page": 1,
        "rows": 100,
        "waitOut": "true",
        "transType": 170401,
        "status": 5,
        "behivior": "",
        "supply_id": "",
        "beginDate": "",
        "endDate": ""
    }
    print(getinvpoinfo_data)
    getinvpoinfo_response = s.post(url=getinvpoinfo_url, data=getinvpoinfo_data)
    print("getInvPoInfo_response返回的是:", getinvpoinfo_response.json())
    return getinvpoinfo_response


def getinvpoinfoformat(s, base_url, ids, *args, **kwargs) -> Response:
    """未发货商品提交预览"""
    getinvpoinfo_url = base_url + "/index.php/scm/invPo/getInvPoInfoFormat"
    getinvpoinfo_data = {
        "ids": ids
    }
    getinvpoinfo_response = s.post(url=getinvpoinfo_url, data=getinvpoinfo_data)
    print("getinvpoinfo_response返回的是:", getinvpoinfo_response.json())
    return getinvpoinfo_response


def closeinvpo(s, base_url, goodslist, token, *args, **kwargs) -> Response:
    """未发货商品提交关闭"""
    closeinvpo_url = base_url + "/index.php/scm/invPo/closeInvPo"
    # hearder = {"Content-Type": "multipart/form-data"}
    closeinvpo_params = {
        "action": "closeInvPo"
    }
    # closeinvpo_data = {
    #     "goodsList": goodslist,
    #     "token": token
    # }
    closeinvpo_data = {
        "goodsList": json.dumps(goodslist),
        "token": token
    }
    closeinvpo_response = s.post(url=closeinvpo_url, data=closeinvpo_data, params=closeinvpo_params)
    # print(closeinvpo_response.raw())
    print("closeinvpo_data返回的是:", closeinvpo_data)
    print("token返回的是,", token)
    print(s.headers)
    print("closeinvpo_response返回的是:", closeinvpo_response.json())
    return closeinvpo_response


if __name__ == "__main__":
    s = requests.Session()
    from api.login_funtion import login

    base_url = "http://dgj-staging.kzmall.cc"
    login(s, base_url)
    # hearder = {"Content-Type": "multipart/form-data"}
    # s.headers.update(hearder)
    # closeinvpo(s, base_url)
#     inventory(s, base_url)
#     getgoodsinfobyid(s, base_url)
# quantitylimitcheck()
# format_interface()
# saveinvpo()
# initpoconfrim()
# submitinvpocg()
# getpayinfonew()
# nopagepay()
# invpo()
