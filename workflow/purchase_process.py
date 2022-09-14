"""
普通采购业务流程
"""
import random
import allure
import pytest
from api.gen_purchase import *
from api.public_func import *
from api.find_po_order import inv_po


class PurchaseGlobalVariable:
    # 类变量
    invid_info = []  # invId_info列表
    invid = ""  # 一个invId
    skuid = ""  # 一个invId对应的skuId
    minnum = ""  # 最小起订量，用于下单数量
    location_id = ""  # 仓库ID
    draft_id = ""  # 草稿单id
    order_info = {}  # 订单明细信息
    order_list = {}  # 订单提交详情
    pretradetoken_id = ""  # 订单id，用于支付
    ids = []  # 未发货退货订单详情id
    iid = ""  # 未发货退货主表id
    getinvpoinfoformat_token = ""  # 未发货退货订单token，每次发起更换
    getinvpoinfo_response_info = []  # 未发货退货订单详情


@allure.epic("采购模块")
@allure.feature("普通采购流程")
class TestGeneralPurchase:
    """
    普通采购模块流程性用例
    登录 -> 采购订单查询商品 -> 选择商品 -> 提交订单 -> 支付订单 -> 采购订单查询详情 -> 未发货关闭商品 -> 退货申请单查询详情
    """

    @allure.title("打开选择商品")
    @pytest.mark.inventory
    def test_inventory(self, login_fixture, base_url):
        """
        打开采购订单，点击表单，点击表单中的选择，并从第一页商品列表中随机选择一个invId
        :param login_fixture:
        :param base_url:
        :return:
        """
        inventory_response = inventory(login_fixture, base_url)
        print(inventory_response.json())
        sleep(1)

        # 取出所有的invid存放在列表中
        for rows_info in inventory_response.json()["data"]["rows"]:
            if "001" in rows_info["saleModel"] and rows_info["status"] == "1":
                inv = rows_info["invId"]
                PurchaseGlobalVariable.invid_info.append(inv)
        # 随机取出一个invid
        PurchaseGlobalVariable.invid = PurchaseGlobalVariable.invid_info[
            random.randint(0, len(PurchaseGlobalVariable.invid_info))]

        assert inventory_response.json()["success"] is True
        assert inventory_response.json()["redirect"] is None
        assert inventory_response.json()["msg"] == "查询成功！"

    @allure.title("选择商品")
    @pytest.mark.getgoodsinfobyid
    def test_getgoodsinfobyid(self, login_fixture, base_url):
        """
        取出invId对应的skuId、最小起订量
        :param login_fixture:
        :param base_url:
        :return:
        """
        getgoodsinfobyid_response = get_goods_info_by_id(login_fixture, base_url, PurchaseGlobalVariable.invid)
        print(getgoodsinfobyid_response.json())

        PurchaseGlobalVariable.skuid = getgoodsinfobyid_response.json()["skuId"]  # 取出invid对应的skuid作为全局变量
        PurchaseGlobalVariable.minnum = getgoodsinfobyid_response.json()["minNum"]  # 取出商品最小起订量

        assert getgoodsinfobyid_response.json()["success"] is True
        assert getgoodsinfobyid_response.json()["status"] == "success"

    @allure.title("采购订单确认页面")
    @pytest.mark.quantitylimitcheck
    def test_quantitylimitcheck(self, login_fixture, base_url):
        """
        采购订单提交预览页面
        :param login_fixture:
        :param base_url:
        :return:
        """
        quantitylimitcheck_response = quantity_limit_check(login_fixture, base_url, PurchaseGlobalVariable.minnum,
                                                           PurchaseGlobalVariable.invid)
        print(quantitylimitcheck_response.json())

        assert quantitylimitcheck_response.json()["msg"] == ""
        assert quantitylimitcheck_response.json()["status"] == "success"
        assert quantitylimitcheck_response.json()["success"] is True

    @allure.title("采购订单提交预览页面-2")
    @pytest.mark.format_interface
    def test_format_interface(self, login_fixture, base_url):
        """
        采购订单提交预览页面接口，作用暂时未知
        :param login_fixture:
        :param base_url:
        :return:
        """
        format_interface_response = format_interface(login_fixture, base_url, PurchaseGlobalVariable.skuid,
                                                     PurchaseGlobalVariable.minnum)
        print(format_interface_response.json())

        assert format_interface_response.json()["success"] is True
        assert format_interface_response.json()["status"] == "success"
        assert format_interface_response.json()["msg"] == "查询成功"

    @allure.title("保存草稿")
    @pytest.mark.saveinvpo
    def test_saveinvpo(self, login_fixture, base_url):
        """
        预览页面提交后先生成草稿订单
        :param login_fixture:
        :param base_url:
        :return:
        """
        location_info = inv_location(login_fixture, base_url)
        for i in location_info.json()["data"]["storeLocation"][0]["locationList"]:
            if i["number"] == "KZ001":
                PurchaseGlobalVariable.location_id = i["id"]
        saveinvpo_respongse = save_inv_po(login_fixture, base_url, PurchaseGlobalVariable.location_id,
                                          PurchaseGlobalVariable.invid, PurchaseGlobalVariable.skuid,
                                          PurchaseGlobalVariable.minnum)
        print(saveinvpo_respongse.json())

        # 草稿单id
        PurchaseGlobalVariable.draft_id = saveinvpo_respongse.json()["id"]

        assert saveinvpo_respongse.json()["success"] is True
        assert saveinvpo_respongse.json()["status"] == "success"
        assert saveinvpo_respongse.json()["msg"] == "保存草稿成功！"

    @allure.title("查询草稿订单")
    @pytest.mark.initpoconfrim
    def test_initpoconfrim(self, login_fixture, base_url):
        """
        提交草稿单后同时查询该草稿单
        :param login_fixture:
        :param base_url:
        :return:
        """
        initpoconfrim_response = init_po_conf_rim(login_fixture, base_url, PurchaseGlobalVariable.draft_id)
        print(initpoconfrim_response.json())

        # 提交订单参数，期货商品/现货商品其中一个详情，以及订单信息
        PurchaseGlobalVariable.order_info = initpoconfrim_response.json()["data"]["list"]["futures"]["order"][0] if \
            initpoconfrim_response.json()["data"]["list"]["stocks"]["order"] == [] else \
            initpoconfrim_response.json()["data"]["list"]["stocks"]["order"][0]

        assert initpoconfrim_response.json()["success"] is True
        assert initpoconfrim_response.json()["status"] == "success"
        assert initpoconfrim_response.json()["msg"] == "查询成功！"

    @allure.title("提交订单")
    @pytest.mark.submitinvpocg
    def test_submitinvpocg(self, login_fixture, base_url):
        """
        校验草稿单后提交该草稿单
        :param login_fixture:
        :param base_url:
        :return:
        """
        submitinvpocg_response = submit_inv_po_cg(login_fixture, base_url, PurchaseGlobalVariable.order_info,
                                                  PurchaseGlobalVariable.draft_id)
        print(submitinvpocg_response.json())

        PurchaseGlobalVariable.order_list = submitinvpocg_response.json()["orderList"]

        assert submitinvpocg_response.json()["success"] is True
        assert submitinvpocg_response.json()["status"] == "success"
        assert submitinvpocg_response.json()["msg"] == "提交订单成功！"

    @allure.title("收银台页面获取订单信息")
    @pytest.mark.getpayinfonew
    def test_getpayinfonew(self, login_fixture, base_url):
        """
        查询订单,获取订单详情
        :param login_fixture:
        :param base_url:
        :return:
        """
        getpayinfonew_response = get_pay_info_new(login_fixture, base_url, PurchaseGlobalVariable.order_list)
        print(getpayinfonew_response.json())

        PurchaseGlobalVariable.pretradetoken_id = getpayinfonew_response.json()["data"]["preTradeToken"]

        assert getpayinfonew_response.json()["success"] is True
        assert getpayinfonew_response.json()["status"] == "success"
        assert getpayinfonew_response.json()["message"] == "成功"
        assert getpayinfonew_response.json()["code"] == 0

    @allure.title("订单支付")
    @pytest.mark.nopagepay
    def test_nopagepay(self, login_fixture, base_url):
        """
        订单支付
        :param login_fixture:
        :param base_url:
        :return:
        """
        nopagepay_response = no_page_pay(login_fixture, base_url, PurchaseGlobalVariable.pretradetoken_id)
        print(nopagepay_response.json())

        assert nopagepay_response.json()["success"] is True
        assert nopagepay_response.json()["status"] == "success"
        assert nopagepay_response.json()["message"] == "成功"
        assert nopagepay_response.json()["code"] == 0

    @allure.title("采购订单查询-待支付页面")
    @pytest.mark.invpo
    def test_invpo(self, login_fixture, base_url):
        """
        支付完成后，返回到采购订单查询待支付页面
        :param login_fixture:
        :param base_url:
        :return:
        """
        invpo_response = inv_po(login_fixture, base_url)
        print(invpo_response.json())

        assert invpo_response.json()["success"] is True
        assert invpo_response.json()["status"] == "success"
        assert invpo_response.json()["msg"] == "查询成功！"


