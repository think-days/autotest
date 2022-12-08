"""
退货申请单
少发退货流程
"""
import heapq
import re

import allure
import jsonpath
import pytest

from api.purchase_returns_func.ZC_return_list import *


class CzReturnListGlobalVariable:
    get_goods_list_info = {}
    order_info = {}


@allure.epic("采购模块-退货流程")
@allure.feature("少发退货流程性用例")
class TestCzReturnList:
    """
    少发退货流程性用例
    打开少发退货页面-查询商品-生成草稿单-提价草稿单-校验订单-取消订单-校验订单
    """

    @allure.title("进入直采退货页面")
    @pytest.mark.zcinvPo
    def test_inv_po_zc_return(self, login_fixture, base_url):
        """
        进入直采退货页面，返回HTML
        :param login_fixture:
        :param base_url:
        :return:
        """
        inv_po_zc_return_res = inv_po_zc_return(login_fixture, base_url)
        print(inv_po_zc_return_res.text)
        assert re.findall("<span>(.+?)</span>", inv_po_zc_return_res.text)[0] == "直采退货"
        assert re.findall("<title>(.+?)</title>", inv_po_zc_return_res.text)[0] == "快准车服-站管家"

    @allure.title("查询可用物料")
    @pytest.mark.zcgetReturnGoods
    def test_zc_get_return_goods(self, login_fixture, base_url):
        """
        查询直采退货中可用物料
        :param login_fixture:
        :param base_url:
        :return:
        """
        zc_get_return_goods_res = zc_get_return_goods(login_fixture, base_url)
        # 获取仓库id
        zc_inv_location_res = inv_location(login_fixture, base_url)
        location_id = jsonpath.jsonpath(zc_inv_location_res.json(), '$...locationList[?(@.number=="KZ001")].id')
        # 根据条件获取一个物料
        goods_info = []
        for i in zc_get_return_goods_res.json()["data"]["rows"]:
            if i["status"] == "1" and i["locationId"] == location_id[0] and i["inQty"] > i["lockNum"] and i["isGift"] == "否":
                goods_info.append(i)
        CzReturnListGlobalVariable.get_goods_list_info = heapq.nlargest(1, goods_info,
                                                                        key=lambda s: s["inQty"] - s["lockNum"])
        print(zc_get_return_goods_res.json())
        assert zc_get_return_goods_res.json()["data"]["rows"] is not None
        assert zc_get_return_goods_res.json()["data"]["records"] >= "1"

    @allure.title("创建草稿单")
    @pytest.mark.zccreate
    def test_zc_create_return_goods_order(self, login_fixture, base_url):
        """
        创建直采退货草稿单,并取出草稿单ID
        :param login_fixture:
        :param base_url:
        :return:
        """
        zc_create_return_goods_order_res = zc_create_return_goods_order(login_fixture, base_url,
                                                                        CzReturnListGlobalVariable.get_goods_list_info)
        CzReturnListGlobalVariable.order_info = zc_create_return_goods_order_res.json()
        print(zc_create_return_goods_order_res.json())
        assert zc_create_return_goods_order_res.json()["success"] is True
        assert zc_create_return_goods_order_res.json()["status"] == "success"
        assert zc_create_return_goods_order_res.json()["msg"] == "保存草稿成功！"
        assert zc_create_return_goods_order_res.json()["data"] is not None

    @allure.title("查询直采退货草稿单")
    @pytest.mark.zcgetSplitOrderBackInfo
    def test_zc_get_split_order_back_info(self, login_fixture, base_url):
        """
        查询直采退货草稿单
        :param login_fixture:
        :param base_url:
        :return:
        """
        zc_get_split_order_back_info_res = zc_get_split_order_back_info(login_fixture, base_url,
                                                                        CzReturnListGlobalVariable.order_info["data"][
                                                                            "order_id"])
        print(zc_get_split_order_back_info_res.json())
        assert zc_get_split_order_back_info_res.json()["success"] is True
        assert zc_get_split_order_back_info_res.json()["status"] == "success"
        assert zc_get_split_order_back_info_res.json()["msg"] == "查询成功！"
        assert zc_get_split_order_back_info_res.json()["data"] is not None

    @allure.title("提交草稿单")
    @pytest.mark.zcsubmit
    def test_zc_submit_draft(self, login_fixture, base_url):
        """
        提交直采退货草稿单
        :param login_fixture:
        :param base_url:
        :return:
        """
        zc_submit_draft_res = zc_submit_draft(login_fixture, base_url,
                                              CzReturnListGlobalVariable.order_info["data"]["order_id"])
        print(zc_submit_draft_res.json())
        assert zc_submit_draft_res.json()["success"] is True
        assert zc_submit_draft_res.json()["status"] == "success"
        assert zc_submit_draft_res.json()["msg"] == "提交订单成功"

    @allure.title("查询提交订单")
    @pytest.mark.zclist
    def test_zc_after_sale_list(self, login_fixture, base_url):
        """
        售后申请单查询列表，并校验订单状态
        :param login_fixture:
        :param base_url:
        :return:
        """
        zc_after_sale_list_res = zc_after_sale_list(login_fixture, base_url)
        print(zc_after_sale_list_res.json())
        assert zc_after_sale_list_res.json()["success"] is True
        assert zc_after_sale_list_res.json()["status"] == "success"
        assert zc_after_sale_list_res.json()["msg"] == "查询成功"
        assert str(CzReturnListGlobalVariable.order_info["data"]["order_id"]) in json.dumps(
            zc_after_sale_list_res.json())
        assert jsonpath.jsonpath(zc_after_sale_list_res.json(), "$..list[?(@.billNo=='{}')].billStatus".format(
            CzReturnListGlobalVariable.order_info["data"]["bill_no"]))[0] == 1

    @allure.title("取消订单")
    @pytest.mark.zccancel
    def test_zc_cancel_draft(self, login_fixture, base_url):
        """
        取消直采退货订单
        :param login_fixture:
        :param base_url:
        :return:
        """
        zc_cancel_draft_res = zc_cancel_draft(login_fixture, base_url,
                                              CzReturnListGlobalVariable.order_info["data"]["order_id"])
        print(zc_cancel_draft_res.json())
        assert zc_cancel_draft_res.json()["success"] is True
        assert zc_cancel_draft_res.json()["status"] == "success"
        assert zc_cancel_draft_res.json()["msg"] == "取消订单成功"

    @allure.title("查询订单")
    @pytest.mark.zclistagain
    def test_zc_after_sale_list_again(self, login_fixture, base_url):
        """
        售后订单查询列表，并校验订单状态
        :param login_fixture:
        :param base_url:
        :return:
        """
        zc_after_sale_list_again_res = zc_after_sale_list_again(login_fixture, base_url)
        print(zc_after_sale_list_again_res.json())
        assert zc_after_sale_list_again_res.json()["success"] is True
        assert zc_after_sale_list_again_res.json()["status"] == "success"
        assert zc_after_sale_list_again_res.json()["msg"] == "查询成功"
        assert str(CzReturnListGlobalVariable.order_info["data"]["order_id"]) in json.dumps(
            zc_after_sale_list_again_res.json())
        assert jsonpath.jsonpath(zc_after_sale_list_again_res.json(), "$..list[?(@.billNo=='{}')].billStatus".format(
            CzReturnListGlobalVariable.order_info["data"]["bill_no"]))[0] == 9
