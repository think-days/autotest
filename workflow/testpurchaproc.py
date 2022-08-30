"""
普通采购模块流程性用例
登录 -> 采购订单查询商品 -> 选择商品 -> 提交订单 -> 支付订单 -> 采购订单查询详情 -> 未发货关闭商品 -> 退货申请单查询详情
"""
import random

import pytest
import yaml

from utils.read_yml import readyml
from pathlib import Path
from api.login_funtion import login
from api.gen_purchase import *

# p = Path(__file__)
# yamlPath = p.parent.parent.joinpath("testdata", "inventory_model.yml")
# inven_data = readyml(yamlPath)  # 获取yaml文件所有内容
# inventory_param = readyml(yamlPath)["InventoryModel"]
# GetGoodsInFoById_param = readyml(yamlPath)["GetGoodsInFoByIdModel"]
# QuantityLimitCheck_param = readyml(yamlPath)["QuantityLimitCheckModel"]
# Format_Interface_param = readyml(yamlPath)["Format_InterfaceModel"]
# SaveInvpoModel_param = readyml(yamlPath)["SaveInvpoModel"]
# InitPoConFrimModel_param = readyml(yamlPath)["InitPoConFrimModel"]
# SubMitInvPoCgModel_param = readyml(yamlPath)["SubMitInvPoCgModel"]
# GetPayInfoNewModel_param = readyml(yamlPath)["GetPayInfoNewModel"]
# NoPagePayModel_param = readyml(yamlPath)["NoPagePayModel"]
# InvpoModel_param = readyml(yamlPath)["InvpoModel"]

# 全局变量
invid_info = []  # invid_info列表
invid = ""  # 一个invid
skuid = ""  # 一个invid对应的skuid
minnum = ""  # 最小起订量，用于下单数量
draft_id = ""  # 草稿单id
order_info = {}  # 订单明细信息
order_list = {}  # 订单提交详情
pretradetoken_id = ""  # 订单id，用于支付
ids = []  # 未发货退货订单详情id
iid = ""  # 未发货退货主表id
getinvpoinfoformat_token = ""  # 未发货退货订单token，每次发起更换
getinvpoinfo_response_info = []  # 未发货退货订单详情


# 公共方法，覆盖更新yaml文件里的参数
# def updata_yaml(updata_inven):
#     with open(yamlPath, "w", encoding="utf-8") as f:
#         yaml.dump(updata_inven, f, allow_unicode=True)


@pytest.mark.inventory
# @pytest.mark.parametrize("inventory_input, expected", inventory_param)
def test_inventory(login_fixture, base_url):
    global invid_info, invid
    login_s = login_fixture
    r = inventory(login_s, base_url)
    sleep(1)
    print(r.json())

    # 取出所有的invid存放在列表中
    for rows_info in r.json()["data"]["rows"]:
        if "001" in rows_info["saleModel"] and rows_info["status"] == "1":
            inv = rows_info["invId"]
            invid_info.append(inv)
    # 随机取出一个invid
    invid = invid_info[random.randint(0, len(invid_info))]

    assert r.json()["success"] is True
    assert r.json()["redirect"] is None
    assert r.json()["msg"] == "查询成功！"


@pytest.mark.getgoodsinfobyid
# @pytest.mark.parametrize("getgoodsinfobyid_model, expected", GetGoodsInFoById_param)
def test_getgoodsinfobyid(login_fixture, base_url):
    global skuid, minnum
    login_s = login_fixture
    getgoodsinfobyid_response = getgoodsinfobyid(login_s, base_url, invid)

    print(getgoodsinfobyid_response.json())
    skuid = getgoodsinfobyid_response.json()["skuId"]  # 取出invid对应的skuid作为全局变量
    minnum = getgoodsinfobyid_response.json()["minNum"]  # 取出商品最小起订量

    assert getgoodsinfobyid_response.json()["success"] is True
    assert getgoodsinfobyid_response.json()["status"] == "success"


@pytest.mark.quantitylimitcheck
# @pytest.mark.parametrize("QuantityLimitCheckModel, expected", QuantityLimitCheck_param)
def test_quantitylimitcheck(login_fixture, base_url):
    login_s = login_fixture
    quantitylimitcheck_response = quantitylimitcheck(login_s, base_url, minnum, invid)
    print(quantitylimitcheck_response.json())
    assert quantitylimitcheck_response.json()["msg"] == ""
    assert quantitylimitcheck_response.json()["status"] == "success"
    assert quantitylimitcheck_response.json()["success"] is True


@pytest.mark.format_interface
# @pytest.mark.parametrize("Format_InterfaceModel, expected", Format_Interface_param)
def test_format_interface(login_fixture, base_url):
    login_s = login_fixture
    format_interface_response = format_interface(login_s, base_url, skuid, minnum)
    print(format_interface_response.json())
    assert format_interface_response.json()["success"] is True
    assert format_interface_response.json()["status"] == "success"
    assert format_interface_response.json()["msg"] == "查询成功"


@pytest.mark.saveinvpo
# @pytest.mark.parametrize("SaveInvpoModel, expected", SaveInvpoModel_param)
def test_saveinvpo(login_fixture, base_url):
    global draft_id
    login_s = login_fixture
    saveinvpo_respongse = saveinvpo(login_s, base_url, invid, skuid, minnum)

    # 草稿单id
    draft_id = saveinvpo_respongse.json()["id"]
    print(saveinvpo_respongse.json())

    assert saveinvpo_respongse.json()["success"] is True
    assert saveinvpo_respongse.json()["status"] == "success"
    assert saveinvpo_respongse.json()["msg"] == "保存草稿成功！"


