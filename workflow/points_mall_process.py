"""
积分商城业务流程
"""
import allure
import pytest
from api.gen_purchase import get_goods_info_by_id

from api.points_mall import *


class PointPurchaseGlobalVariable:
    invId = ""
    pass


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

    @allure.title("打开积分商场调用接口3_3")
    @pytest.mark.pointsMall
    def test_points_mall(self, login_fixture, base_url):
        """
        积分商场商品列表
        :param login_fixture:
        :param base_url:
        :return: 商品列表
        """
        n = 0
        pages = 1
        exit_flag = False
        points_mall_response = {}
        while n < 10:
            points_mall_res = points_mall(login_fixture, base_url, page=pages)
            for i in points_mall_res.json()["data"]["rows"]:
                if i["applyStock"]["allowQty"] > 0 and i["status"] == 1:
                    PointPurchaseGlobalVariable.invId = i["invId"]
                    exit_flag = True
                    print(type(points_mall_res))
                    # points_mall_response = points_mall_res
                    break
            n += 1
            pages += 1
            if exit_flag:
                break

        # print("points_mall_response返回的是:", points_mall_response.json())

    # def test_get_goods_info_by_id(self, login_fixture, base_url):
    #     get_goods_info_by_id(login_fixture, base_url)
