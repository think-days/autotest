"""
首页接口,公共
"""
from requests import Response


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
