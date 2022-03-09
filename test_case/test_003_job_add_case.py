import os.path

import pytest
import time
import traceback
from page import JobEditPage
from selenium.common.exceptions import NoSuchElementException
from public.common import get_json_data, get_now_str
from os.path import dirname, abspath
from public import logging
from .data.constant_data import COMP_DICT, RES_TYPE_DICT, MODEL_NAME_DICT, MESSAGE_DICT
from .data.res_data import RES_DATA_DICT
from .operate import JobAddOperate, CsvOperate, HdfsLoadOperate, HbaseLoadOperate


base_path = dirname(abspath(__file__))
rds_exct_name = COMP_DICT['rds_exct']
local_exct_name = COMP_DICT['local_exct']
excel_name = COMP_DICT['excel']
csv_name = COMP_DICT['csv']
rds_load_name = COMP_DICT['rds_load']
hive_load_name = COMP_DICT['hive_load']
hdfs_load_name = COMP_DICT['hdfs_load']
hbase_load_name = COMP_DICT['hbase_load']
mysql_db_name = RES_DATA_DICT['mysql']['db_name']
oracle_db_name = RES_DATA_DICT['oracle']['db_name']


class TestJobAddCase:
    page = JobEditPage(driver=None)
    op = JobAddOperate(driver=None)
    op_csv = CsvOperate(driver=None)
    op_hdfs_load = HdfsLoadOperate(driver=None)
    op_hbase_load = HbaseLoadOperate(driver=None)

    @pytest.fixture(autouse=True, scope='class')  # 为什么加了这句话，就能拿到browser了
    def setup_class(self, browser):
        self.__class__.page = JobEditPage(browser)
        self.__class__.op = JobAddOperate(browser)
        self.__class__.op_csv = CsvOperate(browser)
        self.__class__.op_hdfs_load = HdfsLoadOperate(browser)
        self.__class__.op_hbase_load = HbaseLoadOperate(browser)
        self.__class__.page.refresh_page()
        self.__class__.page.job_manager_button.click()

    def setup(self):
        self.op.click_job_manager()

    # 新建任务编辑rds抽取组件通用操作
    def edit_rds_exct(self, db_name, tables, res_type=None):
        self.op.comp_operate('double_click', rds_exct_name)
        self.op.select_res_and_db(db_name, res_type)
        self.op.select_table(tables)
        self.op.comp_operate('sure')

    # 新建任务编辑本地文件抽取组件通用操作
    def edit_local_exct(self, *file_list):
        self.op.comp_operate('double_click', local_exct_name)
        for file_name in file_list:
            self.page.file_button.click()
            self.page.upload_file(os.path.join(base_path, 'data', file_name))
        # 理论上需要等到文件都上传完成了再点确定，但是测试文件都很小，先这样
        time.sleep(1)
        self.op.comp_operate('sure')

    # 新建任务编辑excel解析组件通用操作
    def edit_excel(self):
        self.op.comp_operate('double_click', excel_name)
        self.page.file_button.click()
        self.page.fold_file_button.is_displayed()
        self.op.comp_operate('sure')

    # 新建任务编辑csv解析组件通用操作
    def edit_csv(self, suffix_list):
        self.op.comp_operate('double_click', csv_name)
        self.op_csv.select_suffix(*suffix_list)
        self.page.file_button.click()
        time.sleep(1)
        self.op.comp_operate('sure')

    # 新建任务编辑rds加载组件通用操作
    def edit_rds_load(self, db_name, res_type=None, tab_name=None, clear=True):
        self.op.comp_operate('double_click', rds_load_name)
        self.op.select_res_and_db(db_name, res_type)
        if 'tab_name':
            self.op.comp_operate('switch')
            if clear:
                self.page.tab_name_input.clear()
            self.page.tab_name_input = tab_name
        self.op.comp_operate('sure')

    # 新建任务编辑hdfs加载组件通用操作
    def edit_hdfs_load(self, path, switch_type=True):
        self.op.comp_operate('double_click', hdfs_load_name)
        self.op.select_res()
        if switch_type:
            self.op_hdfs_load.switch_file_type()
        self.op_hdfs_load.config_path(path)
        self.op.comp_operate('sure')

    # 新建任务编辑hive加载组件通用操作
    def edit_hive_load(self, db_name):
        self.op.comp_operate('double_click', hive_load_name)
        self.op.select_res_and_db(db_name)
        self.page.wait_elem_not_visibility(self.page.data_loading_sign, 20)
        self.op.comp_operate('sure')

    # 保存任务并启动任务等待任务运行完成
    def save_and_run_job(self):
        self.op.menu_operate('save')
        assert self.page.compare_toast(MESSAGE_DICT['save_success'])
        self.op.menu_operate('start')
        self.op.check_jon_run_success()

    def test_mysql_to_oracle(self):
        """
        用例名称：新建mysql到oracle的单表任务
        步骤：1.新建空白画布 2.拖拽rds抽取和rds加载组件 3.编辑rds抽取组件，选择mysql下的某个表，点击确定
        4.编辑rds加载组件，选择oracle的某个数据库，点击确定 5.保存任务 6.运行任务
        检查点：1.显示启动成功 2.任务三分钟内运行成功
        """
        job_name = 'mysql to oracle ' + get_now_str()
        self.op.add_job_basic(MODEL_NAME_DICT['new'], job_name, '这是一个mysql到oracle的任务，通过web自动化创建')
        self.op.drag_and_connect(rds_exct_name, rds_load_name)
        tabs = ['test1']
        self.edit_rds_exct(mysql_db_name, tabs)
        self.edit_rds_load(oracle_db_name, RES_TYPE_DICT['oracle'])
        self.save_and_run_job()

    # 通过模板新建mysql到hive的任务
    def test_mysql_to_hive(self):
        """
        用例名称：新建mysql到hive的任务
        步骤：1.新建mysql到hive的模板任务 2.编辑rds抽取组件，选择mysql下的某个表，点击确定
        3.编辑hive加载组件，选择hive的某个数据库，点击确定 5.保存任务 6.运行任务
        检查点：1.显示启动成功 2.任务三分钟内运行成功
        """
        job_name = 'mysql to hive ' + get_now_str()
        self.op.add_job_basic(MODEL_NAME_DICT['rds_to_hive'], job_name, '这是一个mysql到hive的任务，通过web自动化创建')
        tabs = ['test1', 'student_info']
        self.edit_rds_exct('datahub_web_auto', tabs)
        self.edit_hive_load('datahub01')
        self.save_and_run_job()

    def test_mysql_to_hbase(self):
        job_name = 'mysql to hbase ' + get_now_str()
        self.op.add_job_basic(MODEL_NAME_DICT['rds_to_hbase'], job_name, '这是一个mysql到hbase的任务，通过web自动化创建')
        tabs = ['student_info']
        self.edit_rds_exct('datahub_web_auto', tabs)
        self.op.comp_operate('double_click', hbase_load_name)
        self.op.select_res_and_db('default', RES_TYPE_DICT['hbase'])
        self.op.comp_operate('switch')
        self.op_hbase_load.select_rowkey('id', 'sex')
        self.op.comp_operate('sure')
        self.save_and_run_job()

    def test_local_excel_to_mysql(self):
        """
        用例名称：新建本地excel到mysql的任务
        步骤：1.上传本地excel文件 2.编辑excel解析组件，获取表单 3.编辑rds加载组件，选择mysql下的某个数据库 4.保存任务运行任务
        检查点：1.显示启动成功 2.任务三分钟内运行成功
        """
        job_name = 'local excel to mysql ' + get_now_str()
        self.op.add_job_basic(MODEL_NAME_DICT['new'], job_name, '这是一个本地上传excel到mysql的任务，通过web自动化创建')
        self.op.drag_and_connect(local_exct_name, excel_name, rds_load_name)
        self.edit_local_exct('学生表.xlsx')
        self.edit_excel()
        self.edit_rds_load(mysql_db_name)
        self.save_and_run_job()

    def test_local_csv_to_mysql(self):
        """
        用例名称：新建本地csv到mysql的任务
        步骤：1.上传本地csv文件 2.编辑csv解析组件，获取文件 3.编辑rds加载组件，选择mysql下的某个数据库 4.保存任务运行任务
        检查点：1.显示启动成功 2.任务三分钟内运行成功
        """
        job_name = 'local csv to mysql ' + get_now_str()
        self.op.add_job_basic(MODEL_NAME_DICT['new'], job_name, '这是一个本地上传csv到mysql的任务，通过web自动化创建')
        self.op.drag_and_connect(local_exct_name, csv_name, rds_load_name)
        self.edit_local_exct('学生信息.txt')
        self.edit_csv(['txt'])
        self.edit_rds_load(mysql_db_name, tab_name='csv1')
        self.save_and_run_job()

    def test_local_csv_to_hdfs(self):
        job_name = 'local csv to hdfs ' + get_now_str()
        self.op.add_job_basic(MODEL_NAME_DICT['new'], job_name, '这是一个本地上传csv到hdfs的任务，通过web自动化创建')
        self.op.drag_and_connect(local_exct_name, csv_name, hdfs_load_name)
        self.edit_local_exct('学生信息.txt')
        self.edit_csv(['txt'])
        self.edit_hdfs_load('/tmp/datahub')
        self.save_and_run_job()


