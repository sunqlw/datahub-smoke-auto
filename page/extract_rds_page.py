from poium import Element
from .menu_page import MenuPage


class ExtractRdsPage(MenuPage):
    config_model_button = Element(xpath='//label[@role="radio"]', describe='配置模式按钮')
    sql_model_button = Element(xpath='//label[@role="radio"]', describe='自定义SQL按钮', index=1)
    table_button = Element(xpath='//label[@role="radio"]', describe='表按钮', index=2)
    view_button = Element(xpath='//label[@role="radio"]', describe='视图按钮', index=3)
    all_select_button = Element(class_name='el-checkbox', describe='全选按钮')
    add_table_button = Element(tag='button', describe='添加表按钮', index=2)
    remove_table_button = Element(tag='button', describe='移除表按钮', index=3)

    @staticmethod
    def table_select_elem(table_name):
        # 根据表名返回选择表列表里面表名后面的多选框元素
        return Element(xpath='//span[text()="'+table_name+'"]/following-sibling::span[1]')

    @staticmethod
    def table_selected_elem(table_name):
        # 根据表名返回已选表列表里面表名后面的多选框元素
        return Element(xpath='//span[text()="' + table_name + '"]/following-sibling::span[1]', index=-1)
