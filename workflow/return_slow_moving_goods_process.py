"""
滞销品退货流程
"""
import heapq
from time import sleep

import allure
import pytest
from jsonpath import jsonpath

from api.gen_purchase import inventory
from api.public_func import *
from api.return_of_slow_moving_goods import *


class ReturnGlobalVariable:
    inv_id_info = []  # 10个物料明细
    goods_list = {}  # 物料仓库、库存明细
    get_inv_id_list = []  # inv_id列表
    get_location_id = ""  # 仓库id
    goods_area = {}  # 商品货位
    draft_id = ""  # 滞销品退货草稿单ID
    draft_number = ""  # 滞销品退货订单号
    draft_info = {}  # 售后订单详情


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
        assert first_return_open_response.json()["success"] is True
        assert first_return_open_response.json()["status"] == "success"
        assert first_return_open_response.json()["msg"] == "查询成功！"

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
        assert get_return_quota_response.json()["success"] is True
        assert get_return_quota_response.json()["status"] == "success"
        assert get_return_quota_response.json()["data"] is not None

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
        assert assist_response.json()["status"] == 200
        assert assist_response.json()["msg"] == "success"
        assert assist_response.json()["data"]["items"] is not None

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
        assert inventory_response.json()["success"] is True
        assert inventory_response.json()["status"] == "success"
        assert inventory_response.json()["msg"] == "查询成功！"
        assert inventory_response.json()["data"] is not None

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
        assert get_goods_for_return_list_response.json()["success"] is True
        assert get_goods_for_return_list_response.json()["status"] == "success"
        assert get_goods_for_return_list_response.json()["msg"] == "查询成功！"
        assert get_goods_for_return_list_response.json()["data"] is not None

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
        assert ReturnGlobalVariable.goods_area is not None

    @allure.title("创建滞销品退货草稿单")
    @pytest.mark.create
    def test_create_draft(self, login_fixture, base_url):
        """
        创建滞销品退货草稿单，提取草稿单ID和草稿单单号
        :param login_fixture:
        :param base_url:
        :return:
        """
        create_draft_response = create_draft(login_fixture, base_url, ReturnGlobalVariable.goods_area)
        ReturnGlobalVariable.draft_id = create_draft_response.json()["data"]["order_id"]
        ReturnGlobalVariable.draft_number = create_draft_response.json()["data"]["bill_no"]
        print(create_draft_response.text)
        assert create_draft_response.json()["success"] is True
        assert create_draft_response.json()["status"] == "success"
        assert create_draft_response.json()["msg"] == "保存草稿成功！"

    @allure.title("拆分订单返回信息")
    @pytest.mark.getSplitOrderBackInfo
    def test_get_split_order_back_info(self, login_fixture, base_url):
        """
        创建草稿单完成后，自动请求草稿单详情
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_split_order_back_info_response = get_split_order_back_info(login_fixture, base_url,
                                                                       ReturnGlobalVariable.draft_id)
        print(get_split_order_back_info_response.text)
        assert get_split_order_back_info_response.json()["success"] is True
        assert get_split_order_back_info_response.json()["status"] == "success"
        assert get_split_order_back_info_response.json()["msg"] == "查询成功！"
        assert get_split_order_back_info_response.json()["data"]["data"][0][
                   "billNo"] == ReturnGlobalVariable.draft_number

    @allure.title("提交草稿单")
    @pytest.mark.submit
    def test_submit_draft(self, login_fixture, base_url):
        submit_draft_response = submit_draft(login_fixture, base_url, ReturnGlobalVariable.draft_id)
        print(submit_draft_response.text)
        assert submit_draft_response.json()["success"] is True
        assert submit_draft_response.json()["status"] == "success"
        assert submit_draft_response.json()["msg"] == "提交订单成功"

    @allure.title("售后申请单列表")
    @pytest.mark.list
    def test_after_sale_list(self, login_fixture, base_url):
        """
        提交售后单后自动返回售后申请单列表
        :param login_fixture:
        :param base_url:
        :return:
        """
        sleep(1)
        after_sale_list_response = after_sale_list(login_fixture, base_url, bill_status="")
        for i in after_sale_list_response.json()["data"]["list"]:
            if i["billNo"] == ReturnGlobalVariable.draft_number:
                ReturnGlobalVariable.draft_info.update(i)
        print(after_sale_list_response.text)
        assert after_sale_list_response.json()["success"] is True
        assert after_sale_list_response.json()["status"] == "success"
        assert after_sale_list_response.json()["msg"] == "查询成功"
        assert ReturnGlobalVariable.draft_number in json.dumps(after_sale_list_response.json())

    @allure.title("取消售后申请单")
    @pytest.mark.cancel
    def test_cancel_draft(self, login_fixture, base_url):
        cancel_draft_response = cancel_draft(login_fixture, base_url, ReturnGlobalVariable.draft_id)
        print(cancel_draft_response.text)
        assert cancel_draft_response.json()["success"] is True
        assert cancel_draft_response.json()["status"] == "success"
        assert cancel_draft_response.json()["msg"] == "取消订单成功"

    @allure.title("售后申请单列表_2")
    @pytest.mark.list_again
    def test_after_sale_list_again(self, login_fixture, base_url):
        """
        取消售后申请单后自动返回售后申请单列表
        :param login_fixture:
        :param base_url:
        :return:
        """
        after_sale_list_again_response = after_sale_list(login_fixture, base_url, bill_status="")
        print(after_sale_list_again_response.text)
        assert after_sale_list_again_response.json()["success"] is True
        assert after_sale_list_again_response.json()["status"] == "success"
        assert after_sale_list_again_response.json()["msg"] == "查询成功"
        assert ReturnGlobalVariable.draft_number in json.dumps(after_sale_list_again_response.json())
        assert jsonpath(after_sale_list_again_response.json(), "$..list[?(@.billNo=='{}')].billStatus".format(ReturnGlobalVariable.draft_number))[0] == 9
        assert jsonpath(after_sale_list_again_response.json(), "$..list[?(@.billNo=='{}')].billStatusName".format(ReturnGlobalVariable.draft_number))[0] == "已关闭"
