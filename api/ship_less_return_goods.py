"""
退货申请单
少发退货
"""
import time

from requests import Response


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
    print(inv_po_less_return_list_response.text)
    return inv_po_less_return_list_response


def get_return_goods_type_one(s, base_url, po_order=None, sku_id=None, product_code=None, product_name=None, *args,
                              **kwargs) -> Response:
    """
    查询少发退货中可用数据
    :param s:
    :param base_url:
    :param base_url:
    :param po_order:采购订单号,str
    :param sku_id:物料编码,str
    :param product_code:产品码,str
    :param product_name:物料名称,str
    :param args:
    :param kwargs:
    :return:
    """
    get_return_goods_type_one_url = base_url + "/index.php/scm/invPo/getReturnGoods"
    get_return_goods_type_one_param = {
        "action": "getReturnGoods",
        "type": 1
    }
    get_return_goods_type_one_data = {
        "_search": "false",
        "nd": time.time(),
        "rows": 20,
        "page": 1,
        "sidx": "",
        "sord": "asc",
        "matchSO": po_order,
        "skuId": sku_id,
        "pid": product_code,
        "pname": product_name,
        "condition": "skuid"
    }
    get_return_goods_type_one_response = s.post(get_return_goods_type_one_url, data=get_return_goods_type_one_data,
                                                params=get_return_goods_type_one_param)
    print(get_return_goods_type_one_response.text)
    return get_return_goods_type_one_response

    def
