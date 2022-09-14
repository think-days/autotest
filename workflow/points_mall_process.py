"""
积分商城业务流程
"""
import random
from time import sleep

import allure
import pytest

from api.gen_purchase import get_goods_info_by_id
from api.public_func import *
from api.points_mall import *
from api.find_po_order import inv_po


class PointPurchaseGlobalVariable:
    invId_list = []  # invId列表
    invId = ""  # 获取invId
    sku_code = ""  # skuId
    rule_code = ""  # 账号code
    points_order_id = ""  # 提交预览ID
    total_num = ""  # 订单数量
    price = ""  # 订单金额
    po_order = ""  # 采购单单号
    pay_token = ""  # 支付token
    location_id = 0  # 仓库id
    ids = []  # 未发货退货订单详情id
    iid = ""  # 未发货退货主表id
    get_inv_po_info_format_token = ""  # 未发货退货订单token，每次发起更换
    get_inv_po_info_response_info = []  # 未发货退货订单详情


@allure.epic("采购模块")
@allure.feature("积分商城采购流程")
class TestPointMall:
    """
    积分商城采购流程性用例
    进入积分商城-选择分类-选择商品-下单预览-提交订单-提交支付-返回待支付订单页
    """

    @allure.title("打开积分商城调用接口3_1")
    @pytest.mark.advertiseIds
    def test_advertise_ids(self, login_fixture, base_url):
        """
        获取广宣品分类
        :param login_fixture:
        :param base_url:
        :return: 广宣品分类
        """
        advertise_ids_response = advertise_ids(login_fixture, base_url)
        print("advertise_ids返回的是:", advertise_ids_response.json())
        assert advertise_ids_response.json()["success"] is True
        assert advertise_ids_response.json()["status"] == "success"
        assert advertise_ids_response.json()["msg"] == "查询成功！"

    @allure.title("打开积分商城调用接口3_2")
    @pytest.mark.getErAccountInfo
    def test_get_er_account_info(self, login_fixture, base_url):
        """
        获取当前积分商城账户明细
        :param login_fixture:
        :param base_url:
        :return:账户积分明细
        """
        get_er_account_info_response = get_er_account_info(login_fixture, base_url)
        print("get_er_account_info_response返回的是:", get_er_account_info_response.json())
        PointPurchaseGlobalVariable.rule_code = get_er_account_info_response.json()["data"]["ruleCode"]
        assert get_er_account_info_response.json()["success"] is True
        assert get_er_account_info_response.json()["status"] == "success"
        assert get_er_account_info_response.json()["msg"] == "查询成功"

    @allure.title("打开积分商场调用接口3_3")
    @pytest.mark.pointsMall
    def test_points_mall(self, login_fixture, base_url):
        """
        积分商场商品列表, 并将商品invId添加到列表中，随机获得一个invId
        :param login_fixture:
        :param base_url:
        :return: 商品列表
        """
        pages = 1
        exit_flag = False
        points_mall_response = {}
        # 返回数据中没有过滤掉供给舱库存为0的商品，所以需要手动过滤；每页不一定有可用数据，所以分十页去循环取值，取到值则结束循环
        while pages < 10:
            points_mall_res = points_mall(login_fixture, base_url, page=pages)
            for i in points_mall_res.json()["data"]["rows"]:
                if i["applyStock"]["allowQty"] > 0 and i["status"] == "1":
                    PointPurchaseGlobalVariable.invId_list.append(i["invId"])
                    exit_flag = True
                    points_mall_response = points_mall_res
                    # break
            pages += 1
            if exit_flag:
                break
        if len(PointPurchaseGlobalVariable.invId_list) == 1:
            PointPurchaseGlobalVariable.invId = PointPurchaseGlobalVariable.invId_list[0]
        else:
            PointPurchaseGlobalVariable.invId = PointPurchaseGlobalVariable.invId_list[
                random.randint(0, len(PointPurchaseGlobalVariable.invId_list))]
        assert points_mall_response.json()["success"] is True
        assert points_mall_response.json()["status"] == "success"
        assert points_mall_response.json()["msg"] == "查询成功！"

        print("points_mall_response返回的是:", points_mall_response.json())

    @allure.title("查询商品")
    @pytest.mark.getGoodsInfoById
    def test_get_goods_info_by_id(self, login_fixture, base_url):
        """
        查询商品，获取最小起订量和skuId
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_goods_info_by_id_res = get_goods_info_by_id(login_fixture, base_url, PointPurchaseGlobalVariable.invId)
        print(get_goods_info_by_id_res.json())
        PointPurchaseGlobalVariable.sku_code = get_goods_info_by_id_res.json()["skuId"]
        assert get_goods_info_by_id_res.json()["success"] is True
        assert get_goods_info_by_id_res.json()["status"] == "success"
        assert get_goods_info_by_id_res.json()["msg"] == "查询成功！"

    @allure.title("订单生成预览")
    @pytest.mark.erOrderDetail
    def test_er_order_confirm(self, login_fixture, base_url):
        """
        订单生成预览,提交订单之前，获取广宣品订单id
        :param login_fixture:
        :param base_url:
        :return:
        """
        er_order_detail_response = er_order_confirm(login_fixture, base_url, PointPurchaseGlobalVariable.invId)
        # sleep(1)
        PointPurchaseGlobalVariable.points_order_id = er_order_detail_response.json()["data"]["id"]
        print(er_order_detail_response.json())
        assert er_order_detail_response.json()["success"] is True
        assert er_order_detail_response.json()["status"] == "success"
        assert er_order_detail_response.json()["msg"] == "操作成功"

    @allure.title("请求仓库信息")
    @pytest.mark.invlocation
    def test_inv_location(self, login_fixture, base_url):
        """
        请求仓库信息
        :param login_fixture:
        :param base_url:
        :return:
        """
        inv_location_response = inv_location(login_fixture, base_url)
        for i in inv_location_response.json()["data"]["storeLocation"][0]["locationList"]:
            if i["number"] == "KZ001":
                PointPurchaseGlobalVariable.location_id = i["id"]
                print(i["id"])
        print(inv_location_response.json())
        assert inv_location_response.json()["success"] is True
        assert inv_location_response.json()["status"] == "success"
        assert inv_location_response.json()["msg"] == "查询成功！"

    @allure.title("订单明细")
    @pytest.mark.erOrderDetail
    def test_er_order_detail(self, login_fixture, base_url):
        """
        订单明细，获取订单数量和金额
        :param login_fixture:
        :param base_url:
        :return:
        """
        er_order_detail_response = er_order_detail(login_fixture, base_url, PointPurchaseGlobalVariable.points_order_id)
        PointPurchaseGlobalVariable.total_num = er_order_detail_response.json()["data"]["totalNum"]
        PointPurchaseGlobalVariable.price = er_order_detail_response.json()["data"]["totalAmount"]
        print(er_order_detail_response.json())
        assert er_order_detail_response.json()["success"] is True
        assert er_order_detail_response.json()["status"] == "success"
        assert er_order_detail_response.json()["msg"] == "操作成功"

    @allure.title("订单提交")
    @pytest.mark.saveEr
    def test_save_er(self, login_fixture, base_url):
        """
        广宣品订单提交，生成采购单，获取采购单号
        :param login_fixture:
        :param base_url:
        :return:
        """
        save_er_response = save_er(login_fixture, base_url, PointPurchaseGlobalVariable.rule_code,
                                   PointPurchaseGlobalVariable.location_id,
                                   PointPurchaseGlobalVariable.invId,
                                   PointPurchaseGlobalVariable.sku_code, PointPurchaseGlobalVariable.total_num,
                                   PointPurchaseGlobalVariable.price)
        PointPurchaseGlobalVariable.po_order = save_er_response.json()["data"]["orderList"]
        print(save_er_response.json())
        assert save_er_response.json()["success"] is True
        assert save_er_response.json()["status"] == "success"
        assert save_er_response.json()["msg"] == "提交成功"

    @allure.title("获取支付明细")
    @pytest.mark.getPayInfo
    def test_get_pay_info(self, login_fixture, base_url):
        """
        获取支付明细，获取token
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_pay_info_response = get_pay_info(login_fixture, base_url, PointPurchaseGlobalVariable.po_order)
        PointPurchaseGlobalVariable.pay_token = get_pay_info_response.json()["token"]
        print(get_pay_info_response.json())
        assert get_pay_info_response.json()["success"] is True
        assert get_pay_info_response.json()["status"] == "success"
        assert get_pay_info_response.json()["msg"] == "查询成功！"

    @allure.title("提交支付")
    @pytest.mark.getQRCodeByActivity
    def test_get_qr_code_by_activity(self, login_fixture, base_url):
        """
        提交支付，返回支付明细
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_qr_code_by_activity_response = get_qr_code_by_activity(login_fixture, base_url,
                                                                   PointPurchaseGlobalVariable.po_order)
        print(get_qr_code_by_activity_response.json())
        assert get_qr_code_by_activity_response.json()["success"] is True
        assert get_qr_code_by_activity_response.json()["status"] == "success"
        assert get_qr_code_by_activity_response.json()["msg"] == ""
        assert get_qr_code_by_activity_response.json()["message"] == "支付成功！"
        assert get_qr_code_by_activity_response.json()["code"] == -100550

    @allure.title("未知查询")
    @pytest.mark.getPayResult
    def test_get_pay_result(self, login_fixture, base_url):
        """
        未知查询
        :param login_fixture:
        :param base_url:
        :return:
        """
        sleep(3)
        get_pay_result_response = get_pay_result(login_fixture, base_url, PointPurchaseGlobalVariable.po_order,
                                                 PointPurchaseGlobalVariable.pay_token)
        print(get_pay_result_response.json())
        assert get_pay_result_response.json()["success"] is True
        assert get_pay_result_response.json()["status"] == "success"
        assert get_pay_result_response.json()["payStatus"] == 1
        assert get_pay_result_response.json()["msg"] == "查询成功！"


@allure.epic("采购模块")
@allure.feature("积分商城订单未发货退货流程")
class TestPointMallOrderClose:

    @allure.title("未发货退货查询")
    @pytest.mark.get_inv_po_info
    def test_get_inv_po_info(self, login_fixture, base_url):
        """
        查询订单状态是否是待出库，每60秒查一次
        :param login_fixture:
        :param base_url:
        :return:
        """
        while True:
            a = inv_po(login_fixture, base_url, typenumber="allStatus", skey=PointPurchaseGlobalVariable.po_order)
            if a.json()["data"]["rows"][0]["billStatus"] == "3":
                break
            else:
                sleep(60)
        get_inv_po_info_response = get_inv_po_info(login_fixture, base_url, PointPurchaseGlobalVariable.po_order)
        print(get_inv_po_info_response.json())

        for i in get_inv_po_info_response.json()["data"]["rows"]:
            PointPurchaseGlobalVariable.ids.append(i["id"])
        PointPurchaseGlobalVariable.iid = get_inv_po_info_response.json()["data"]["rows"][0]["iid"]
        PointPurchaseGlobalVariable.get_inv_po_info_response_info = get_inv_po_info_response.json()["data"]["rows"]

        assert get_inv_po_info_response.json()["msg"] == "查询成功！"
        assert get_inv_po_info_response.json()["status"] == "success"
        assert get_inv_po_info_response.json()["data"]["rows"][0]["billNo"] == PointPurchaseGlobalVariable.po_order[0]

    @allure.title("未发货商品提交预览")
    @pytest.mark.getinvpoinfoformat
    def test_get_inv_po_info_format(self, login_fixture, base_url):
        """
        未发货商品提交预览
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_inv_po_info_format_response = get_inv_po_info_format(login_fixture, base_url,
                                                                 ids=PointPurchaseGlobalVariable.ids)
        print(get_inv_po_info_format_response.json())

        PointPurchaseGlobalVariable.get_inv_po_info_format_token = get_inv_po_info_format_response.json()["data"][
            "token"]

        assert get_inv_po_info_format_response.json()["msg"] == "查询成功！"
        assert get_inv_po_info_format_response.json()["status"] == "success"
        assert get_inv_po_info_format_response.json()["data"]["rows"][0]["billNo"] == \
               PointPurchaseGlobalVariable.po_order[0]

    @allure.title("未发货商品关闭")
    @pytest.mark.closeinvpo
    def test_close_inv_po(self, login_fixture, base_url):
        """
        未发货商品关闭
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_goods_list = []
        for i in PointPurchaseGlobalVariable.get_inv_po_info_response_info:
            n = {"id": i["id"], "iid": i["iid"]}
            get_goods_list.append(n)
        close_inv_po_response = close_inv_po(login_fixture, base_url, goodslist=get_goods_list,
                                             token=PointPurchaseGlobalVariable.get_inv_po_info_format_token)
        print(close_inv_po_response.json())

        assert close_inv_po_response.json()["msg"] == "关闭成功1条采购单!"
        assert close_inv_po_response.json()["status"] == "success"
        assert close_inv_po_response.json()["success"] is True
