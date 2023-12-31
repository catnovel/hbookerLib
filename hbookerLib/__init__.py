import json
from . import util, url_constants


class HbookerAPI:
    def __init__(self):
        self.account = None
        self.login_token = None
        self.util = util.Util()
        self.common_params = {'app_version': '2.9.290', 'device_token': 'ciweimao_'}

    def set_common_params(self, account, login_token):
        if len(login_token) != 32:
            raise ValueError('login_token must be 32 characters long')
        elif "书客" not in account:
            raise ValueError('account must be a valid account')

        self.common_params.update({'account': account, 'login_token': login_token})

    def post(self, api_url, data=None):
        if data is None:
            data = self.common_params
        if data is not None:
            data.update(self.common_params)
        api_point = api_url.replace(url_constants.WEB_SITE, '')
        try:
            return json.loads(self.util.decrypt(self.util.post(url_constants.WEB_SITE + api_point, data=data)))
        except Exception as error:
            print("post error:", error)

    def login(self, login_name, passwd):
        return self.post(url_constants.MY_SIGN_LOGIN, {'login_name': login_name, 'passwd': passwd})

    def get_shelf_list(self):
        return self.post(url_constants.BOOKSHELF_GET_SHELF_LIST)

    def get_shelf_book_list(self, shelf_id, last_mod_time='0', direction='prev'):
        return self.post(url_constants.BOOKSHELF_GET_SHELF_BOOK_LIST,
                         {'shelf_id': shelf_id, 'last_mod_time': last_mod_time, 'direction': direction})

    def get_division_list(self, book_id):
        return self.post(url_constants.GET_DIVISION_LIST, {'book_id': book_id})

    def get_updated_chapter_by_division_new(self, book_id: str):
        return self.post(url_constants.GET_DIVISION_LIST_NEW, {'book_id': book_id})

    def get_chapter_update(self, division_id, last_update_time='0'):
        return self.post(url_constants.GET_CHAPTER_UPDATE,
                         {'division_id': division_id, 'last_update_time': last_update_time})

    def get_info_by_id(self, book_id):
        return self.post(url_constants.BOOK_GET_INFO_BY_ID, {'book_id': book_id})

    def get_chapter_command(self, chapter_id):
        return self.post(url_constants.GET_CHAPTER_COMMAND, {'chapter_id': chapter_id})

    def get_cpt_ifm(self, chapter_id, chapter_command):
        return self.post(url_constants.GET_CPT_IFM, {'chapter_id': chapter_id, 'chapter_command': chapter_command})

    def get_check_in_records(self):
        return self.post(url_constants.SIGN_RECORD, {})

    def do_check_in(self):
        return self.post(url_constants.SING_RECORD_TASK, {'task_type': 1})

    def get_version(self):
        return self.post(url_constants.MY_SETTING_UPDATE)
