import yaml
import os


def readyml(yamlPath):
    """
    读取yaml文件内容
    :param yamlPath:文件的真实路径，绝对路径地址
    :return:
    """
    if not os.path.isfile(yamlPath):
        raise FileExistsError("文件路径不存在，请检查是否正确:%s" % yamlPath)
    # open方法打开直接读取

    f = open(yamlPath, "r", encoding="utf-8")
    cfg = f.read()
    d = yaml.safe_load(cfg)
    return d


if __name__ == "__main__":
    r = readyml(yamlPath="A:\\Code\\aotuuse_test1\\testdata\\login.yml")
    print(r)
