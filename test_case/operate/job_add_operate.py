import time
from page import JobEditPage
from ..data.constant_data import MESSAGE_DICT, COMP_DICT

position_dict = {
    COMP_DICT['rds_exct']: (380, 400),
    COMP_DICT['local_exct']: (380, 400),
    COMP_DICT['excel']: (550, 400),
    COMP_DICT['csv']: (550, 400),
    COMP_DICT['rds_load']: (800, 400),
    COMP_DICT['hive_load']: (800, 400),
    COMP_DICT['hdfs_load']: (800, 400)
}


class JobAddOperate(object):
    def __init__(self, driver):
        self.page = JobEditPage(driver)

    def click_job_manager(self):
        self.page.job_manager_button.click()

    # 新建任务基本信息填写
    def add_job_basic(self, model_name, job_name, job_describe='', op='sure'):
        self.page.add_job_button.click()
        self.page.model_job_elem(model_name).click()
        self.page.job_name_input = job_name
        if job_describe:
            self.page.job_describe_input = job_describe
        if op == 'sure':
            self.page.add_sure_button.click()
        elif op == 'cancel':
            self.page.add_cancel_button.click()
        else:
            self.page.add_close_button.click()

    # 拖拽元素
    def drag_comp(self, *comp_name_list):
        for comp_name in comp_name_list:
            elem = self.page.menu_comp_elem(comp_name)
            if comp_name in [COMP_DICT['excel'], COMP_DICT['csv'], COMP_DICT['table_join'], COMP_DICT['hbase_load'],
                             COMP_DICT['hive_load'], COMP_DICT['hdfs_load'], COMP_DICT['rds_load']]:
                self.page.focus(elem)
            self.page.drag_and_drop_by_offset_by_pyautogui(elem, *position_dict[comp_name])

    # 将传进来的组件依次连线
    def connection_point(self, *comps):
        for x in range(len(comps)-1):
            self.page.connect_elem(self.page.point_elem(comps[x], 'right'), self.page.point_elem(comps[x+1], 'left'))

    # 拖拽组件并连线
    def drag_and_connect(self, *comp_name_list):
        self.drag_comp(*comp_name_list)
        self.connection_point(*comp_name_list)

    # 组件操作，根据操作类型来判断，提供组件的通用操作，比如双击、删除、确定取消关闭按钮的点击、切换两个tab页等
    def comp_operate(self, op, comp_name=None):
        if op == 'sure':
            self.page.comp_sure_button.click()
        elif op == 'cancel':
            self.page.comp_cancel_button.click()
        elif op == 'close':
            self.page.comp_close_button.click()
        elif op == 'double_click':
            self.page.canvas_comp_elem(comp_name).double_click()
        elif op == 'delete':
            self.page.comp_delete_elem(comp_name).click()
            self.page.box_sure_button.click()
        elif op == 'switch':
            if 'is-active' in self.page.basic_conf_button.get_attribute('class'):
                self.page.data_conf_button.click()
            else:
                self.page.basic_conf_button.click()
        else:
            raise Exception('操作类型只能为sure、cancel、close')

    # 选择资源连接
    def select_res(self, res_name=''):
        self.page.res_select.click()
        if res_name:
            self.page.res_select = res_name
        self.page.first_res.click()

    # 选择资源链接和数据库，资源类型只有为非mysql的数据库类型才需要传值
    def select_res_and_db(self, db_name, res_type=None, res_name=''):
        if res_type and res_type != 'HBase':
            self.page.rds_type_select.click()
            self.page.db_type_elem(res_type).click()
        self.select_res(res_name)
        if res_type == 'HBase':
            self.page.space_select.click()
        else:
            self.page.db_select.click()
        db_elem = self.page.db_elem(db_name)
        self.page.focus(db_elem)
        db_elem.click()

    # 根据表列表选择表，根据操作判断是添加还是移除
    def select_table(self, table_list, op='add'):
        if op == 'add':
            for table_name in table_list:
                self.page.table_select_elem(table_name).click()
            self.page.add_table_button.click()
        if op == 'remove':
            for table_name in table_list:
                self.page.table_selected_elem(table_name).click()
            self.page.remove_table_button.click()

    def menu_operate(self, op, confirm=None):
        """
        菜单栏操作，根据操作判断是启停任务、保存、清空画布、查看运行记录等
        params:
        op:用于控制点击什么按钮，值可以为start、stop、save、record，输入其他报错
        confirm:用于控制二次弹窗执行什么操作，值可以为sure、cancel、close，输入其他值默认执行close操作
        """
        if op in ['start', 'stop']:
            self.page.job_run_button.click()
        elif op == 'save':
            self.page.job_save_button.click()
        elif op == 'clear':
            self.page.clear_button.click()
        elif op == 'record':
            self.page.run_record_button.click()
        else:
            raise Exception('操作的值只能为start、stop、save、record中的一个')
        if confirm:
            self.page.box_operate(confirm)

    # 判断任务是否运行成功
    def check_jon_run_success(self):
        assert self.page.compare_toast(MESSAGE_DICT['run_success'])
        # 循环遍历检查运行状态的值，如果检查到时失败，就抛出异常，如果是运行中则重新检查
        sign = False
        for x in range(180):
            status = self.page.run_status_sign.text
            if status == '失败':
                break
            elif status == '成功':
                sign = True
                break
            else:
                time.sleep(1)
                continue
        assert sign
