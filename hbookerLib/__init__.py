import time
import uuid
from . import client, util, url_constants


class HbookerAPI:

    def __init__(self, account: str = None, login_token: str = None, verify_token: bool = False):
        self.util = client.Client()
        if account is not None and login_token is not None:
            self.util.set_common_params(account, login_token)
            if verify_token:
                self.verify_token()

    def verify_token(self):
        if self.get_my_info().get('code') != '100000':
            raise ValueError('Invalid account or login_token')

    def get_my_info(self):
        return self.util.post(url_constants.MY_DETAILS_INFO)

    @util.deprecated("ciweimao has added geetest verification, this login interface is invalid")
    def login(self, login_name, passwd):
        return self.util.post(url_constants.MY_SIGN_LOGIN, {'login_name': login_name, 'passwd': passwd})

    def signup_use_geetest(self, login_name: str):
        return self.util.post(url_constants.SIGNUP_USE_GEETEST, {'login_name': login_name})

    def signup_first_register(self, login_name: str):
        params = {'user_id': login_name, 't': int(round(time.time() * 1000))}
        return self.util.get(url_constants.SIGNUP_FIRST_REGISTER, params=params)

    def login_new(self, login_name, passwd, geetest_validate, geetest_challenge):
        data = {'login_name': login_name, 'passwd': passwd, 'geetest_seccode': geetest_validate + "|jordan",
                'geetest_validate': geetest_validate, 'geetest_challenge': geetest_challenge}
        return self.util.post(url_constants.MY_SIGN_LOGIN, data=data)

    def get_shelf_list(self):
        return self.util.post(url_constants.BOOKSHELF_GET_SHELF_LIST)

    @util.deprecated(
        "ciweimao has used new interface since version 2.9.290, please use get_shelf_book_list_new() instead")
    def get_shelf_book_list(self, shelf_id, last_mod_time='0', direction='prev'):
        return self.util.post(url_constants.BOOKSHELF_GET_SHELF_BOOK_LIST,
                              {'shelf_id': shelf_id, 'last_mod_time': last_mod_time, 'direction': direction})

    def get_shelf_book_list_new(self, shelf_id):
        data = {'count': 999, 'page': 0, 'order': 'last_read_time', 'shelf_id': shelf_id}
        return self.util.post(url_constants.BOOKSHELF_GET_SHELF_BOOK_LIST_NEW, data)

    def get_bookshelf(self):
        shelf_list = self.get_shelf_list()
        if shelf_list.get('code') != '100000':
            print(f"get_shelf_list error: {shelf_list.get('tip', 'Unknown error')}")
            return
        for shelf in shelf_list['data']['shelf_list']:
            book_list = self.get_shelf_book_list_new(shelf['shelf_id'])
            if book_list.get('code') == '100000':
                for data in book_list['data']['book_list']:
                    yield data['book_info']
            else:
                print(f"get_shelf_book_list_new error: {book_list.get('tip', 'Unknown error')}")

    @util.deprecated("please use get_updated_chapter_by_division_new() instead,This api is deprecated")
    def get_division_list(self, book_id):
        return self.util.post(url_constants.GET_DIVISION_LIST, {'book_id': book_id})

    @util.deprecated("please use get_updated_chapter_by_division_new() instead,This api is deprecated")
    def get_chapter_update(self, division_id):
        return self.util.post(url_constants.GET_CHAPTER_UPDATE, {'division_id': division_id, 'last_update_time': '0'})

    def get_updated_chapter_by_division_new(self, book_id: str):
        return self.util.post(url_constants.GET_DIVISION_LIST_NEW, {'book_id': book_id})

    def get_info_by_id(self, book_id):
        return self.util.post(url_constants.BOOK_GET_INFO_BY_ID, {'book_id': book_id})

    def get_chapter_command(self, chapter_id):
        return self.util.post(url_constants.GET_CHAPTER_COMMAND, {'chapter_id': chapter_id})

    def get_cpt_ifm(self, chapter_id, command):
        return self.util.post(url_constants.GET_CPT_IFM, {'chapter_id': chapter_id, 'chapter_command': command})

    def get_chapter_content(self, chapter_id):
        command = self.get_chapter_command(chapter_id)
        command_data = command.get('data', {})
        if not command_data.get('command'):
            print(f"get_chapter_command error: {command.get('tip', 'Unknown error')}")
            return
        chapter_info = self.get_cpt_ifm(chapter_id, command_data['command'])
        if chapter_info.get('code') != '100000':
            print(f"get_chapter_content error: {chapter_info.get('tip', 'Unknown error')}")
            return
        txt_content = chapter_info.get('data', {}).get('chapter_info', {}).get('txt_content', '')
        if txt_content:
            decrypted_content = self.util.decrypt(txt_content, command_data['command']).decode('utf-8')
            chapter_info['data']['chapter_info']['txt_content'] = decrypted_content
        else:
            print("get_chapter_content error: txt_content is empty")
            return
        return chapter_info

    def get_check_in_records(self):
        return self.util.post(url_constants.SIGN_RECORD, {})

    def do_check_in(self):
        return self.util.post(url_constants.SING_RECORD_TASK, {'task_type': 1})

    def get_version(self):
        return self.util.post(url_constants.MY_SETTING_UPDATE)

    def auto_req_v2(self, android_id=None):
        data = {"oauth_union_id": "", "gender": 1, "oauth_open_id": "", "channel": "oppo", "oauth_type": "",
                'uuid': android_id if android_id else "android" + uuid.uuid4().hex}
        return self.util.post(url_constants.SIGNUP_AUTO_REQ_V2, data=data)
