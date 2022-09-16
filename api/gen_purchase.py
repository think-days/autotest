"""
普通采购模块
采购订单
"""
import json
import os
from time import sleep

import requests
from requests import Response

# 绕过代理访问，否则挂代理时会报错requests.exceptions.ProxyError代理错误
os.environ["NO_PROXY"] = "dgj-staging.kzmall.cc"


def inventory(s, base_url, buss_type, *args, **kwargs) -> Response:
    """
    采购订单打开选择商品页面
    :param s: session对象
    :param base_url:配置参数url
    :param kwargs: inventory_data
    :return:
    """
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
        "bussType": buss_type,
        "typeNumber": "all",
        "_search": "false",
        "nd": 1655264792823,
        "rows": 20,
        "page": 1,
        "sidx": "number",
        "sord": "desc",
        **kwargs
    }
    inventory_response = s.get(url=inventory_url, params=inventory_data)
    return inventory_response  # invid_info  # 返回所有商品，和商品的值


def get_goods_info_by_id(s, base_url, *args, **kwargs) -> Response:
    """采购订单选择一个商品"""
    getgoodsinfobyid_url = base_url + "/index.php/scm/invPo/getGoodsInfoById"
    getgoodsinfobyid_data = {
        "invId": args  # 随机取出一个invid
    }
    getgoodsinfobyid_response = s.get(url=getgoodsinfobyid_url, params=getgoodsinfobyid_data)
    return getgoodsinfobyid_response  # 返回单个商品，和商品的值


def quantity_limit_check(s, base_url, minnum, *args, **kwargs) -> Response:
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
    return quantitylimitcheck_response


def format_interface(s, base_url, skuid, minnum, *args, **kwargs) -> Response:
    """格式化接口，作用未知"""
    format_url = base_url + "/index.php/po/Minimum/format"
    format_body = {
        "goodsData": {"skuId": skuid, "shipperCode": "001", "qty": minnum}
    }
    format_response = s.post(url=format_url, data=format_body)
    return format_response


def save_inv_po(s, base_url, locationid, invid, skuid, minnum, *args, **kwargs) -> Response:
    """保存草稿接口"""
    # global draft_id
    saveinvpo_url = base_url + "/index.php/scm/invPo/saveInvPo"
    str_info = {
        "action": "saveInvPo"
    }
    saveinvpo_body = {
        "orderType": "30-Cxx-07",
        "locationId": locationid,
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
    return saveinvpo_response


def init_po_conf_rim(s, base_url, draft_id, *args, **kwargs) -> Response:
    """查询采购草稿单"""
    initpoconfrim_url = base_url + "/index.php/scm/invPo/initPoConfrim_"
    initpoconfrim_data = {"id": draft_id}
    initpoconfrim_response = s.post(url=initpoconfrim_url, data=initpoconfrim_data)
    return initpoconfrim_response


def submit_inv_po_cg(s, base_url, order_info, draft_id, *args, **kwargs) -> Response:
    """采购订单提交"""
    submitinvpocg_url = base_url + "/index.php/scm/invPo/submitInvPoCG"
    submitinvpocg_body = {"action": "submitInvPoCG"}
    submitinvpocg_data = {
        "entries": order_info,
        "orderId": draft_id,
        "cartGoods": ""
    }
    submitinvpocg_response = s.post(url=submitinvpocg_url, params=submitinvpocg_body, data=submitinvpocg_data)
    return submitinvpocg_response


def get_pay_info_new(s, base_url, order_list, *args, **kwargs) -> Response:
    """提交支付页面，获取订单信息"""
    getpayinfonew_url = base_url + "/index.php/scm/invPo/getPayInfoNew"
    getpayinfonew_data = {
        "orders": order_list,
        "subAccountId": ""
    }
    getpayinfonew_responst = s.post(url=getpayinfonew_url, data=getpayinfonew_data)
    return getpayinfonew_responst


def no_page_pay(s, base_url, pretradetoken_id, *args, **kwargs) -> Response:
    """订单支付"""
    nopagepay_url = base_url + "/index.php/scm/invPo/noPagePay"
    nopagepay_data = {
        "preTradeToken": pretradetoken_id
    }
    nopagepay_response = s.post(url=nopagepay_url, data=nopagepay_data)
    return nopagepay_response
