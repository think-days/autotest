# 不良品退货流程
import heapq
import random
import re
import allure
import pytest
from api.defective_product_return import *
from api.public_func import get_contact_2_select


class DefectiveGlobalVariable:
    contact_info = ""
    order_goods_info = {}
    get_order_goods_info = {}


@allure.epic("采购模块")
@allure.title("不良品退货流程")
class TestDefectiveProductReturn:
    """
    不良品退货流程性用例
    打开不良品品页面-选择商品-上传图片-创建草稿单-提交订单-退货申请单查询取消不良品品退货
    """

    @allure.title("获取客户资料")
    @pytest.mark.DefectiveGetContact2Select
    def test_defective_get_contact_2_select(self, login_fixture, base_url):
        """
        获取客户资料，用于提交不良品退货
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_contact_2_select_res = get_contact_2_select(login_fixture, base_url)
        print(get_contact_2_select_res.text)
        DefectiveGlobalVariable.contact_info = \
            get_contact_2_select_res.json()["data"][random.randint(0, len(get_contact_2_select_res.json()["data"]))][
                "id"]
        assert get_contact_2_select_res.json()["success"] is True
        assert get_contact_2_select_res.json()["status"] == "success"
        assert get_contact_2_select_res.json()["msg"] == "查询成功！"

    @allure.title("打开不良品退货页面")
    @pytest.mark.DefectiveinvPo
    def test_inv_po(self, login_fixture, base_url):
        """
        打开不良品退货页面，返回HTML
        :param login_fixture:
        :param base_url:
        :return:
        """
        inv_po_res = inv_po(login_fixture, base_url)
        print(inv_po_res.text)
        assert re.findall("<title>(.+?)</title>", inv_po_res.text) == ['快准车服-站管家']
        assert re.findall("<label>(.+?)</label>", inv_po_res.text) == ['退货类型:', '单据日期:', '单据编号:']
        assert re.findall('<span class="fs12">(.+?)</span>', inv_po_res.text) == ['不良品退货', '采购订单号']

    @allure.title("获取可退货商品列表")
    @pytest.mark.getReturnGoods
    def test_get_return_goods(self, login_fixture, base_url):
        """
        查询可用的不良品退货物料，并选取其中一条
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_return_goods_res = get_return_goods(login_fixture, base_url)
        # 从返回的字典中取出一条入库数量大于锁定数量最多的物料
        get_goods = []
        for i in get_return_goods_res.json()["data"]["rows"]:
            if i["locationId"] == "638" and i["status"] == "1" and i["inQty"] > i["lockNum"] and i["isGift"] == "否":
                get_goods.append(i)
        DefectiveGlobalVariable.order_goods_info = heapq.nlargest(1, get_goods, key=lambda s: s["inQty"] - s["lockNum"])
        print(get_return_goods_res.text)
        assert get_return_goods_res.json()["data"]["page"] == 1
        assert get_return_goods_res.json()["data"]["rows"] is not None

    @allure.title("选择商品")
    @pytest.mark.getReturnGoodsForSoCode
    def test_get_return_goods_for_so_code(self, login_fixture, base_url):
        print(DefectiveGlobalVariable.order_goods_info)
        get_return_goods_for_so_code_res = get_return_goods_for_so_code(login_fixture, base_url,
                                                                        DefectiveGlobalVariable.order_goods_info[0][
                                                                            "id"])
        print("-------", get_return_goods_for_so_code_res.text)
        assert get_return_goods_for_so_code_res.json()["unitId"] == DefectiveGlobalVariable.order_goods_info[0]["invId"]
        assert get_return_goods_for_so_code_res.json()["srcOrderId"] == DefectiveGlobalVariable.order_goods_info[0][
            "iid"]
        print("--------", DefectiveGlobalVariable.order_goods_info)
        assert get_return_goods_for_so_code_res.json()["lockNum"] == DefectiveGlobalVariable.order_goods_info[0][
            "lockNum"]

    @allure.title("提交预览不良品退货")
    @pytest.mark.getReturnGoodsForSoCodeAgain
    def test_get_return_goods_for_so_code_again(self, login_fixture, base_url):
        get_return_goods_for_so_code_again_res = get_return_goods_for_so_code_again(
            login_fixture, base_url, DefectiveGlobalVariable.order_goods_info[0]["id"])
        DefectiveGlobalVariable.get_order_goods_info = get_return_goods_for_so_code_again_res.json()
        print(get_return_goods_for_so_code_again_res.text)
        assert get_return_goods_for_so_code_again_res.json()["unitId"] == DefectiveGlobalVariable.order_goods_info[0][
            "invId"]
        assert get_return_goods_for_so_code_again_res.json()["srcOrderId"] == \
               DefectiveGlobalVariable.order_goods_info[0]["iid"]
        assert get_return_goods_for_so_code_again_res.json()["lockNum"] == DefectiveGlobalVariable.order_goods_info[0][
            "lockNum"]

    @allure.title("创建不良品退货订单")
    @pytest.mark.after_sale_create
    def test_after_sale_create(self, login_fixture, base_url):
        """
        创建不良品退货订单，普通订单正常提交。
        物料是蓄电池：上传蓄电池所需要的额外参数。
        物料是轮胎：上传轮胎所需要的额外参数。
        :param login_fixture:
        :param base_url:
        :return:
        """
        # 本地图片和视频路径,仅在本地环境使用，更换环境则更换图片路径
        pictures_video = [
            "C:\\Users\\lumia\\Pictures\\9e39916b5c2b07d00c5900a481bd6146e3ee5811.jpg",
            "C:\\Users\\lumia\\Pictures\\0121952da2d96a4e1b8dd1ae6fb7b636.jpg",
            "C:\\Users\\lumia\\Pictures\\lALPD26eL7xLjdvNAfDNBNo_1242_496.jpg",
            "C:\\Users\\lumia\\Pictures\\20200507_115152.mp4"
        ]

        after_sale_create_res = after_sale_create(
                            s=login_fixture,
                            base_url=base_url,
                            description="原因",
                            so_code_id=DefectiveGlobalVariable.order_goods_info[0]["id"],
                            src_order_id=DefectiveGlobalVariable.order_goods_info[0]["iid"],
                            contact_id=DefectiveGlobalVariable.contact_info,
                            install_car_model="安装车型",
                            install_time=time.strftime("%Y-%m-%d", time.gmtime()),
                            install_mileage="100",
                            need_extra_voucher=DefectiveGlobalVariable.get_order_goods_info["needExtraVoucher"],
                            need_video=DefectiveGlobalVariable.get_order_goods_info["needVideo"],
                            pictures=pictures_video)
        print(after_sale_create_res.text)
        assert after_sale_create_res.json()["success"] is True
        assert after_sale_create_res.json()["status"] == "success"
        assert after_sale_create_res.json()["msg"] == "保存草稿成功！"
