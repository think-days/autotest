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


def after_sale_create(s, base_url, description, so_code_id, src_order_id, contact_id, install_car_model, install_time,
                      install_mileage, need_extra_voucher, need_video, pictures, rt_num=1, *args, **kwargs) -> Response:
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
    :param pictures:图片和视频的绝对路径
    :param need_extra_voucher:蓄电池凭证，是否需要额外售后凭证,0:不需要,1:需要
    :param need_video:轮胎凭证，物料是否需要上传视频,0:不需要,1:需要
    :param args:
    :param kwargs:
    :return:
    """
    oss_image_link = []
    oss_video_link = ""

    # 获取上传图片和视频后的链接
    for i in pictures:
        res = upload_file_to_oss(s, base_url, file_path=i)
        if "https://kz-open-beta.oss-cn-hangzhou" in res.json()["fileUrl"]:
            oss_image_link.append(res.json()["fileUrl"])
        if "http://kz-dgj.oss-cn-hangzhou" in res.json()["fileUrl"]:
            oss_video_link = res.json()["fileUrl"]

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
        },
        "need_extra_voucher": 0,
        "need_video": 0,
        "orderType": "30-Cxx-06",
    }
    # 如果物料是蓄电池，则需要传入下列参数
    if need_extra_voucher == "true":
        after_sale_create_data["after_sale_certificate"].update({"tagged_cca": "100",  # 标注CCA
                                                                 "measured_cca": "100",  # 实测CCA
                                                                 "date_code": "221010",  # 日期码
                                                                 "voltage": "24",  # 电压
                                                                 "color": 1,  # 电眼颜色，1:无电眼，2:绿色，3:黑色，4:白色
                                                                 "product_code": "123VS"  # 产品识别码
                                                                 })
        after_sale_create_data.update({"need_extra_voucher": 1})
    # 如果物料是轮胎，则需要传入下列参数
    if need_video == "true":
        after_sale_create_data["after_sale_certificate"].update({"car_number": "浙A12345",  # 车牌
                                                                 "production_date": "1232",  # 轮胎生产周期
                                                                 "video": oss_video_link  # 视频链接
                                                                 })
        after_sale_create_data["need_video"] = 1
    after_sale_create_response = s.post(after_sale_create_url, json=after_sale_create_data)
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
