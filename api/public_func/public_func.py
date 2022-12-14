"""
公共接口
"""
import json
import os
import time

from filetype import filetype
from requests import Response
from requests_toolbelt import MultipartEncoder


def inv_location(s, base_url, *args, **kwargs) -> Response:
    """
    获取仓库信息
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:仓库明细
    """
    inv_location_url = base_url + "/index.php/basedata/invlocation"
    inv_location_data = {
        "action": "list",
        "isDelete": 2
    }
    inv_location_response = s.get(url=inv_location_url, params=inv_location_data)
    print(inv_location_response.json())
    return inv_location_response


# 未发货商品页面（get_inv_po_info，get_inv_po_info_format，close_inv_po）
def get_inv_po_info(s, base_url, skey, *args, **kwargs) -> Response:
    """未发货订单根据订单号查询"""
    getinvpoinfo_url = base_url + "/index.php/scm/InvPo/getInvPoInfo"
    getinvpoinfo_data = {
        "skey": skey,
        "category_ids": "",
        "skuStatus": 0,
        "page": 1,
        "rows": 100,
        "waitOut": "true",
        "transType": 170401,
        "status": 5,
        "behivior": "",
        "supply_id": "",
        "beginDate": "",
        "endDate": ""
    }
    getinvpoinfo_response = s.post(url=getinvpoinfo_url, data=getinvpoinfo_data)
    return getinvpoinfo_response


def get_inv_po_info_format(s, base_url, ids, *args, **kwargs) -> Response:
    """未发货商品提交预览"""
    getinvpoinfo_url = base_url + "/index.php/scm/invPo/getInvPoInfoFormat"
    getinvpoinfo_data = {
        "ids": ids
    }
    getinvpoinfo_response = s.post(url=getinvpoinfo_url, data=getinvpoinfo_data)
    return getinvpoinfo_response


def close_inv_po(s, base_url, goodslist, token, *args, **kwargs) -> Response:
    """未发货商品提交关闭"""
    closeinvpo_url = base_url + "/index.php/scm/invPo/closeInvPo"
    closeinvpo_params = {
        "action": "closeInvPo"
    }
    closeinvpo_data = {
        "goodsList": json.dumps(goodslist),
        "token": token
    }
    closeinvpo_response = s.post(url=closeinvpo_url, data=closeinvpo_data, params=closeinvpo_params)
    return closeinvpo_response


# 退货申请单列表（return_order_list）
def after_sale_list(s, base_url, key_words=None, bill_status="", order_type=None, *args, **kwargs) -> Response:
    """
    售后申请单查询
    :param s:
    :param base_url:
    :param key_words:售后订单号, str
    :param bill_status:售后订单状态, str
    :param order_type:售后订单类型, str
    :param args:
    :param kwargs:
    :return:
    """
    after_sale_list_url = base_url + "/index.php/po/AfterSale/list"
    after_sale_list_data = {
        "page": 1,
        "limit": 20,
        "keywords": key_words,
        "billStatus": bill_status,
        "orderType": order_type
    }
    after_sale_list_response = s.post(after_sale_list_url, data=after_sale_list_data)
    return after_sale_list_response


def cancel_draft(s, base_url, id_s) -> Response:
    """
    取消订单
    :param s:
    :param base_url:
    :param id_s:草稿单id, str
    :return:
    """
    cancel_draft_url = base_url + "/index.php/po/AfterSale/cancel"
    cancel_draft_data = {
        "id": id_s
    }
    cancel_draft_response = s.post(cancel_draft_url, data=cancel_draft_data)
    return cancel_draft_response


