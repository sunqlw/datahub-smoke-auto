from poium import Element
from .timer_page import TimerPage


class TimerEditPage(TimerPage):
    timer_name_input = Element(xpath='//input[@placeholder="请输入定时器名"]', describe='定时器名输入框')
    effect_time_input = Element(xpath='//label[contains(text(),"生效时间")]/following-sibling::div[1]/div/input[1]',
                                describe='生效时间输入框')
    invalid_time_input = Element(xpath='//label[contains(text(),"失效时间")]/following-sibling::div[1]/div/input[1]',
                                 describe='失效时间输入框')
    add_job_button = Element(xpath='//span[contains(text(),"添加任务")]/..', describe='添加任务按钮')
    add_job_save_button = Element(xpath='//span[contains(text(),"保存")]/..', index=1, describe='添加任务保存按钮')
    add_job_cancel_button = Element(xpath='//span[contains(text(),"取消")]/..', index=1, describe='添加任务取消按钮')
    add_timer_save_button = Element(xpath='//span[contains(text(),"保存")]/..', describe='新建定时器保存按钮')

    @staticmethod
    def select_job(job_col='all'):
        """
        @param job_col: all表示全选，其他数字表示对应选择第几行的任务
        """
        if job_col == 'all':
            Element(class_name='el-checkbox').click()
        else:
            Element(class_name='el-checkbox', index=int(job_col)).click()
