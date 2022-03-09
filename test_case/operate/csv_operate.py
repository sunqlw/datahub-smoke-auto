import time
from page import JobEditPage
from ..data.constant_data import MESSAGE_DICT, COMP_DICT


class CsvOperate(object):
    def __init__(self, driver):
        self.page = JobEditPage(driver)

    # 根据传递进来的后缀列表选择或者取消后缀
    def select_suffix(self, *suffix_list):
        self.page.file_suffix_select.click()
        for suffix_name in suffix_list:
            if suffix_name not in ['txt', 'csv', 'noSuffix']:
                self.page.file_suffix_input = suffix_name
            self.page.file_suffix_elem(suffix_name).click()
        self.page.file_suffix_select.double_click()
