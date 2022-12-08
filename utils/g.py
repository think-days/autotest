import filetype
import os
from requests_toolbelt import MultipartEncoder
import requests
# 作者-上海悠悠 QQ交流群：730246532


def upload(filepath="files/122.png"):
    '''根据文件路径，自动获取文件名称和文件mime类型'''
    kind = filetype.guess(filepath)
    if kind is None:
        print('Cannot guess file type!')
        return
    # 媒体类型，如：image/png
    mime_type = kind.mime
    # 文件真实路径
    file_real_path = os.path.realpath(filepath)
    # 获取文件名 122.png
    fullflname = os.path.split(file_real_path)[-1]
    return (fullflname, open(file_real_path, "rb"), mime_type)


m = MultipartEncoder(
    fields = [
                ('source', upload(filepath="files/122.png")),
                ('source', upload(filepath="files/123.png")),
            ]
            )

r = requests.post('http://httpbin.org/post',
                  data=m,
                  headers={'Content-Type': m.content_type})
