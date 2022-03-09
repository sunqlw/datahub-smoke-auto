import time
from page import JobEditPage


class HdfsLoadOperate(object):
    def __init__(self, driver):
        self.page = JobEditPage(driver)

    def switch_file_type(self):
        self.page.file_type_select.click()
        if 'selected' in self.page.file_type_binary.get_attribute('class'):
            self.page.file_type_textfile.click()
        else:
            self.page.file_type_binary.click()

    def config_path(self, path=''):
        self.page.path_config_button.click()
        path_list = path.split('/')
        path_list[0] = '/'
        for path_name in path_list:
            self.page.folder_operate_elem(path_name).click()
        self.page.folder_elem(path_list[-1]).click()
