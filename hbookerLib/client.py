import json
import time
import sys
import httpx
import base64
import hashlib

from hbookerLib import url_constants, util
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

APP_VERSION = '2.9.290'
DEVICE_TOKEN = 'ciweimao_'

SK_DEVICE_TOKEN = 'shuke_'
SK_APP_VERSION = '1.5.596'


class Client:
    IV = b'\0' * 16

    def __init__(self, sk: bool):
        self.sk = sk
        self.max_retry = 5
        self.host = url_constants.WEB_SITE
        self.common_params = {'app_version': APP_VERSION, 'device_token': DEVICE_TOKEN}
        self.set_sk_client()

    def set_sk_client(self):
        if self.sk:
            self.host = url_constants.SK_WEB_SITE
            self.common_params['app_version'] = SK_APP_VERSION
            self.common_params['device_token'] = SK_DEVICE_TOKEN

    def set_common_params(self, account, login_token):
        if len(login_token) != 32:
            raise ValueError('login_token must be 32 characters long')
        elif "书客" not in account:
            raise ValueError('account must be a valid account')

        self.common_params.update({'account': account, 'login_token': login_token})

    def decrypt(self, encrypted, key: str = 'zG2nSeEfSHfvTCHy5LCcqtBbQehKNLXn'):
        cipher_aes_key = algorithms.AES(hashlib.sha256(key.encode('utf-8')).digest())
        cipher = Cipher(cipher_aes_key, modes.CBC(self.IV), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(base64.b64decode(encrypted)) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return decrypted_data.decode('utf-8')

    def encrypt(self, text, key: str = 'zG2nSeEfSHfvTCHy5LCcqtBbQehKNLXn'):
        cipher_aes_key = algorithms.AES(hashlib.sha256(key.encode('utf-8')).digest())
        cipher = Cipher(cipher_aes_key, modes.CBC(self.IV), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(text.encode('utf-8')) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted_data)

    def default_headers(self):
        return {
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': 'Android com.kuangxiangciweimao.novel ' + self.common_params['app_version'],
        }

    def get(self, api_point: str, data: dict = None):
        data = data or {}
        data.update(self.common_params)
        for count in range(self.max_retry):
            try:
                res = httpx.get(url=self.host + api_point, params=data, headers=self.default_headers())
                if util.is_json(res.text):
                    return json.loads(res.text)
                return json.loads(self.decrypt(res.text))
            except Exception as e:
                print(f"\nGet Error Retry: {e}\n{api_point}")
                time.sleep(1 * count)
        print("\nGet Failed, Terminating......")
        sys.exit(1)

    def post(self, api_point: str, data: dict = None):
        data = data or {}
        data.update(self.common_params)
        for count in range(self.max_retry):
            try:
                res = httpx.post(url=self.host + api_point, data=data, headers=self.default_headers())
                if util.is_json(res.text):
                    return json.loads(res.text)
                return json.loads(self.decrypt(res.text))
            except Exception as e:
                print(f"\nPost Error Retry: {e}\n{api_point}")
                time.sleep(1 * count)
        print("\nPost Failed, Terminating......")
        sys.exit(1)
