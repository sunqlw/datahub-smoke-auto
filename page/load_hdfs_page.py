from poium import Element
from .menu_page import MenuPage


class LoadHdfsPage(MenuPage):
    file_type_select = Element(class_name='el-select--mini', index=1, describe='文件类型下拉框')
    file_type_binary = Element(xpath='//li[@title="二进制文件加载"]', describe='二进制文件加载')
    file_type_textfile = Element(xpath='//li[@title="TextFile"]', describe='TextFile')
    path_config_button = Element(xpath='//span[text()="路径配置"]/..', describe='路径配置按钮')
    path_clear_button = Element(xpath='//span[text()="清空路径"]/..', describe='清空路径按钮')

    @staticmethod
    def folder_operate_elem(folder_name):
        # 根据传入的文件夹名返回文件夹前面的展开收起按钮
        return Element(xpath='//span[@title="'+folder_name+'"]/../preceding-sibling::span', describe='文件夹展开收起按钮')

    @staticmethod
    def folder_elem(folder_name):
        # 根据传入的文件夹名返回文件夹对象
        return Element(xpath='//span[@title="' + folder_name + '"]', describe='文件夹元素')
