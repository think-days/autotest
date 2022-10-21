"""
退货申请单-不良品退货
"""
import time
from requests import Response
from api.public_func import upload_file_to_oss


def inv_po(s, base_url, *args, **kwargs) -> Response:
    """
    返回HTML页面
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:
    """
    inv_po_url = base_url + "/index.php/scm/invPo"
    inv_po_param = {
        "action": "returnBadGoodsOrder"
    }
    inv_po_data = {
        "_search": "false",
        "nd": time.time(),
        "rows": 20,
        "page": 1,
        "sidx": "",
        "sord": "asc"
    }
    inv_po_response = s.post(inv_po_url, data=inv_po_data, params=inv_po_param)
    # print(inv_po_response.text)
    return inv_po_response


def get_return_goods(s, base_url, po_order=None, sku_id=None, product_code=None, product_name=None, *args,
                     **kwargs) -> Response:
    """
    查询可用的不良品退货物料
    :param s:
    :param base_url:
    :param po_order:采购订单号,str
    :param sku_id:物料编码,str
    :param product_code:产品码,str
    :param product_name:物料名称,str
    :param args:
    :param kwargs:
    :return:
    """
    get_return_goods_url = base_url + "/index.php/scm/invPo/getReturnGoods"
    get_return_goods_params = {
        "action": "getReturnGoods"
    }
    get_return_goods_data = {
        "_search": "false",
        "nd": time.time(),
        "rows": 20,
        "page": 1,
        "sidx": "",
        "sord": "asc",
        "matchSO": po_order,
        "skuId": sku_id,
        "pid": product_code,
        "pname": product_name,
        "condition": "skuid"
    }
    get_return_goods_response = s.post(get_return_goods_url, data=get_return_goods_data, params=get_return_goods_params)
    print(get_return_goods_response.text)
    return get_return_goods_response


def get_return_goods_for_so_code(s, base_url, so_code_id, *args, **kwargs) -> Response:
    """
    选择商品，返回商品需要基本信息
    :param s:
    :param base_url:
    :param so_code_id:getReturnGoods返回的id,str
    :param args:
    :param kwargs:
    :return:
    """
    get_return_goods_for_so_code_url = base_url + "/index.php/scm/invPo/getReturnGoodsForSoCode"
    get_return_goods_for_so_code_params = {
        "soCodeId": so_code_id
    }
    get_return_goods_for_so_code_response = s.get(get_return_goods_for_so_code_url,
                                                  params=get_return_goods_for_so_code_params)
    print(get_return_goods_for_so_code_response.text)
    return get_return_goods_for_so_code_response


def get_return_goods_for_so_code_again(s, base_url, so_code_id, *args, **kwargs) -> Response:
    """
    提交预览不良品退货
    :param s:
    :param base_url:
    :param so_code_id:
    :param args:
    :param kwargs:
    :return:
    """
    get_return_goods_for_so_code_again_url = base_url + "/index.php/scm/invPo/getReturnGoodsForSoCode"
    get_return_goods_for_so_code_again_params = {
        "action": "getReturnGoodsForSoCode"
    }
    get_return_goods_for_so_code_again_data = {
        "soCodeId": so_code_id,
        "rtId": ""
    }
    get_return_goods_for_so_code_again_response = s.post(get_return_goods_for_so_code_again_url,
                                                         data=get_return_goods_for_so_code_again_data,
                                                         params=get_return_goods_for_so_code_again_params)
    print(get_return_goods_for_so_code_again_response.text)
    return get_return_goods_for_so_code_again_response


def after_sale_create(s, base_url, description, so_code_id, src_order_id, rt_num, contact_id, install_car_model,
                      install_time, install_mileage, oss_image_link, need_extra_voucher=0, need_video=0, *args, **kwargs) -> Response:
    """
    创建草稿单
    :param s:
    :param base_url:
    :param description:原因/备注,str
    :param so_code_id:选择商品id,str
    :param src_order_id:源订单id,str
    :param rt_num:提交数量,int
    :param contact_id:客户id,str
    :param install_car_model:安装车型,str
    :param install_time:安装时间,2020-12-12
    :param install_mileage:行驶里程,int
    :param oss_image_link:上传图片后的oss链接,list
    :param need_extra_voucher:是否需要额外售后凭证,0:不需要,1:需要
    :param need_video:
    :param args:
    :param kwargs:
    :return:
    """

    # 本地图片路径,仅在本地环境使用，更换环境则更换图片路径
    pictures = [
        "C:\\Users\\lumia\\Pictures\\9e39916b5c2b07d00c5900a481bd6146e3ee5811.jpg",
        "C:\\Users\\lumia\\Pictures\\0121952da2d96a4e1b8dd1ae6fb7b636.jpg",
        "C:\\Users\\lumia\\Pictures\\lALPD26eL7xLjdvNAfDNBNo_1242_496.jpg"
    ]
    oss_link = []
    # 获取上传图片后的链接
    for i in pictures:
        pictures_read = open(i, "rb")
        res = upload_file_to_oss(s, base_url, pictures_read)
        oss_link.append(res.json()["fileUrl"])
        pictures_read.close()

    after_sale_create_url = base_url + "/index.php//po/AfterSale/create"
    after_sale_create_data = {
        "description": description,
        "entries": [
            {
                "srcOrderEntryId": so_code_id,
                "srcOrderId": src_order_id,
                "rtNum": rt_num
            }
        ],
        "after_sale_certificate": {
            "contact_id": contact_id,
            "install_car_model": install_car_model,
            "install_time": install_time,
            "install_mileage": install_mileage,
            "image": oss_image_link,
            **kwargs
        },
        "need_extra_voucher": need_extra_voucher,
        "need_video": need_video,
        "orderType": "30-Cxx-06",
    }
    after_sale_create_response = s.post(after_sale_create_url, json=after_sale_create_data)
    print(after_sale_create_response.text)
    return after_sale_create_response


def get_split_order_back_info(s, base_url, defective_order_id, *args, **kwargs) -> Response:
    """
    查询草稿单，返回该草稿单明细
    :param s:
    :param base_url:
    :param defective_order_id: 不良品草稿单id:str
    :param args:
    :param kwargs:
    :return:
    """
    get_split_order_back_info_url = base_url + "/index.php/scm/invPo/getSplitOrderBackInfo"
    get_split_order_back_info_data = {
        "orderId": defective_order_id
    }
    get_split_order_back_info_response = s.post(get_split_order_back_info_url, data=get_split_order_back_info_data)
    print(get_split_order_back_info_response.text)
    return get_split_order_back_info_response

# submit_draft()
# after_sale_list()
# cancel_draft()
# after_sale_list()
