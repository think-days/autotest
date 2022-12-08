"""
采购模块
普通活动采购
"""
import requests
from requests import Response


def get_activity_list_new(s: requests.Session, base_url, title_type=None, order_group=None, act_type=None,
                          brand_id=None, category_id=None, sorc_way=None, skey=None) -> requests.Response:
    """
    活动中心活动列表
    :param s:
    :param base_url:
    :param skey:查询关键字
    :param sorc_way:排序，发布时间：creatTime；开始时间：startTime；结束时间：expiryTime
    :param category_id:分类ID
    :param brand_id:品牌ID
    :param act_type:活动类型，折扣：discount；赠品：gift；一口价：fixed；预订单：preorder；拼团：preorderGroup
    :param order_group:订单分类，长期促销活动：ACT_LONG；月度促销活动：ACT_MONTH；厂家直发单：ACT_DIRECT
    :param title_type:活动阶段
    :return:
    """
    get_activity_list_new_url = base_url + "/index.php/scm/invPre/get_actList_new"
    get_activity_list_new_data = {
        "page": 1,
        "rows": 10,
        "titleType": title_type,
        "orderGroup": order_group,
        "actType": act_type,
        "brandId": brand_id,
        "categoryId": category_id,
        "sorcWay": sorc_way,
        "skey": skey
    }
    get_activity_list_new_response = s.post(get_activity_list_new_url, get_activity_list_new_data)
    print(get_activity_list_new_response.text)
    return get_activity_list_new_response


def get_activity_info(s: requests.Session, base_url, activity_id) -> requests.Response:
    """
    获取活动详情
    :param s:
    :param base_url:
    :param activity_id:活动ID
    :return:
    """
    get_activity_info_url = base_url + "/index.php/scm/invPre/activity_data"
    get_activity_info_data = {
        "id": activity_id
    }
    get_activity_info_response = s.post(get_activity_info_url, get_activity_info_data, activity_id)
    print(get_activity_info_response.text)
    return get_activity_info_response
