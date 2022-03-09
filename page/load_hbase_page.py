from poium import Element
from .menu_page import MenuPage


class LoadHbasePage(MenuPage):
    space_select = Element(xpath='//input[@placeholder="请选择命名空间"]', describe='命名空间下拉框')

    @staticmethod
    def add_rowkey_button(index=1):
        # 根据index返回对应行后面的新增rowkey按钮
        return Element(class_name='add-icon', describe='新增rowkey按钮', index=int(index)-1)

    @staticmethod
    def remove_rowkey_button(index=1):
        # 根据index返回对应行后面的移除rowkey按钮
        return Element(class_name='remove-icon', describe='移除rowkey按钮', index=int(index)-1)

    @staticmethod
    def rowkey_select(index):
        # 根据index返回对应行数的行键下拉框
        return Element(xpath='//span[text()="组合字段'+str(index)+'："]/../div', describe='行键下拉框')

    @staticmethod
    def field_in_list_elem(field_name):
        # 根据字段名返回下拉列表中的字段元素
        return Element(xpath='//span[text()="'+field_name+'"]/..', index=-1)