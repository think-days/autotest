"""
积分商城
"""
import json
from requests import Response


def advertise_ids(s, base_url, *args, **kwargs) -> Response:
    """
    获取广宣品分类
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:广宣品分类
    """
    advertise_ids_url = base_url + "/index.php/basedata/inventory/advertiseIds"
    advertise_ids_response = s.post(url=advertise_ids_url)
    return advertise_ids_response


def get_er_account_info(s, base_url, *args, **kwargs) -> Response:
    """
    获取当前积分商城账号明细
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:账号明细：可用金额，账号状态等
    """
    get_er_account_url = base_url + "/index.php/scm/receipt/getErAccountInfo"
    get_er_account_response = s.post(url=get_er_account_url)
    return get_er_account_response


def points_mall(s, base_url, page=1) -> Response:
    """
    积分商城商品列表
    :param s:
    :param base_url:
    :return:商品列表
    """
    points_mall_url = base_url + "/index.php/basedata/inventory/pointsMall"
    points_mall_data = {
        "skey": "",
        "firstCategory": "",
        "secondCategory": "",
        "page": page,
        "rows": 20
    }
    points_mall_response = s.post(url=points_mall_url, data=points_mall_data)
    return points_mall_response


# get_goods_info_by_id():

def er_order_confirm(s, base_url, inv_id, num=1, *args, **kwargs) -> Response:
    """
    广宣品订单预览
    :param s:
    :param base_url:
    :param inv_id:
    :param num:订货批量
    :return:生成订单
    """
    er_order_confirm_url = base_url + "/index.php/scm/invPo/erOrderConfirm"
    er_order_confirm_data = {
        "postData": json.dumps([{"invId": inv_id, "num": num}])
    }
    er_order_confirm_response = s.post(url=er_order_confirm_url, data=er_order_confirm_data)
    return er_order_confirm_response


# get_er_account_info()

def er_order_detail(s, base_url, er_id, *args, **kwargs) -> Response:
    """
    查询广宣品订单
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:订单明细
    """
    er_order_detail_url = base_url + "/index.php/scm/invPo/erOrderDetail"
    er_order_detail_data = {
        "id": er_id
    }
    er_order_detail_response = s.post(url=er_order_detail_url, data=er_order_detail_data)
    return er_order_detail_response


def save_er(s, base_url, rulecode, location_id, invid, skucode, qty, price, *args, **kwargs) -> Response:
    """
    广宣品提交订单,生成采购订单
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:采购订单
    """
    save_er_url = base_url + "/index.php/scm/invPo/saveEr"
    save_er_data = {
        "postData": json.dumps({
            "payerCode": "001",
            "ruleCode": rulecode,
            "accountId": 15,
            "locationId": location_id,
            "entries": [{
                "invId": invid,
                "skuCode": skucode,
                "qty": qty,
                "price": price
            }]
        })
    }
    save_er_response = s.post(url=save_er_url, data=save_er_data)
    return save_er_response


def get_pay_info(s, base_url, orders, *args, **kwargs) -> Response:
    """
    获取支付信息
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:支付明细
    """
    get_pay_info_url = base_url + "/index.php/scm/invPo/getPayInfo"
    get_pay_info_data = {
        "orders": orders,
        "subAccountId": ""
    }
    get_pay_info_response = s.post(url=get_pay_info_url, data=get_pay_info_data)
    return get_pay_info_response


def get_qr_code_by_activity(s, base_url, source_order_id, *args, **kwargs) -> Response:
    """
    提交支付
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:支付返回消息
    """
    get_qr_code_by_activity_url = base_url + "/index.php/scm/invPo/getQRCodeByActivity"
    get_qr_code_by_activity_data = {
        "sourceOrderId": source_order_id
    }
    get_qr_code_by_activity_response = s.post(url=get_qr_code_by_activity_url, data=get_qr_code_by_activity_data)
    return get_qr_code_by_activity_response


def get_pay_result(s, base_url, orders, token, *args, **kwargs) -> Response:
    """
    查询该订单
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:查询状态
    """
    get_pay_result_url = base_url + "/index.php/scm/invPo/getPayResult"
    get_pay_result_data = {
        "orders": orders,
        "icbcPayChannel": 12,
        "token": token
    }
    get_pay_result_response = s.post(url=get_pay_result_url, data=get_pay_result_data)
    return get_pay_result_response

# inv_po()


# if __name__ == '__main__':
#     from api.login_funtion import login
#
#     s = requests.Session()
#     base_url = "http://dgj-staging.kzmall.cc"
#     login(s, base_url)
#
#     advertise_ids(s, base_url)
#     get_er_account_info(s, base_url)
