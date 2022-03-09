import pyautogui
from page import JobManagerPage


class JobManagerOperate(object):
    def __init__(self, driver):
        self.page = JobManagerPage(driver)

    def search_by_conditions(self, operate='search', **kwargs):
        # 根据传入的条件进行搜索或者点击重置按钮
        for condition in kwargs.keys():
            if condition == 'creator':
                self.page.creator_search_input = kwargs[condition]
            elif condition == 'job_id':
                self.page.job_id_search_input = kwargs[condition]
            elif condition == 'job_name':
                self.page.job_name_search_input = kwargs[condition]
            elif condition in ['start_time', 'create_time', 'effect_time', 'end_time', 'invalid_time']:
                data_map = {'start_time': '开始时间', 'end_time': '结束时间', 'create_time': '创建时间',
                            'effect_time': '生效时间', 'invalid_time': '失效时间'}
                self.page.select_time(data_map[condition], kwargs[condition][0], kwargs[condition][1])
                pyautogui.press('enter')
            elif 'status' in condition:
                if condition == 'status':
                    self.page.status_select.click()
                elif condition == 'run_status':
                    self.page.run_status_select.click()
                else:
                    self.page.timer_status_select.click()
                self.page.status_elem_in_list(kwargs[condition]).click()
        if operate == 'search':
            self.page.search_button.click()
        else:
            self.page.reset_button.click()

    def check_form_search_result(self, col_no, value):
        # 检查表格搜索结果，根据传入的列和要比较的值进行检查
        results = self.page.return_table_col(col_no=col_no)
        for result in results:
            if isinstance(value, str):
                assert value.lower() in result.lower()
            elif isinstance(value, tuple):
                # 传入的时间是xxxx-xx-xx，列表里面的时间是xxxx.xx.xx，所以需要将列表里面的时间格式转换了
                assert value[0] <= result.replace('.', '-') <= value[1]

