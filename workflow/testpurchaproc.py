"""
普通采购模块流程性用例
登录 -> 采购订单查询商品 -> 选择商品 -> 提交订单 -> 支付订单 -> 采购订单查询详情 -> 未发货关闭商品 -> 退货申请单查询详情
"""
import sys
import pytest
import requests
import yaml
import ruamel.yaml
# from ruamel import yaml
from ruamel.yaml import YAML

from utils.read_yml import readyml
from pathlib import Path
from api.login_funtion import login
from api.gen_purchase import inventory, getgoodsinfobyid

p = Path(__file__)
yamlPath = p.parent.parent.joinpath("testdata", "inventory_model.yml")
inven_data = readyml(yamlPath)  # 获取yaml文件所有内容
inventory_param = readyml(yamlPath)["InventoryModel"]
getgoodsinfobyid_param = readyml(yamlPath)["getgoodsinfobyidmodel"]


# 公共方法，覆盖更新yaml文件里的参数
def updata_yaml(updata_inven):
    with open(yamlPath, "w", encoding="utf-8") as f:
        yaml.dump(updata_inven, f, allow_unicode=True)


@pytest.mark.inventory
@pytest.mark.parametrize("inventory_input, expected", inventory_param)
def test_inventory(inventory_input, base_url, expected):
    s = requests.Session()
    login(s, base_url)
    r = inventory(s, base_url, **inventory_input)

    # 取出所有的invid存放在列表中
    invid_info = []
    for rows_info in r.json()["data"]["rows"]:
        if "001" in rows_info["saleModel"] and rows_info["status"] == "1":
            inv = rows_info["invId"]
            invid_info.append(inv)
    print("inviod_info----", invid_info)

    # 将所有invid都放入yaml文件中
    inven_data["getgoodsinfobyidmodel"][0][0]["InvId"] = invid_info
    print("inven_data-----", inven_data)
    updata_yaml(inven_data)
    print(r.headers)

    print("测试数据:", inventory_input)
    print(r.json())
    assert r.json()["success"] == expected["success"]
    assert r.json()["redirect"] == expected["redirect"]
    assert r.json()["msg"] == expected["msg"]


@pytest.mark.getgoodsinfobyid
@pytest.mark.parametrize("getgoodsinfobyid_model, expected", getgoodsinfobyid_param)
def test_getgoodsinfobyid(login_fixture, base_url, getgoodsinfobyid_model, expected):
    login_s = login_fixture
    print("!!!", getgoodsinfobyid_param)
    a = getgoodsinfobyid(login_s, base_url, invid_info=getgoodsinfobyid_param[0][0]["InvId"])
    print(a.json())
    print(a.headers)
    assert a.json()["success"] == expected["success"]
    assert a.json()["status"] == expected["status"]
