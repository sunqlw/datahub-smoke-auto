from poium import Element
from .job_manager_page import JobManagerPage


class RunRecordPage(JobManagerPage):
    run_detail_button = Element(class_name='leapicon-detail', describe='运行详情按钮')
