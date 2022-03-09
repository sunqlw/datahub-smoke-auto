import pytest
import time
from public.common import get_now_str
from .operate import JobManagerOperate


class TestRunRecordCase:
    op_jm = JobManagerOperate(driver=None)

    @pytest.fixture(autouse=True, scope='class')
    def setup_class(self, browser):
        self.__class__.op_jm = JobManagerOperate(browser)

    def test_search_by_time(self):
        """
        测试
        """
        self.op_jm.search_by_conditions(create_time=(get_now_str(), get_now_str()))
        time.sleep(2)
