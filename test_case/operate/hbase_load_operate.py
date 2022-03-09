import time
from page import JobEditPage


class HbaseLoadOperate(object):
    def __init__(self, driver):
        self.page = JobEditPage(driver)

    def select_rowkey(self, *rowkey_list):
        self.page.rowkey_select(1).click()
        self.page.field_in_list_elem(rowkey_list[0]).click()
        for index in range(1, len(rowkey_list)):
            self.page.add_rowkey_button().click()
            self.page.rowkey_select(index+1).click()
            self.page.field_in_list_elem(rowkey_list[index]).click()

