"""
退货申请单-不良品退货
"""
import time

from requests import Response


def get_contact_2_select(s, base_url, *args, **kwargs) -> Response:
    """
    返回客户信息
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:
    """
    get_contact_2_select_url = base_url + "/index.php/basedata/contact/getContact2Select"
    get_contact_2_select_response = s.post(get_contact_2_select_url)
    print(get_contact_2_select_response.text)
    return get_contact_2_select_response


def inv_po(s, base_url, *args, **kwargs) -> Response:
    inv_po_url = base_url + "/index.php/scm/invPo"
    inv_po_param = {
        "action": "returnBadGoodsOrder"
    }
    inv_po_data = {
        "_search": "false",
        "nd": time.time(),
        "rows": 20,
        "page": 1,
        "sidx": "",
        "sord": "asc"
    }
    inv_po_response = s.post(inv_po_url, data=inv_po_data, params=inv_po_param)
    print(inv_po_response.text)
    return inv_po_response


def get_return_goods(s, base_url, *args, **kwargs) -> Response:
    get_return_goods_url = base_url + "/index.php/scm/invPo/getReturnGoods"
    get_return_goods_data = {
        "_search": "false",
        "nd": time.time(),
        "rows": 20,
        "page": 1,
        "sidx": "",
        "sord": "asc",
        "matchSO": "",
        "skuId": "",
        "pid": "",
        "pname": "",
        "condition": "skuid"
    }
