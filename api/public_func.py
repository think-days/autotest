"""
公共接口
"""
import json

from requests import Response


# 首页接口（inv_location）
def inv_location(s, base_url, *args, **kwargs) -> Response:
    """
    获取仓库信息
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:仓库明细
    """
    inv_location_url = base_url + "/index.php/basedata/invlocation"
    inv_location_data = {
        "action": "list",
        "isDelete": 2
    }
    inv_location_response = s.get(url=inv_location_url, params=inv_location_data)
    print(inv_location_response.json())
    return inv_location_response


# 未发货商品页面（get_inv_po_info，get_inv_po_info_format，close_inv_po）
def get_inv_po_info(s, base_url, skey, *args, **kwargs) -> Response:
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
    getinvpoinfo_response = s.post(url=getinvpoinfo_url, data=getinvpoinfo_data)
    return getinvpoinfo_response


def get_inv_po_info_format(s, base_url, ids, *args, **kwargs) -> Response:
    """未发货商品提交预览"""
    getinvpoinfo_url = base_url + "/index.php/scm/invPo/getInvPoInfoFormat"
    getinvpoinfo_data = {
        "ids": ids
    }
    getinvpoinfo_response = s.post(url=getinvpoinfo_url, data=getinvpoinfo_data)
    return getinvpoinfo_response


def close_inv_po(s, base_url, goodslist, token, *args, **kwargs) -> Response:
    """未发货商品提交关闭"""
    closeinvpo_url = base_url + "/index.php/scm/invPo/closeInvPo"
    closeinvpo_params = {
        "action": "closeInvPo"
    }
    closeinvpo_data = {
        "goodsList": json.dumps(goodslist),
        "token": token
    }
    closeinvpo_response = s.post(url=closeinvpo_url, data=closeinvpo_data, params=closeinvpo_params)
    return closeinvpo_response


# 退货申请单列表（return_order_list）
def return_order_list(s, base_url, key_words=None, bill_status=None, order_type=None, *args, **kwargs) -> Response:
    """
    售后申请单查询
    :param s:
    :param base_url:
    :param key_words:售后订单号
    :param bill_status:售后订单状态
    :param order_type:售后订单类型
    :param args:
    :param kwargs:
    :return:
    """
    return_order_list_url = base_url + "/index.php/po/AfterSale/list"
    return_order_list_data = {
        "page": 1,
        "limit": 20,
        "keywords": key_words,
        "billStatus": bill_status,
        "orderType": order_type
    }
    return_order_list_response = s.post(return_order_list_url, data=return_order_list_data)
    print(return_order_list_response.json())
    return return_order_list_response


def cancel_draft(s, base_url, id_s) -> Response:
    cancel_draft_url = base_url + "/index.php/po/AfterSale/cancel"
    cancel_draft_data = {
        "id": id_s
    }
    cancel_draft_response = s.post(cancel_draft_url, data=cancel_draft_data)
    print(cancel_draft_response.json())
    return cancel_draft_response

