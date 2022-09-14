"""
首页接口,公共
"""
import json

from requests import Response


# 首页接口
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


# 未发货商品页面
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