@pytest.mark.initpoconfrim
# @pytest.mark.parametrize("InitPoConFrimModel, expected", InitPoConFrimModel_param)
def test_initpoconfrim(login_fixture, base_url):
    global order_info
    login_s = login_fixture
    initpoconfrim_response = initpoconfrim(login_s, base_url, draft_id)

    # 提交订单参数，期货商品/现货商品其中一个详情，以及订单信息
    order_info = initpoconfrim_response.json()["data"]["list"]["futures"]["order"][0] if \
        initpoconfrim_response.json()["data"]["list"]["stocks"]["order"] == [] else \
        initpoconfrim_response.json()["data"]["list"]["stocks"]["order"][0]

    print(initpoconfrim_response.json())
    assert initpoconfrim_response.json()["success"] is True
    assert initpoconfrim_response.json()["status"] == "success"
    assert initpoconfrim_response.json()["msg"] == "查询成功！"


@pytest.mark.submitinvpocg
# @pytest.mark.parametrize("SubMitInvPoCgModel, expected", SubMitInvPoCgModel_param)
def test_submitinvpocg(login_fixture, base_url):
    global order_list
    login_s = login_fixture
    submitinvpocg_response = submitinvpocg(login_s, base_url, order_info, draft_id)
    order_list = submitinvpocg_response.json()["orderList"]
    print(submitinvpocg_response.json())
    assert submitinvpocg_response.json()["success"] is True
    assert submitinvpocg_response.json()["status"] == "success"
    assert submitinvpocg_response.json()["msg"] == "提交订单成功！"


@pytest.mark.getpayinfonew
# @pytest.mark.parametrize("GetPayInfoNewModel, expected", GetPayInfoNewModel_param)
def test_getpayinfonew(login_fixture, base_url):
    global pretradetoken_id
    login_s = login_fixture
    getpayinfonew_response = getpayinfonew(login_s, base_url, order_list)

    print(getpayinfonew_response.json())
    pretradetoken_id = getpayinfonew_response.json()["data"]["preTradeToken"]

    assert getpayinfonew_response.json()["success"] is True
    assert getpayinfonew_response.json()["status"] == "success"
    assert getpayinfonew_response.json()["message"] == "成功"
    assert getpayinfonew_response.json()["code"] == 0


@pytest.mark.nopagepay
# @pytest.mark.parametrize("NoPagePayModel, expected", NoPagePayModel_param)
def test_nopagepay(login_fixture, base_url):
    login_s = login_fixture
    nopagepay_response = nopagepay(login_s, base_url, pretradetoken_id)
    print(nopagepay_response.json())
    assert nopagepay_response.json()["success"] is True
    assert nopagepay_response.json()["status"] == "success"
    assert nopagepay_response.json()["message"] == "成功"
    assert nopagepay_response.json()["code"] == 0


@pytest.mark.invpo
# @pytest.mark.parametrize("InvpoModel, expected", InvpoModel_param)
def test_invpo(login_fixture, base_url):
    login_s = login_fixture
    invpo_response = invpo(login_s, base_url)
    print(invpo_response.json())
    assert invpo_response.json()["success"] is True
    assert invpo_response.json()["status"] == "success"
    assert invpo_response.json()["msg"] == "查询成功！"


@pytest.mark.getinvpoinfo
def test_getinvpoinfo(login_fixture, base_url):
    global ids, iid, getinvpoinfo_response_info
    login_s = login_fixture
    while True:
        a = invpo(login_fixture, base_url=base_url, typenumber="allStatus", skey=order_list[0])
        if a.json()["data"]["rows"][0]["billStatus"] == "3":
            break
        else:
            sleep(120)

    getinvpoinfo_response = getinvpoinfo(login_s, base_url, skey=order_list[0])

    for i in getinvpoinfo_response.json()["data"]["rows"]:
        ids.append(i["id"])
    iid = getinvpoinfo_response.json()["data"]["rows"][0]["iid"]
    getinvpoinfo_response_info = getinvpoinfo_response.json()["data"]["rows"]
    print(ids)
    print(order_list[0])
    print(getinvpoinfo_response.json())

    assert getinvpoinfo_response.json()["msg"] == "查询成功！"
    assert getinvpoinfo_response.json()["status"] == "success"
    assert getinvpoinfo_response.json()["data"]["rows"][0]["billNo"] == order_list[0]


@pytest.mark.getinvpoinfoformat
def test_getinvpoinfoformat(login_fixture, base_url):
    global getinvpoinfoformat_token
    login_s = login_fixture
    getinvpoinfoformat_response = getinvpoinfoformat(login_s, base_url, ids=ids)

    print(getinvpoinfoformat_response.json())
    getinvpoinfoformat_token = getinvpoinfoformat_response.json()["data"]["token"]
    print("getinvpoinfoformat_token返回的是:", getinvpoinfoformat_token)

    assert getinvpoinfoformat_response.json()["msg"] == "查询成功！"
    assert getinvpoinfoformat_response.json()["status"] == "success"
    assert getinvpoinfoformat_response.json()["data"]["rows"][0]["billNo"] == order_list[0]


@pytest.mark.closeinvpo
def test_closeinvpo(login_fixture, base_url):
    print(getinvpoinfo_response_info)
    get_goodslist = []
    for i in getinvpoinfo_response_info:
        n = {"id": i["id"], "iid": i["iid"]}
        get_goodslist.append(n)
    print(get_goodslist)
    login_s = login_fixture
    closeinvpo_response = closeinvpo(login_s, base_url, goodslist=get_goodslist, token=getinvpoinfoformat_token)
    print("closeinvpo_response返回的是:", closeinvpo_response.json())

    assert closeinvpo_response.json()["msg"] == "关闭成功1条采购单!"
    assert closeinvpo_response.json()["status"] == "success"
    assert closeinvpo_response.json()["success"] is True
