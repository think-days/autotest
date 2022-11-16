"""
退货申请单
少发退货流程
"""
import heapq
import json
import re

import allure
import jsonpath
import pytest

from api.public_func import inv_location, after_sale_list, cancel_draft
from api.ship_less_return_goods import *


class ShipLessGlobalVariable:
    ship_less_goods_info = {}
    ship_less_order_id = ""
    ship_less_after_order_info = {}


class TestShipLessReturnGoods:
    """
    少发退货流程性用例
    打开少发退货页面-选择商品-生成草稿单-提交订单-查询该少发退货订单，取消该少发退货订单
    """

    @allure.title("打开少发退货页面")
    @pytest.mark.LessReturnList
    def test_inv_po_less_return_list(self, login_fixture, base_url):
        """
        少发退货页面，返回HTML
        :param login_fixture:
        :param base_url:
        :return:
        """
        inv_po_less_return_list_res = inv_po_less_return_list(login_fixture, base_url)
        print(inv_po_less_return_list_res.text)
        assert re.findall("<span>(.+?)</span>", inv_po_less_return_list_res.text) == ['少发退货']
        assert re.findall("<label>(.+?)</label>", inv_po_less_return_list_res.text) == ['退货类型:', '单据日期:', '单据编号:']

    @allure.title("查询少发退货可用物料")
    @pytest.mark.getReturnGoods
    def test_get_return_goods_type_one(self, login_fixture, base_url):
        """
        查询少发退货可用物料，并取出二个仓库ID为KZ001，采购单号相同，入库数量大于锁定数量的物料
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_return_goods_type_one_res = get_return_goods_type_one(login_fixture, base_url)
        get_inv_location = jsonpath.jsonpath(inv_location(login_fixture, base_url).json(),
                                             '$...locationList[?(@.number=="KZ001")].id')
        get_goods = []
        for i in get_return_goods_type_one_res.json()["data"]["rows"]:
            if i["status"] == "1" and i["locationId"] == get_inv_location[0] and i["inQty"] > i["lockNum"] and i[
                    "isGift"] == "否":
                get_goods.append(i)
        ShipLessGlobalVariable.ship_less_goods_info = heapq.nlargest(2, get_goods,
                                                                     key=lambda s: s["iid"] == s["iid"] and s["inQty"] -
                                                                     s["lockNum"])
        print(get_return_goods_type_one_res.text)
        print(ShipLessGlobalVariable.ship_less_goods_info)
        assert get_return_goods_type_one_res.json()["data"]["records"] >= "1"
        assert get_return_goods_type_one_res.json()["data"]["rows"] is not None

    @allure.title("创建少发退货草稿单")
    @pytest.mark.ship_less_create
    def test_ship_less_create(self, login_fixture, base_url):
        """
        创建少发退货草稿单，取出草稿单ID
        :param login_fixture:
        :param base_url:
        :return:
        """
        ship_less_create_res = ship_less_create(login_fixture, base_url, ShipLessGlobalVariable.ship_less_goods_info)
        ShipLessGlobalVariable.ship_less_order_id = ship_less_create_res.json()["data"]["order_id"]
        ShipLessGlobalVariable.ship_less_after_order_info = ship_less_create_res.json()
        print(ship_less_create_res.text)
        assert ship_less_create_res.json()["success"] is True
        assert ship_less_create_res.json()["status"] == "success"
        assert ship_less_create_res.json()["msg"] == "保存草稿成功！"
        assert ship_less_create_res.json() is not None

    @allure.title("查询少发退货草稿单")
    @pytest.mark.ship_less_getSplitOrderBackInfo
    def test_ship_less_get_split_order_back_info(self, login_fixture, base_url):
        """
        查询少发退货草稿单
        :param login_fixture:
        :param base_url:
        :return:
        """
        ship_less_get_split_order_back_info_res = ship_less_get_split_order_back_info(login_fixture, base_url,
                                                                                      ShipLessGlobalVariable.ship_less_order_id)
        print(ship_less_get_split_order_back_info_res.text)
        assert ship_less_get_split_order_back_info_res.json()["success"] is True
        assert ship_less_get_split_order_back_info_res.json()["status"] == "success"
        assert ship_less_get_split_order_back_info_res.json()["msg"] == "查询成功！"

    @allure.title("提交少发退货订单")
    @pytest.mark.ship_less_submit
    def test_ship_less_submit_draft(self, login_fixture, base_url):
        """
        提交少发退货订单
        :param login_fixture:
        :param base_url:
        :return:
        """
        ship_less_submit_draft_res = ship_less_submit_draft(login_fixture, base_url,
                                                            ShipLessGlobalVariable.ship_less_order_id)
        print(ship_less_submit_draft_res.text)
        assert ship_less_submit_draft_res.json()["success"] is True
        assert ship_less_submit_draft_res.json()["status"] == "success"
        assert ship_less_submit_draft_res.json()["msg"] == "提交订单成功"

    @allure.title("售后申请单查询")
    @pytest.mark.ship_less_list
    def test_ship_less_after_sale_list(self, login_fixture, base_url):
        """
        售后申请单查询列表
        :param login_fixture:
        :param base_url:
        :return:
        """
        ship_less_after_sale_list_res = after_sale_list(login_fixture, base_url)
        print(ship_less_after_sale_list_res.text)
        assert ship_less_after_sale_list_res.json()["success"] is True
        assert ship_less_after_sale_list_res.json()["status"] == "success"
        assert ship_less_after_sale_list_res.json()["msg"] == "查询成功"
        assert ShipLessGlobalVariable.ship_less_after_order_info["data"]["bill_no"] in json.dumps(
            ship_less_after_sale_list_res.json())
        assert jsonpath.jsonpath(ship_less_after_sale_list_res.json(), "$..list[?(@.billNo=='{}')].billStatus".format(
            ShipLessGlobalVariable.ship_less_after_order_info["data"]["bill_no"]))[0] == 1

    @allure.title("取消少发退货售后订单")
    @pytest.mark.ship_less_cancel
    def test_ship_less_cancel_draft(self, login_fixture, base_url):
        """
        取消少发退货售后订单
        :param login_fixture:
        :param base_url:
        :return:
        """
        ship_less_cancel_draft_res = cancel_draft(login_fixture, base_url, ShipLessGlobalVariable.ship_less_order_id)
        print(ship_less_cancel_draft_res.text)
        assert ship_less_cancel_draft_res.json()["success"] is True
        assert ship_less_cancel_draft_res.json()["status"] == "success"
        assert ship_less_cancel_draft_res.json()["msg"] == "取消订单成功"

    def test_ship_less_after_sale_list_again(self, login_fixture, base_url):
        ship_less_after_sale_list_again_res = after_sale_list(login_fixture, base_url)
        print(ship_less_after_sale_list_again_res.text)
        assert ship_less_after_sale_list_again_res.json()["success"] is True
        assert ship_less_after_sale_list_again_res.json()["status"] == "success"
        assert ship_less_after_sale_list_again_res.json()["msg"] == "查询成功"
        assert jsonpath.jsonpath(ship_less_after_sale_list_again_res.json(),
                                 "$..list[?(@.billNo=='{}')].billStatus".format(
                                     ShipLessGlobalVariable.ship_less_after_order_info["data"]["bill_no"]))[0] == 9
