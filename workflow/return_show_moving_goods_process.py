"""
滞销品退货流程
"""
import heapq

import allure
import pytest

from api.gen_purchase import inventory
from api.return_request_form import *


class ReturnGlobalVariable:
    inv_id_info = []


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

    def test_assist(self, login_fixture, base_url):
        """
        查询商品品类
        :param login_fixture:
        :param base_url:
        :return:
        """
        assist_response = assist(login_fixture, base_url)
        print(assist_response.json())

    def test_inventory(self, login_fixture, base_url):
        """
        查询物料，获取物料明细
        :param login_fixture:
        :param base_url:
        :return:
        """
        inventory_response = inventory(login_fixture, base_url, buss_type="PUORT", unsalable=1)
        ReturnGlobalVariable.inv_id_info = heapq.nlargest(10, inventory_response.json()["data"]["rows"],
                                                          key=lambda s: s['fineQty'])
        print(inventory_response.text)

    def test_get_goods_for_return_list(self, login_fixture, base_url):
        """
        获取三条inv_id
        :param login_fixture:
        :param base_url:
        :return:
        """
        inv_id_list = [i["invId"] for i in ReturnGlobalVariable.inv_id_info]
        get_goods_for_return_list_response = get_goods_for_return_list(login_fixture, base_url)
        print(get_goods_for_return_list_response.text)

    def test_create_draft(self, login_fixture, base_url):
        create_draft_response = create_draft(login_fixture, base_url)

