import base64
import requests
import os

from .config import *
from .get_header import *

path = os.getcwd()

class GetVervfi():
    def __new__(self):
        self.GetVerifiCodeImg(self)
        return self

    def GetVerifiCodeImg(self):
        url = 'https://pix.ipv4.host/verificationCode'
        headers = get_verification_code_header()
        verifi = requests.get(url, headers=headers).json()
        image_base64 = verifi['data']['imageBase64']
        byte_data = base64.b64decode(image_base64)
        with open(f'data/PixivSearcher/tmp.png', 'wb') as f:
            f.write(byte_data)
            f.close()
        self.verify = verifi['data']['vid']

class login__():
    def __init__(self, verifi, login_msg):
        self.verifi = verifi
        self.login_msg = login_msg
        self.login()

    def login(self):
        account_data = read('account')
        account = json.dumps({"username": account_data['username'], "password": account_data['password']})
        url1 = f"https://pix.ipv4.host/users/token?vid={self.verifi}&value={self.login_msg}"
        account_msg = requests.post(url1, data=account, headers=get_login_header())
        self.accountjson = account_msg.json()['message']
        if 'authorization' in account_msg.headers:
            token = account_msg.headers['authorization']
        if self.accountjson == '登录成功':
            account_data['token'] = token
            write(account_data, 'account')
            os.remove('data/PixivSearcher/tmp.png')
        if self.accountjson == '验证码错误':
            os.remove('data/PixivSearcher/tmp.png')