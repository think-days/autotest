"""
退货申请单
直采退货申请单
"""
import time

from requests import Response

from api.public_func import *


def inv_po_zc_return(s, base_url, *args, **kwargs) -> Response:
    """
    进入直采退货页面，返回html
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:
    """
    inv_po_zc_return_url = base_url + "/index.php/scm/invPo"
    inv_po_zc_return_params = {
        "action": "ZcReturnList"
    }
    inv_po_zc_return_data = {
        "_search": "false",
        "nd": time.time(),
        "rows": 20,
        "page": 1,
        "sidx": "",
        "sord": "asc"
    }
    inv_po_zc_return_response = s.post(url=inv_po_zc_return_url, data=inv_po_zc_return_data,
                                       params=inv_po_zc_return_params)
    return inv_po_zc_return_response


def zc_get_return_goods(s, base_url, *args, **kwargs) -> Response:
    """
    查询可用的直采退货申请单中的物料
    :param s:
    :param base_url:
    :param args:
    :param kwargs: 退货类型
    :return:
    """
    zc_get_return_goods_response = get_return_goods(s, base_url, *args, isZC=1)
    return zc_get_return_goods_response


def zc_create_return_goods_order(s, base_url, e_dic, *args, **kwargs) -> Response:
    """
    创建直采退货草稿单
    :param s:
    :param base_url:
    :param e_dic:
    :param args:
    :param kwargs:
    :return:
    """
    e = []
    for i in e_dic:
        b = {"srcOrderEntryId": i["id"], "srcOrderId": i["iid"], "rtNum": "1"}
        e.append(b)
    zc_create_return_goods_order_data = {
        "entries": e,
        "description": "",
        "orderType": "30-Cxx-16"
    }
    create_return_goods_order_response = create_return_goods_order(s, base_url, zc_create_return_goods_order_data)
    return create_return_goods_order_response


def zc_get_split_order_back_info(s, base_url, zc_draft_order_id, *args, **kwargs) -> Response:
    """
    查询直采退货草稿单
    :param s:
    :param base_url:
    :param zc_draft_order_id: 直采退货草稿单ID
    :param args:
    :param kwargs:
    :return:
    """
    zc_get_split_order_back_info_response = get_split_order_back_info(s, base_url, zc_draft_order_id)
    return zc_get_split_order_back_info_response


def zc_submit_draft(s, base_url, zc_draft_order_id, *args, **kwargs) -> Response:
    """
    提交直采退货草稿单
    :param s:
    :param base_url:
    :param zc_draft_order_id: 直采退货草稿单ID
    :param args:
    :param kwargs:
    :return:
    """
    zc_submit_draft_response = submit_draft(s, base_url, zc_draft_order_id)
    return zc_submit_draft_response


def zc_after_sale_list(s, base_url, *args, **kwargs) -> Response:
    """
    售后申请单列表
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:
    """
    zc_after_sale_list_response = after_sale_list(s, base_url)
    return zc_after_sale_list_response


def zc_cancel_draft(s, base_url, zc_draft_order_id, *args, **kwargs) -> Response:
    """
    取消直采退货售后单
    :param s:
    :param base_url:
    :param zc_draft_order_id: 草稿单ID
    :param args:
    :param kwargs:
    :return:
    """
    zc_cancel_draft_response = cancel_draft(s, base_url, zc_draft_order_id)
    return zc_cancel_draft_response


def zc_after_sale_list_again(s, base_url, *args, **kwargs) -> Response:
    """
    售后申请单列表
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:
    """
    zc_after_sale_list_again_response = after_sale_list(s, base_url)
    return zc_after_sale_list_again_response