@allure.epic("采购模块")
@allure.feature("普通采购未发货退货流程")
class TestReturnTheGoods:

    @allure.title("未发货退货查询采购订单")
    @pytest.mark.getinvpoinfo
    def test_getinvpoinfo(self, login_fixture, base_url):
        """
        到未发货页面，查询采购订单是否存在；每120秒查询一次采购订单，采购订单billstatus=3继续执行
        :param login_fixture:
        :param base_url:
        :return:
        """
        while True:
            a = inv_po(login_fixture, base_url=base_url, typenumber="allStatus",
                       skey=PurchaseGlobalVariable.order_list[0])
            if a.json()["data"]["rows"][0]["billStatus"] == "3":
                break
            else:
                sleep(120)
        getinvpoinfo_response = get_inv_po_info(login_fixture, base_url, skey=PurchaseGlobalVariable.order_list[0])
        print(getinvpoinfo_response.json())

        for i in getinvpoinfo_response.json()["data"]["rows"]:
            PurchaseGlobalVariable.ids.append(i["id"])
        PurchaseGlobalVariable.iid = getinvpoinfo_response.json()["data"]["rows"][0]["iid"]
        PurchaseGlobalVariable.getinvpoinfo_response_info = getinvpoinfo_response.json()["data"]["rows"]

        assert getinvpoinfo_response.json()["msg"] == "查询成功！"
        assert getinvpoinfo_response.json()["status"] == "success"
        assert getinvpoinfo_response.json()["data"]["rows"][0]["billNo"] == PurchaseGlobalVariable.order_list[0]

    @allure.title("未发货商品提交预览")
    @pytest.mark.getinvpoinfoformat
    def test_getinvpoinfoformat(self, login_fixture, base_url):
        """
        未发货商品提交预览
        :param login_fixture:
        :param base_url:
        :return:
        """
        getinvpoinfoformat_response = get_inv_po_info_format(login_fixture, base_url, ids=PurchaseGlobalVariable.ids)
        print(getinvpoinfoformat_response.json())

        PurchaseGlobalVariable.getinvpoinfoformat_token = getinvpoinfoformat_response.json()["data"]["token"]

        assert getinvpoinfoformat_response.json()["msg"] == "查询成功！"
        assert getinvpoinfoformat_response.json()["status"] == "success"
        assert getinvpoinfoformat_response.json()["data"]["rows"][0]["billNo"] == PurchaseGlobalVariable.order_list[0]

    @allure.title("未发货商品关闭")
    @pytest.mark.closeinvpo
    def test_closeinvpo(self, login_fixture, base_url):
        """
        未发货商品关闭
        :param login_fixture:
        :param base_url:
        :return:
        """
        get_goodslist = []
        for i in PurchaseGlobalVariable.getinvpoinfo_response_info:
            n = {"id": i["id"], "iid": i["iid"]}
            get_goodslist.append(n)
        closeinvpo_response = close_inv_po(login_fixture, base_url, goodslist=get_goodslist,
                                           token=PurchaseGlobalVariable.getinvpoinfoformat_token)
        print(closeinvpo_response.json())

        assert closeinvpo_response.json()["msg"] == "关闭成功1条采购单!"
        assert closeinvpo_response.json()["status"] == "success"
        assert closeinvpo_response.json()["success"] is True
