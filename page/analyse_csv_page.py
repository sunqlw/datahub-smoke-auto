from poium import Element
from .menu_page import MenuPage


class AnalyseCsvPage(MenuPage):
    file_suffix_select = Element(class_name='el-select--mini', describe='文件后缀下拉框')
    file_suffix_input = Element(xpath='//div[@class="el-select__tags"]/input', describe='文件后缀输入框')

    @staticmethod
    def file_suffix_elem(suffix_name):
        # 根据后缀名返回可点击的后缀元素
        return Element(xpath='//li/span[text()="'+suffix_name+'"]/..')