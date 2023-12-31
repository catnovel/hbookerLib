import time
import sys
import base64
import hashlib
import requests
from Crypto.Cipher import AES


def default_headers():
    return {
        'User-Agent': 'Android com.kuangxiangciweimao.novel ',
        "Content-Type": "application/x-www-form-urlencoded",
    }


class Util:
    def __init__(self):
        self.max_retry = 10
        self.iv = b'\0' * 16
        self.requests_timeout = 20
        self.key = 'zG2nSeEfSHfvTCHy5LCcqtBbQehKNLXn'
        self.aes_key = hashlib.sha256(self.key.encode('utf-8')).digest()

    def encrypt(self, text, key: str = ""):
        aes_key = hashlib.sha256(key.encode('utf-8')).digest() if key != "" else self.aes_key
        return base64.b64encode(AES.new(aes_key, AES.MODE_CFB, self.iv).encrypt(text))

    def decrypt(self, encrypted, key: str = ""):
        aes_key = hashlib.sha256(key.encode('utf-8')).digest() if key != "" else self.aes_key
        data = AES.new(aes_key, AES.MODE_CBC, self.iv).decrypt(base64.b64decode(encrypted))
        length = len(data)
        un_padding = ord(chr(data[length - 1]))
        return data[0:length - un_padding]

    def get(self, url, params=None, **kwargs):
        for count in range(self.max_retry):
            try:
                return requests.get(url, params=params, headers=default_headers(), **kwargs,
                                    timeout=self.requests_timeout).text
            except requests.exceptions.RequestException as e:
                print("\nGet Error Retry: " + str(e) + '\n' + url)
                time.sleep(1 * count)
            except Exception as e:
                print(repr(e))
                break
        print("\nGet Failed, Terminating......")
        sys.exit(1)

    def post(self, url, data=None, **kwargs):
        for count in range(self.max_retry):
            try:
                headers = default_headers()
                if data.get('app_version') is not None:
                    headers['User-Agent'] += data.get('app_version')
                print(headers)
                return requests.post(url, data, headers=headers, **kwargs, timeout=self.requests_timeout).text
            except requests.exceptions.RequestException as e:
                print("\nPost Error Retry: " + str(e) + '\n' + url)
                time.sleep(1 * count)
            except Exception as e:
                print(repr(e))
                break
        print("\nPost Failed, Terminating......")
        sys.exit(1)
