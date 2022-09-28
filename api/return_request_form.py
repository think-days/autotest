"""
退货申请单
"""
from requests import Response


def first_return_open(s, base_url, *args, **kwargs) -> Response:
    """
    打开退货申请单
    :param s:
    :param base_url:
    :return:
    """
    first_return_open_url = base_url + "/index.php/po/AfterSale/firstReturnOpen"
    first_return_open_response = s.post(first_return_open_url)
    return first_return_open_response


def get_return_quota(s, base_url, *args, **kwargs) -> Response:
    """
    打开滞销品退货
    :param s:
    :param base_url:
    :return:
    """
    get_return_quota_url = base_url + "/index.php/po/AfterSale/getReturnQuota"
    get_return_quota_response = s.post(get_return_quota_url)
    return get_return_quota_response


def assist(s, base_url, *args, **kwargs) -> Response:
    """
    查询商品品类
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:
    """
    assist_url = base_url + "/index.php/basedata/assist"
    assist_data = {
        "action": "kzlist",
        "typeNumber": "trade",
        "isDelete": 2
    }
    assist_response = s.post(assist_url, params=assist_data)
    return assist_response


# inventory()

def get_goods_for_return_list(s, base_url, inv_id, bu_id="203755", *args, **kwargs) -> Response:
    """
    返回物料明细
    :param s:
    :param base_url:
    :param inv_id: 物料列表
    :param bu_id: 货主主键ID
    :param args:
    :param kwargs:
    :return:
    """
    get_goods_for_return_list_url = base_url + "/index.php/basedata/Inventory/getGoodsForReturnList"
    get_goods_for_return_list_data = {
        "invIds": inv_id,
        "buId": bu_id,
        "returnType": "30-Cxx-05"
    }
    get_goods_for_return_list_response = s.post(get_goods_for_return_list_url, data=get_goods_for_return_list_data)
    return get_goods_for_return_list_response


def create_draft(s, base_url, goods_area, *args, **kwargs) -> Response:
    """
    创建滞销品退货草稿单
    :param goods_area: 字典，返回所有仓库和货位
    :param s:
    :param base_url:
    :return:
    """
    create_url = base_url + "/index.php/po/AfterSale/create"
    e = []
    for i, k in dict.items(goods_area):
        for n, f in dict.items(k):
            b = {"invId": i, "rtNum": "1", "locationId": n, "locationAreaId": f[0]["id"]}
            e.append(b)
    create_data = {
        "buId": 203755,
        "description": "",
        "entries": e,
        "orderType": "30-Cxx-05"
    }
    create_response = s.post(create_url, json=create_data)
    return create_response


def get_split_order_back_info(s, base_url, order_id, *args, **kwargs) -> Response:
    """
    滞销品退货草稿单创建完成后查询该草稿单
    :param s:
    :param base_url:
    :param order_id:草稿单ID，来自create_draft
    :param args:
    :param kwargs:
    :return:
    """
    get_split_order_back_info_url = base_url + "/index.php/scm/invPo/getSplitOrderBackInfo"
    get_split_order_back_info_data = {
        "orderId": order_id
    }
    get_split_order_back_info_response = s.post(get_split_order_back_info_url, data=get_split_order_back_info_data)
    return get_split_order_back_info_response


def submit_draft(s, base_url, order_id, *args, **kwargs) -> Response:
    """
    滞销品退货提交订单
    :param s:
    :param base_url:
    :param order_id: 草稿单ID，来自create_draft
    :return:
    """
    submit_url = base_url + "/index.php/po/AfterSale/submit"
    submit_data = {
        "id": order_id
    }
    submit_response = s.post(submit_url, data=submit_data)
    return submit_response


# 关闭滞销品退货订单
# after_sale_list()
# cancel_draft()
# after_sale_list()