# 退货申请单商品查询
def get_return_goods(s, base_url, po_order=None, sku_id=None, product_code=None, product_name=None, *args,
                     **kwargs) -> Response:
    """
    查询退货申请单中中可用数据:不良品退货、少发退货、直采退货
    :param s:
    :param base_url:
    :param base_url:
    :param po_order:采购订单号,str
    :param sku_id:物料编码,str
    :param product_code:产品码,str
    :param product_name:物料名称,str
    :param args:
    :param kwargs:键值对，用于区分退货类型
    :return:
    """
    get_return_goods_type_one_url = base_url + "/index.php/scm/invPo/getReturnGoods"
    get_return_goods_type_one_param = {
        "action": "getReturnGoods",
        **kwargs
    }
    get_return_goods_type_one_data = {
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
    print("....", get_return_goods_type_one_param)
    get_return_goods_type_one_response = s.post(get_return_goods_type_one_url, data=get_return_goods_type_one_data,
                                                params=get_return_goods_type_one_param)
    return get_return_goods_type_one_response


# 退货申请单-获取商品下仓库、货位明细，用于切换仓库
def get_goods_by_storage_and_area_info(s, base_url, inv_ids, location_id) -> Response:
    """
    退货申请单中选择商品页面，选择商品后，切换仓库，返回该物料下的仓库、货位明细
    :param s:
    :param base_url:
    :param inv_ids:字符串，inv_id
    :param location_id:字符串，仓库id
    :return:
    """
    get_goods_by_storage_and_area_info_url = base_url + "/index.php/basedata/Inventory/getGoodsByStorageAndAreaInfo"
    get_goods_by_storage_and_area_info_params = {
        "isGoodsToStorageType": "true"
    }
    get_goods_by_storage_and_area_info_date = {
        "invIds[]": inv_ids,
        "locationId": location_id,
        "NoStorage": "no"
    }
    get_goods_by_storage_and_area_info_response = s.post(url=get_goods_by_storage_and_area_info_url,
                                                         data=get_goods_by_storage_and_area_info_date,
                                                         params=get_goods_by_storage_and_area_info_params)
    return get_goods_by_storage_and_area_info_response


# 不良品退货页面
def get_contact_2_select(s, base_url, *args, **kwargs) -> Response:
    """
    获取客户信息
    :param s:
    :param base_url:
    :param args:
    :param kwargs:
    :return:
    """
    get_contact_2_select_url = base_url + "/index.php/basedata/contact/getContact2Select"
    get_contact_2_select_response = s.post(get_contact_2_select_url)
    print(get_contact_2_select_response.text)
    return get_contact_2_select_response


# 不良品退货页面，上传图片
def upload(filepath="files/122.png"):
    """根据文件路径，自动获取文件名称和文件mime类型"""
    kind = filetype.guess(filepath)
    if kind is None:
        print('Cannot guess file type!')
        return
    # 媒体类型，如：image/png
    mime_type = kind.mime
    # 文件真实路径
    file_real_path = os.path.realpath(filepath)
    # 获取文件名 122.png
    file_name = os.path.split(file_real_path)[-1]
    return file_name, open(file_real_path, "rb"), mime_type


def upload_file_to_oss(s, base_url, file_path) -> Response:
    """
    上传图片/视频接口
    :param s:
    :param base_url:
    :param file_path:文件绝对路径
    :return:
    """
    upload_file_to_oss_url = base_url + "/index.php/file/ossFile/uploadFileToOSS"
    m = MultipartEncoder(fields={"file": upload(filepath=file_path)})
    upload_file_to_oss_response = s.post(upload_file_to_oss_url, data=m, headers={'Content-Type': m.content_type})
    return upload_file_to_oss_response


# 创建退货单
def create_return_goods_order(s, base_url, create_data) -> Response:
    """
    创建退货单，根据不同的退货单类型传入不同的参数，需外部传参
    :param s:
    :param base_url:
    :param create_data:
    :return:
    """
    create_url = base_url + "/index.php/po/AfterSale/create"
    create_response = s.post(create_url, json=create_data)
    return create_response


# 查询退货草稿单
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
    return get_split_order_back_info_response


# 退货订单提交
def submit_draft(s, base_url, order_id, *args, **kwargs) -> Response:
    """
    退货提交订单
    :param s:
    :param base_url:
    :param order_id: 订单ID，来自create_draft
    :return:
    """
    submit_url = base_url + "/index.php/po/AfterSale/submit"
    submit_data = {
        "id": order_id
    }
    submit_response = s.post(submit_url, data=submit_data)
    return submit_response

# if __name__ == '__main__':
# s = requests.Session()
# base_url = "http://dgj-staging.kzmall.cc"
# c = login(s, base_url)
#
# a = get_goods_by_storage_and_area_info(s, base_url, 897, 640)
# print(a.json())
