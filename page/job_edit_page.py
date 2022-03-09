from poium import Element
from .extract_component_page import ExtractComponentPage
from .load_component_page import LoadComponentPage
from .transform_component_page import TransformComponentPage
from .analyse_excel_page import AnalyseExcelPage
from .analyse_csv_page import AnalyseCsvPage


class JobEditPage(ExtractComponentPage, LoadComponentPage, TransformComponentPage, AnalyseExcelPage, AnalyseCsvPage):
    add_job_button = Element(xpath='//button[@type="button"]', describe='新建任务按钮', index=2)
    add_new_canvas_button = Element(class_name='new-box', describe='新建空白画布按钮')
    job_name_input = Element(xpath='//input[@placeholder="请输入任务名"]', describe='任务名输入框')
    job_describe_input = Element(tag='textarea', describe='描述输入框')
    add_sure_button = Element(xpath='//div[@class="btn-wrap own-btn-wrap"]/button[2]', describe='新建任务确定按钮')
    add_cancel_button = Element(xpath='//div[@class="btn-wrap own-btn-wrap"]/button[1]', describe='新建任务取消按钮')
    add_close_button = Element(xpath='//button[@aria-label="Close"]', describe='新建任务右上角×按钮')
    work_place = Element(id_='workplace', describe='画布')
    job_run_button = Element(xpath='//div[@class="tool-bar flexSpaceBetween"]/div[1]/div[1]', describe='任务启停按钮')
    job_save_button = Element(xpath='//div[@class="tool-bar flexSpaceBetween"]/div[1]/div[2]', describe='任务保存按钮')
    clear_button = Element(xpath='//div[@class="tool-bar flexSpaceBetween"]/div[1]/div[3]', describe='清空画布按钮')
    run_record_button = Element(xpath='//div[@class="tool-bar flexSpaceBetween"]/div[1]/div[4]', describe='运行记录按钮')
    basic_conf_button = Element(id_='tab-first', describe='抽取配置/加载配置按钮')
    data_conf_button = Element(id_='tab-second', describe='数据配置按钮')
    file_button = Element(class_name='isActive', describe='添加文件/获取文件按钮')
    res_select = Element(xpath='//input[@placeholder="请选择资源连接"]', describe='组件资源连接下拉框')
    first_res = Element(xpath='/html/body/div[last()]/div[1]/div[1]/ul/li[1]', describe='资源连接下拉框中第一个资源')
    db_select = Element(xpath='//input[@placeholder="请选择数据库"]', describe='数据库下拉框')
    comp_sure_button = Element(tag='button', describe='组件确定按钮', index=-1)
    comp_cancel_button = Element(tag='button', describe='组件取消按钮', index=-2)
    comp_close_button = Element(tag='button', describe='组件右上角×按钮')
    rds_type_select = Element(xpath='//input[@placeholder="请选择数据库类型"]', describe='数据库类型下拉框')
    run_status_sign = Element(xpath='//tr[@class="el-table__row"]/td[4]/div/span', describe='运行状态')
    data_loading_sign = Element(class_name='el-icon-loading', describe='数据加载中标识')

    @staticmethod
    def model_job_elem(model_name):
        # 根据模板任务名返回模板任务元素，model_name必须是标准的模板名
        return Element(xpath='//div[text()="'+model_name+'"]/../..', describe='模板任务'+model_name)

    @staticmethod
    def canvas_comp_elem(comp_name):
        # 根据组件名返回画布上的组件元素
        return Element(xpath='//div[@alias="'+comp_name+'"]', describe='画布上的'+comp_name+'组件')

    @staticmethod
    def comp_delete_elem(comp_name):
        # 根据组件名返回画布上的组件的删除按钮
        return Element(xpath='//div[@alias="'+comp_name+'"]/div[1]/div[1]/i[2]', describe=comp_name+'组件删除按钮')

    @staticmethod
    def point_elem(comp_name, position):
        """
        根据组件名和位置返回该组件的左边的连线点或者右边的连线点
        comp_name: 组件名称，会根据组件名称去定位到组件所在元素
        position: 位置，用left和right来表示是想要坐节点还是右节点
        """
        position_num = '1'
        if position == 'left':
            position_num = '2'
        return Element(xpath='//div[@alias="' + comp_name + '"]/following-sibling::div[' + position_num + ']')

    @staticmethod
    def db_elem(db_name):
        # 根据数据库名返回数据库元素
        return Element(xpath='//*[@title="'+db_name+'"]')


    @staticmethod
    def db_type_elem(db_type):
        # 根据数据库类型返回数据库类型元素，db_type必须是规范的类型名，否则会找不到元素
        return Element(xpath='//li[@title="'+db_type+'"]', describe='数据库类型'+db_type)

    @staticmethod
    def menu_comp_elem(comp_name):
        # 根据组件名返回左侧菜单组件元素
        return Element(xpath='//span[text()="'+comp_name+'"]', describe=comp_name+'组件')

