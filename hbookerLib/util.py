import json
import time
import sys
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import hashlib

from hbookerLib import url_constants


def default_headers():
    return {
        'User-Agent': 'Android com.kuangxiangciweimao.novel ',
        "Content-Type": "application/x-www-form-urlencoded",
    }


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


class Util:
    IV = b'\0' * 16
    APP_VERSION = '2.9.290'
    DEVICE_TOKEN = 'ciweimao_'

    def __init__(self, account=None, login_token=None):
        self.max_retry = 10
        self.requests_timeout = 20
        self.common_params = {'app_version': self.APP_VERSION, 'device_token': self.DEVICE_TOKEN}

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

    def get(self, url, params=None):
        headers = default_headers()
        if params.get('app_version') is not None:
            headers['User-Agent'] += params.get('app_version')
        for count in range(self.max_retry):
            try:
                res = requests.get(url, params=params, headers=headers, timeout=self.requests_timeout)
                if is_json(res.text):
                    return json.loads(res.text)
                return json.loads(self.decrypt(res.text))
            except requests.exceptions.RequestException as e:
                print("\nGet Error Retry: " + str(e) + '\n' + url)
                time.sleep(1 * count)
            except Exception as e:
                print(repr(e))
                break
        print("\nGet Failed, Terminating......")
        sys.exit(1)

    def post(self, api_point, data=None):
        headers = default_headers()
        if data.get('app_version') is not None:
            headers['User-Agent'] += data.get('app_version')
        url = url_constants.WEB_SITE + api_point
        data = data or {}
        data.update(self.common_params)
        for count in range(self.max_retry):
            try:
                res = requests.post(url=url, data=data, headers=headers, timeout=self.requests_timeout)
                if is_json(res.text):
                    return json.loads(res.text)
                return json.loads(self.decrypt(res.text))
            except requests.exceptions.RequestException as e:
                print(f"\nPost Error Retry: {e}\n{url}")
                time.sleep(1 * count)
            except Exception as e:
                print(repr(e))
                break
        print("\nPost Failed, Terminating......")
        sys.exit(1)
