import time
import sys
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import hashlib


def default_headers():
    return {
        'User-Agent': 'Android com.kuangxiangciweimao.novel ',
        "Content-Type": "application/x-www-form-urlencoded",
    }


class Util:
    iv = b'\0' * 16

    def __init__(self):
        self.max_retry = 10
        self.requests_timeout = 20

    def decrypt(self, encrypted, key: str = 'zG2nSeEfSHfvTCHy5LCcqtBbQehKNLXn'):
        cipher_aes_key = algorithms.AES(hashlib.sha256(key.encode('utf-8')).digest())
        cipher = Cipher(cipher_aes_key, modes.CBC(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(base64.b64decode(encrypted)) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return decrypted_data.decode('utf-8')

    def encrypt(self, text, key: str = 'zG2nSeEfSHfvTCHy5LCcqtBbQehKNLXn'):
        cipher_aes_key = algorithms.AES(hashlib.sha256(key.encode('utf-8')).digest())
        cipher = Cipher(cipher_aes_key, modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(text.encode('utf-8')) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted_data)

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
