"""
滞销品退货流程
"""
import api

class ReturnGlobalVariable:
    pass


class TestReturnOfSlowMovingGoods:
    """
    滞销品退货流程性用例
    打开滞销品页面-选择商品-创建草稿单-提交订单-退货申请单查询取消滞销品退货
    """

    def test_first_return_open(self, login_fixture, base_url):
        first_return_open()