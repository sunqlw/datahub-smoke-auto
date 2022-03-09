import pytest
from page import ResPage
from public.common import get_json_data
from os.path import dirname, abspath
from conftest import capture_screenshots
from .data.constant_data import RES_TYPE_DICT
from time import sleep

base_path = dirname(dirname(abspath(__file__)))
message_data_dict = get_json_data(base_path + "/test_case/data/message.json")


class TestResSearchCase:

    page = ResPage(driver=None)

    @pytest.fixture(autouse=True, scope='class')
    def setup_class(self, browser):
        self.__class__.page = ResPage(browser)
        self.__class__.page.res_manager_button.click()
        self.__class__.page.res_name_search_input.is_displayed()
        self.__class__.page.refresh_page()

    def test_search_by_res_name(self):
        """
        用例名称：根据资源名搜索关键字不存在的资源
        步骤：1.输入一个不存在的关键字 2.点击搜索
        检查点：1.列表里面显示无数据
        """
        self.search_common(res_name='关键字不存在的')
        self.check_search_result(no_data=True)

    # res_type_list = ['mysql', 'oracle', 'sqlserver', 'db2', 'postgresql', 'hana', 'tidb', 'dm', 'ftp', 's3',
    #                  'hdfs', 'hive', 'hbase']

    res_type_list = ['mysql']

    @pytest.mark.parametrize('res_type', res_type_list, ids=res_type_list)
    def test_search_by_res_type(self, res_type):
        """
        用例名称：根据资源类型搜索
        步骤：1.选择资源类型 2.点击搜索
        检查点：1.列表里的都是所搜索类型的资源
        """
        self.search_common(res_type)
        self.check_search_result(res_type=res_type)
        capture_screenshots('搜索mysql类型.png')

    @pytest.mark.日志埋点
    def test_search(self):
        """
        用例名称：根据资源类型搜索
        步骤：1.选择资源类型 2.点击搜索
        检查点：1.列表里的都是所搜索类型的资源
        """
        res_name = 'mysql'
        res_type = 'oracle'
        # self.search_common(res_type=res_type)
        # self.check_search_result(res_type=res_type)
        # self.search_common(res_name=res_name)
        # self.check_search_result(res_name=res_name)
        self.search_common(res_type=res_type, res_name=res_name)
        self.check_search_result(no_data=True)

    def test_delete_res_cancel(self):
        """
        用例名称：取消删除资源验证
        步骤：1.点击第一行数据的删除按钮 2.弹窗后点击取消按钮
        检查点：1.弹窗消失 2.数据没有删除
        """
        self.page.table_tr1_td1.refresh_element()
        res_name_first = self.page.table_tr1_td1.text
        self.page.res_delete_button.click()
        self.page.box_operate('cancel')
        self.page.wait_elem_not_visibility(self.page.box_text_ele)
        res_name_check = self.page.table_tr1_td1.text
        assert res_name_first == res_name_check

    @pytest.mark.日志埋点
    def test_delete_res_sure(self):
        """
        用例名称：确定删除资源验证
        步骤：1.点击第一行数据的删除按钮 2.弹窗后点击确定按钮
        检查点：1.弹窗消失 2.toast弹窗提示删除成功 3.数据从列表中移除
        """
        self.page.table_tr1_td1.refresh_element()
        res_name_first = self.page.table_tr1_td1.text
        self.page.res_delete_button.click()
        self.page.box_operate('sure')
        self.page.wait_elem_not_visibility(self.page.box_text_ele)
        self.page.toast_elem.is_displayed()
        assert self.page.toast_elem.text == '删除成功'
        res_name_check = self.page.table_tr1_td1.text
        assert res_name_first != res_name_check

    # 搜索通用方法，可根据资源名或资源类型搜索
    def search_common(self, res_type=None, res_name=None):
        self.page.reset_button.click()
        if res_name:
            self.page.res_name_search_input = res_name
        if res_type:
            self.page.res_type_search_select.click()
            self.page.click_res_type(res_type=res_type)
        self.page.search_button.click()

    # 检查搜索结果
    def check_search_result(self, no_data=False, res_name=None, res_type=None):
        if no_data:
            assert self.page.no_data_sign.text == '暂无数据'
        if res_name:
            results = self.page.return_table_col(self.page.table_ele, 1)
            for x in range(len(results)):
                assert res_name.lower() in results[x].lower()
        if res_type:
            results = self.page.return_table_col(self.page.table_ele, 2)
            for y in range(len(results)):
                assert RES_TYPE_DICT[res_type] == results[y]

