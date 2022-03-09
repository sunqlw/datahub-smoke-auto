import pytest
import time
import pyautogui
from page import TimerPage
from .data.constant_data import MESSAGE_DICT


class TestTimerAddCase:
    page = TimerPage(driver=None)

    @pytest.fixture(autouse=True, scope='class')
    def setup_class(self, browser):
        self.__class__.page = TimerPage(browser)
        self.__class__.page.timer_tab.click()

    # # @pytest.fixture(autouse=True, scope='function')
    # def setup(self):
    #     # self.page.refresh_page()
    #     # time.sleep(3)
    #     pass

    @pytest.mark.日志埋点
    def test_stop_timer(self):
        """
        完成停止、编辑、启动、删除一系列完整操作
        @return:
        """
        self.page.operate_timer('停止', timer_num=1)
        assert self.page.toast_elem.text == MESSAGE_DICT['stop_timer_success']

    @pytest.mark.日志埋点
    def test_edit_timer(self):
        # self.page.refresh_page()
        self.page.operate_timer('编辑', timer_num=1)
        self.page.update_timer_sure_button.click()
        assert self.page.toast_elem.text == MESSAGE_DICT['update_timer_success']

    @pytest.mark.日志埋点
    def test_start_timer(self):
        # self.page.refresh_page()
        self.page.operate_timer('启动', timer_num=1)
        assert self.page.toast_elem.text == MESSAGE_DICT['start_timer_success']
        # self.page.refresh_page()
        # self.page.operate_timer('停止', timer_num=1)
        # assert self.page.toast_elem.text == MESSAGE_DICT['stop_timer_success']
        # self.page.refresh_page()
        # self.page.operate_timer('删除', timer_num=1)
        # self.page.box_sure_button.click()
        # assert self.page.toast_elem.text == MESSAGE_DICT['delete_success']

