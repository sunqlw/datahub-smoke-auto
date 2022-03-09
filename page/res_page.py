from poium import Element
from .menu_page import MenuPage


class ResPage(MenuPage):
    res_name_search_input = Element(xpath='//input[@placeholder="请输入资源名"]', describe='资源名搜索框')
    res_type_search_select = Element(xpath='//input[@placeholder="请选择"]', describe='资源类型搜索下拉框')
    res_delete_button = Element(xpath='//i[@title="删除"]', describe='资源删除按钮')
    res_edit_button = Element(xpath='//i[@title="编辑"]', describe='资源编辑按钮')
    res_total_span = Element(class_name='el-pagination__total', describe='总条数标签')

    @staticmethod
    def click_res_type(res_type, ops='search'):
        """
        根据资源类型点击资源，用于新建资源和搜索资源时选择资源类型
        @param res_type:
        @param ops:
        @return:
        """
        ele_index = 0 if ops == 'search' else -1
        res_type_map = {
            'mysql': (1, 1), 'oracle': (1, 2), 'sqlserver': (1, 3), 'db2': (1, 4), 'postgresql': (1, 5),
            'hana': (1, 6), 'tidb': (1, 7), 'dm': (1, 8), 'hive': (2, 1), 'hbase': (2, 2), 'hdfs': (2, 3),
            'ftp': (3, 1), 's3': (3, 2)
        }
        location = res_type_map[res_type]
        str1 = '//div[@class="el-cascader-panel"]/div[1]/div[1]/ul/li['+str(location[0])+']'
        str2 = '//div[@class="el-cascader-panel"]/div[2]/div[1]/ul/li['+str(location[1])+']'
        Element(xpath=str1, index=ele_index).click()
        Element(xpath=str2, index=ele_index).click()