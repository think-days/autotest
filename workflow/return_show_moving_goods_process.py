"""
滞销品退货流程
"""
import heapq

import allure
import pytest

from api.gen_purchase import inventory
from api.public_func import get_goods_by_storage_and_area_info
from api.return_request_form import *


class ReturnGlobalVariable:
    inv_id_info = []  # 10个物料明细
    goods_list = {}  # 物料仓库、库存明细
    get_inv_id_list = []  # inv_id列表
    get_location_id = ""  # 仓库id
    goods_area = {}  # 商品货位


@allure.epic("采购模块")
@allure.feature("滞销品退货流程")
class TestReturnOfSlowMovingGoods:
    """
    滞销品退货流程性用例
    打开滞销品页面-选择商品-创建草稿单-提交订单-退货申请单查询取消滞销品退货
    """

    @allure.title("打开退货申请单")
    @pytest.mark.firstReturnOpen
    def test_first_return_open(self, login_fixture, base_url):
        """
        打开退货申请单页面
        :param login_fixture:
        :param base_url:
        :return:
        """
        first_return_open_response = first_return_open(login_fixture, base_url)
        print(first_return_open_response.json())

    @allure.title("打开滞销品退货")
    @pytest.mark.getReturnQuota
    def test_get_return_quota(self, login_fixture, base_url):
        """
        打开滞销品退货
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_return_quota_response = get_return_quota(login_fixture, base_url)
        print(get_return_quota_response.json())

    @allure.title("查询商品品类")
    @pytest.mark.assist
    def test_assist(self, login_fixture, base_url):
        """
        查询商品品类
        :param login_fixture:
        :param base_url:
        :return:
        """
        assist_response = assist(login_fixture, base_url)
        print(assist_response.json())

    @allure.title("打开选择商品页面")
    @pytest.mark.inventory
    def test_inventory(self, login_fixture, base_url):
        """
        查询物料，获取10条物料明细
        :param login_fixture:
        :param base_url:
        :return:
        """
        inventory_response = inventory(login_fixture, base_url, buss_type="PUORT", unsalable=1)
        ReturnGlobalVariable.inv_id_info = heapq.nlargest(10, inventory_response.json()["data"]["rows"],
                                                          key=lambda s: s['fineQty'])
        print(inventory_response.text)

    @allure.title("返回物料仓库货位明细")
    @pytest.mark.getGoodsForReturnList
    def test_get_goods_for_return_list(self, login_fixture, base_url):
        """
        获取三条inv_id
        :param login_fixture:
        :param base_url:
        :return:
        """
        # 取出上个接口返回的10条inv_id
        inv_id_list = ",".join([i["invId"] for i in ReturnGlobalVariable.inv_id_info])
        # 本条用例接口
        get_goods_for_return_list_response = get_goods_for_return_list(login_fixture, base_url, inv_id_list)
        # 取出inv_id
        for i in get_goods_for_return_list_response.json()["data"]["goods"]:
            # 用inv_id取出对应的仓库明细
            for n in get_goods_for_return_list_response.json()["data"]["storage"][i]:
                # 取仓库明细条件
                if n["locationNo"] == "KZ001" and n["locationQty"] > 620:
                    # 赋值仓库id，len为1
                    ReturnGlobalVariable.get_location_id = n["locationId"]
                    # 返回符合条件的inv_id
                    ReturnGlobalVariable.get_inv_id_list.append(i)

        print(get_goods_for_return_list_response.text)

    @allure.title("获取物料下的仓库、货位明细")
    @pytest.mark.getGoodsByStorageAndAreaInfo
    def test_get_goods_by_storage_and_area_info(self, login_fixture, base_url):
        """
        获取每个物料下的仓库、货位明明细
        :param login_fixture:
        :param base_url:
        :return:
        """
        for i in ReturnGlobalVariable.get_inv_id_list:
            get_goods_by_storage_and_area_info_response = get_goods_by_storage_and_area_info(
                login_fixture, base_url, inv_ids=i, location_id=ReturnGlobalVariable.get_location_id)
            ReturnGlobalVariable.goods_area.update(get_goods_by_storage_and_area_info_response.json()["data"]["rows"])
        print(ReturnGlobalVariable.goods_area)

    def test_create_draft(self, login_fixture, base_url):
        create_draft_response = create_draft(login_fixture, base_url)
