from poium import Element
from .job_manager_page import JobManagerPage


class TimerPage(JobManagerPage):
    add_timer_button = Element(xpath='//div[@class="time-config-list"]/a/button', describe='新建定时器按钮')
    add_timer_cancel_button = Element(xpath='//span[contains(text(),"返回")]/..', describe='新建定时器取消按钮')
    update_timer_sure_button = Element(xpath='//span[contains(text(),"更新")]/..', describe='更新定时器确定按钮')

    @staticmethod
    def operate_timer(op_type, timer_num):
        """

        @param op_type: 分为启动/停止，编辑，删除
        @param timer_num: 传入实际操作行数
        @return:
        """
        Element(xpath='//i[@title="'+op_type+'"]', index=int(timer_num)-1).click()
