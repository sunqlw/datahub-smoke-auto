import os.path
import time
import pytest
import sys
from page import ResEditPage
from public.common import get_json_data, get_now_str
from os.path import dirname, abspath
from selenium.common import exceptions
from public import logging
from .data.constant_data import MESSAGE_DICT
from .data.res_data import RES_DATA_DICT
from config import RunConfig

sys.path.insert(0, dirname(dirname(abspath(__file__))))  # 这行代码在干啥？？
base_path = dirname(dirname(abspath(__file__)))


# 添加资源前点击新建资源按钮并填写资源名和填写完参数后点击测试连接和保存按钮
def deco_add_res(func):
    def wrapper(self, *args, **kwargs):
        self.click_add_res_button()
        self.page.res_name_input = kwargs['res_name']
        f = func(self, *args, **kwargs)
        self.connect_success_and_save()
        return f
    return wrapper


class TestResEditorCase:

    page = ResEditPage(driver=None)

    @pytest.fixture(autouse=True, scope='class')  # 为什么加了这句话，就能拿到browser了，
    # @classmethod 为什么fixture不能作用在类方法上
    def setup_class(self, browser):
        self.__class__.page = ResEditPage(browser)
        self.__class__.page.res_manager_button.click()
        self.__class__.page.res_name_search_input.is_displayed()
        self.__class__.page.refresh_page()

    res_type_list = ['mysql', 'oracle', 'sqlserver', 'db2', 'postgresql', 'tidb', 'dm', 'ftp', 'sftp', 's3',
                     'hdfs', 'hive', 'hive_ha', 'hbase']

    # res_type_list = ['mysql', 'oracle', 'sqlserver', 'db2', 'postgresql', 'tidb', 'dm']
    # res_type_list = ['ftp']

    # @pytest.mark.skip
    # @pytest.mark.smoke
    @pytest.mark.parametrize('res_type', res_type_list, ids=res_type_list)
    def test_add(self, res_type):
        """
        用例名称：添加资源
        步骤：1.填写完相关参数 2.点击测试连接，等待连接通过后点击保存按钮
        检查点：1.toast提示保存成功 2.表格第一列为新增的资源名
        """
        params = RES_DATA_DICT[res_type]
        params['res_name'] = res_type + get_now_str()
        if 'ftp' in res_type:
            self.add_ftp_common(**params)
        elif res_type == 's3':
            self.add_s3_common(**params)
        elif res_type == 'hdfs':
            self.add_hdfs_common(**params)
        elif 'hive' in res_type:
            self.add_hive_common(**params)
        elif 'hbase' in res_type:
            self.add_hbase_common(**params)
        else:
            self.add_rds_common(**params)
        self.check_add_success(params['res_name'])

    @pytest.mark.smoke
    def test_add_res_name_exist(self):
        """
        用例名称：新建资源重名检查
        步骤：1.资源连接名填写一个已存在的名字，填写完相关参数 2.点击测试连接，等待连接通过后点击保存按钮
        检查点：1.保存失败，弹窗提示资源名已存在
        """
        params = RES_DATA_DICT['mysql']
        self.page.table_tr1_td1.refresh_element()
        params['res_name'] = self.page.table_tr1_td1.text
        self.add_rds_common(**params)
        assert self.page.box_text_ele.text == MESSAGE_DICT['res_name_exist']

    @pytest.mark.日志埋点
    def test_add_mysql(self):
        """
        用例名称：添加mysql资源
        步骤：
        1.资源类型选择mysql，填写完相关参数
        2.点击测试连接，等待连接通过后点击保存按钮
        检查点：
        """
        params = RES_DATA_DICT['mysql']
        params['res_name'] = 'mysql-ui-' + get_now_str()
        self.add_rds_common(**params)
        self.check_add_success(params['res_name'])

    @pytest.mark.日志埋点
    def test_editor(self):
        self.page.res_edit_button.click()
        self.connect_success_and_save()
        assert self.page.toast_elem.text == MESSAGE_DICT['update_success']

    # 点击新增资源按钮
    def click_add_res_button(self):
        # 增加try，如果新建资源按钮不能点击，则刷新界面
        # 相当于一个让测试用例更稳定的做法
        try:
            self.page.add_res_button.click()
        except exceptions.ElementClickInterceptedException:
            self.page.refresh_page()
            self.page.add_res_button.click()

    # 点击测试连接等待通过后点击保存按钮
    def connect_success_and_save(self):
        self.page.connect_button.click()
        # 在这里应该增加判断，如果出现了测试连接失败，则应该直接抛出异常了
        self.page.connect_finish_sign.timeout = 10
        self.page.connect_finish_sign.is_displayed()
        # 如果是测试连接失败，则直接判定为失败
        if 'close' in self.page.connect_finish_sign.get_attribute('class'):
            assert False
        self.page.save_button.click()

    # 根据zk串输入zk地址通用方法
    def input_zk_host(self, zk_str):
        zk_list = zk_str.split(',')
        if len(zk_list) >= 1:
            self.page.first_zk_input = zk_list[0]
        if len(zk_list) >= 2:
            self.page.zk_add_button.click()
            self.page.second_zk_input = zk_list[1]
        if len(zk_list) >= 3:
            self.page.zk_add_button.click()
            self.page.third_zk_input = zk_list[2]
        if len(zk_list) >= 4:
            print("抛出异常，最多只支持3个zk地址")

    # 选择类型
    def select_type(self, res_type):
        if res_type != 'mysql':
            self.page.res_type_select.click()
            self.page.click_res_type(res_type=res_type, ops='add')

    # 正常添加关系型数据库的通用方法
    @deco_add_res
    def add_rds_common(self, **kwargs):
        self.select_type(kwargs['type'])
        if kwargs['type'] in ['oracle', 'db2']:
            self.page.db_server_input = kwargs['server_name']
        self.page.db_host_input = kwargs['host']
        self.page.db_port_input = kwargs['port']
        self.page.db_username_input = kwargs['username']
        self.page.db_password_input = kwargs['password']

    @deco_add_res
    def add_ftp_common(self, **kwargs):
        self.select_type(res_type='ftp')
        if kwargs['type'] == 'sftp':
            self.page.protocol_select.click()
            self.page.protocol_sftp.click()
        self.page.ftp_host_input = kwargs['host']
        self.page.ftp_port_input = kwargs['port']
        self.page.ftp_username_input = kwargs['username']
        self.page.ftp_password_input = kwargs['password']

    @deco_add_res
    def add_s3_common(self, **kwargs):
        self.select_type('s3')
        self.page.s3_accesskey_input = kwargs['accesskey']
        self.page.s3_secretkey_input = kwargs['secretkey']
        self.page.s3_region_select.click()
        if kwargs['region'] == 'china':
            self.page.focus(self.page.s3_region_china)
            self.page.s3_region_china.click()
        else:
            print("抛出异常，暂不支持其他区域")

    @deco_add_res
    def add_hdfs_common(self, **kwargs):
        self.select_type('hdfs')
        self.page.core_site_upload_button.click()
        core_site_file_path = os.path.join(base_path, 'test_case', 'data', RunConfig.env, kwargs['core-site'])
        hdfs_site_file_path = os.path.join(base_path, 'test_case', 'data', RunConfig.env, kwargs['hdfs-site'])
        self.page.upload_file(core_site_file_path)
        self.page.hdfs_site_upload_button.click()
        self.page.upload_file(hdfs_site_file_path)
        self.page.hdfs_username_input = kwargs['username']

    @deco_add_res
    def add_hive_common(self, **kwargs):
        self.select_type('hive')
        self.page.hive_hdfs_select.click()
        self.page.hive_bind_hdfs.click()
        self.page.hive_username_input = kwargs['username']
        if kwargs['service_model'] == 'HA模式':
            self.page.hive_service_model_select.click()
            self.page.hive_ha_service.click()
            self.page.hive_space_name_input = kwargs['space_name']
            self.input_zk_host(kwargs['zk_host'])
        elif kwargs['service_model'] == '普通模式':
            self.page.hive_host_input = kwargs['host']
        else:
            print("抛出异常，只支持HA模式和普通模式")
        self.page.hive_port_input = kwargs['port']

    @deco_add_res
    def add_hbase_common(self, **kwargs):
        self.select_type('hbase')
        self.page.hbase_username_input = kwargs['username']
        self.input_zk_host(kwargs['zk_host'])
        self.page.hbase_port_input = kwargs['port']
        self.page.znode_input = kwargs['znode']

    # 判断资源是否添加成功
    def check_add_success(self, res_name):
        assert self.page.toast_elem.text == MESSAGE_DICT['save_success']
        self.page.table_tr1_td1.is_displayed()
        assert self.page.table_tr1_td1.text == res_name



