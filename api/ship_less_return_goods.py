"""
退货申请单
少发退货
"""
import time

from requests import Response

from api.public_func import create_return_goods_order, get_split_order_back_info, submit_draft, get_return_goods


def inv_po_less_return_list(s, base_url, *args, **kwargs) -> Response:
    """
    打开少发退货页面，返回html
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:
    """
    inv_po_less_return_list_url = base_url + "/index.php/scm/invPo"
    inv_po_less_return_list_param = {
        "action": "LessReturnList"
    }
    inv_po_less_return_list_data = {
        "_search": "false",
        "nd": time.time(),
        "rows": 20,
        "page": 1,
        "sidx": "",
        "sord": "asc"
    }
    inv_po_less_return_list_response = s.post(inv_po_less_return_list_url, data=inv_po_less_return_list_data,
                                              params=inv_po_less_return_list_param)
    return inv_po_less_return_list_response


def ship_less_get_return_goods(s, base_url, *args, **kwargs) -> Response:
    """
    查询可用的少发退货物料
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:
    """
    ship_less_get_return_goods_res = get_return_goods(s, base_url, *args, **kwargs)
    return ship_less_get_return_goods_res


def ship_less_create(s, base_url, e_dic, *args, **kwargs) -> Response:
    """
    创建少发退货草稿单
    :param s:
    :param base_url:
    :param e_dic:全量返回物料数据，来自上个接口
    :param args:
    :param kwargs:
    :return:
    """
    e = []
    for i in e_dic:
        b = {"srcOrderEntryId": i["id"], "srcOrderId": i["iid"], "rtNum": "1"}
        e.append(b)

    create_return_goods_order_data = {
        "entries": e,
        "description": "",
        "orderType": "30-Cxx-04"
    }
    create_return_goods_order_response = create_return_goods_order(s, base_url, create_return_goods_order_data)
    return create_return_goods_order_response


def ship_less_get_split_order_back_info(s, base_url, draft_id, *args, **kwargs) -> Response:
    """
    查询少发退货草稿单
    :param s:
    :param base_url:
    :param draft_id: 少发退货草稿单ID
    :param args:
    :param kwargs:
    :return:
    """
    ship_less_get_split_order_back_info_response = get_split_order_back_info(s, base_url, draft_id)
    return ship_less_get_split_order_back_info_response


def ship_less_submit_draft(s, base_url, draft_id, *args, **kwargs) -> Response:
    """
    提交少发退货订单
    :param s:
    :param base_url:
    :param draft_id:少发退货草稿单ID
    :param args:
    :param kwargs:
    :return:
    """
    ship_less_submit_draft_response = submit_draft(s, base_url, draft_id)
    return ship_less_submit_draft_response

# after_sale_list()
# cancel_draft()
# after_sale_list()
