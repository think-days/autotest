import requests
from requests import Response


def login(s, base_url, username="1176", userpwd="dgj123456", ispwd=1) -> Response:
    """

    :param s:Session对象
    :param username:登录用户名
    :param userpwd:登录密码
    :param ispwd:是否记住密码
    :return:返回登陆对象
    """
    login_url = base_url + "/index.php/passport/login/signIn"
    body = {
        "username": username,
        "userpwd": userpwd,
        "ispwd": ispwd
    }
    r1 = s.post(login_url, data=body)
    return r1


if __name__ == "__main__":
    s = requests.session()
    base_url = "http://dgj-staging.kzmall.cc"
    a = login(s, base_url)
    print(a.json())
