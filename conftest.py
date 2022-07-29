import pytest
import requests
from requests import Response

from api.login_funtion import login


@pytest.fixture(scope="session")
def login_fixture(base_url) -> Response:
    """全局登录session会话"""
    s = requests.Session()
    login(s, base_url)
    yield s
    s.close()  # 关闭会话
