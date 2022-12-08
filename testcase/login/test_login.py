"""
参数化登录
"""

import requests
import pytest

from utils.read_yml import readyml
from pathlib import Path
from api.public_func.login_funtion import login

p = Path(__file__)
yamlPath = p.parent.parent.parent.joinpath("testdata", "login.yml")
login_data = readyml(yamlPath)["login"]


@pytest.mark.login
@pytest.mark.parametrize("test_input, expected", login_data)
def test_login_params(test_input, base_url, expected):
    print("测试数据", test_input)
    s = requests.Session()
    r = login(s, base_url, **test_input)
    print(r.json())
    assert r.json()["redirect"] == expected["redirect"]
    assert r.json()["msg"] == expected["msg"]
    assert r.json()["status"] == expected["status"]
