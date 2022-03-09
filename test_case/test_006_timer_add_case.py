import pytest
import time
import pyautogui
from page import TimerEditPage
from datetime import date, timedelta
from public.common import get_now_str


class TestTimerAddCase:
    page = TimerEditPage(driver=None)

    @pytest.fixture(autouse=True, scope='class')
    def setup_class(self, browser):
        self.__class__.page = TimerEditPage(browser)
        self.__class__.page.timer_tab.click()

    @pytest.mark.日志埋点
    def test_add_timer(self):
        self.page.add_timer_button.click()
        self.page.add_job_button.click()
        self.page.select_job()
        self.page.add_job_save_button.click()
        self.page.timer_name_input = '定时器测试' + get_now_str()
        self.page.effect_time_input = get_now_str()
        pyautogui.press('enter')
        self.page.invalid_time_input = str(date.today()+timedelta(days=+1))+' 00:00:00'
        pyautogui.press('enter')
        self.page.add_timer_save_button.click()
