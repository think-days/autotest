from requests import Response


def inv_po(s, base_url, typenumber="waitPay", skey=None, *args, **kwargs) -> Response:
    """
    查询未支付采购订单
    :param s:
    :param base_url:
    :param typenumber: 订单状态
    :param skey:订单号
    :param args:
    :param kwargs:
    :return:
    """
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
    return invpo_response
