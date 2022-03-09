from poium import Element
from .menu_page import MenuPage


class AnalyseExcelPage(MenuPage):
    open_file_button = Element(class_name='expand-add-icon', describe='文件前面的+按钮')
    fold_file_button = Element(class_name='expand-remove-icon', describe='文件前面的-按钮')