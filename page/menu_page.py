import time
import timeit

import pyautogui
import platform
import pyperclip
from poium import Page, Element
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from poium.common import logging


class MenuPage(Page):
    res_type_list = ['mysql', 'oracle', 'sqlserver', 'db2', 'postgresql', 'hana', 'tidb', 'dm', 'ftp', 'sftp', 's3',
                     'hdfs', 'hive', 'hive_ha', 'hbase']
    job_manager_button = Element(xpath='//ul[@class="main-nav"]/li[1]/div', describe='任务管理按钮')
    res_manager_button = Element(xpath='//ul[@class="main-nav"]/li[2]/div', describe='资源管理按钮')
    toast_elem = Element(xpath='/html/body/div[last()]/p', describe='toast标签')
    table_ele = Element(tag='tbody', describe='表格通用对象')
    table_tr1_td1 = Element(xpath='//tbody/tr[1]/td[1]/div', describe='表格第一行第一列')
    box_text_ele = Element(xpath='//div[@class="el-message-box__message"]/p', describe='弹窗内容')
    box_cancel_button = Element(xpath='//div[@class="el-message-box__btns"]/button[1]', describe='弹窗取消按钮')
    box_sure_button = Element(xpath='//div[@class="el-message-box__btns"]/button[2]', describe='弹窗确定按钮')
    box_close_button = Element(xpath='//div[@class="el-message-box__header"]/button[1]', describe='弹窗右上角×按钮')
    no_data_sign = Element(xpath='//div[@class="empty-content"]/p', describe='暂无数据标识')
    search_button = Element(xpath='//span[contains(text(),"搜索")]/..', describe='搜索按钮')
    reset_button = Element(xpath='//span[contains(text(),"重置")]/..', describe='重置按钮')

    # 弹窗操作通用方法
    def box_operate(self, confirm):
        if confirm == 'sure':
            self.box_sure_button.click()
        elif confirm == 'cancel':
            self.box_cancel_button.click()
        else:
            self.box_close_button.click()

    # 比较浮窗内容通用方法
    def compare_toast(self, content):
        self.toast_elem.is_displayed()
        return self.toast_elem.text == content

    @staticmethod
    def find_elem_by_attribute(attribute, value):
        """
        根据属性和值寻找元素并返回元素
        """
        return Element(xpath='//*[@'+attribute+'="'+value+'"]')

    # 定义自己的方法，根据pyautogui采用绝对坐标来拖拽元素
    def drag_and_drop_by_offset_by_pyautogui(self, elem, x, y):
        elem_location = self.switch_elem(elem).location
        browser_height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')
        y_absolute_coord = elem_location['y'] + browser_height
        pyautogui.moveTo(x=elem_location['x'], y=y_absolute_coord, duration=1, tween=pyautogui.linear)
        pyautogui.dragTo(x=x, y=y, duration=1, button='left')  # 鼠标拖拽

    # 定位元素
    def focus(self, elem):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.switch_elem(elem))

    # 刷新页面
    def refresh_page(self):
        self.driver.refresh()

    # 等待元素不可见
    def wait_elem_not_visibility(self, elem, timeout=10):
        WebDriverWait(self.driver, timeout).until_not(ec.visibility_of(self.switch_elem(elem)), '元素未消失')

    def return_table_line(self, table_ele=table_ele, line_no=1):
        """
        返回表格某一行的所有内容
        :param table_ele: 表格对象
        :param line_no: 行号，从1开始
        :return: 表格内容的list对象
        """
        return self.__return_table_content(table_ele, line_no=int(line_no))

    def return_table_col(self, table_ele=table_ele, col_no=1):
        """
        返回表格某一列的所有内容
        :param table_ele: 表格对象
        :param col_no: 列号，从1开始
        :return: 表格内容的list对象
        """
        return self.__return_table_content(table_ele, col_no=int(col_no))

    def __return_table_content(self, table_ele, line_no=None, col_no=None):
        """
        返回表格某一行的所有内容或者某一列的所有内容
        :param line_no: 行号，从1开始，和col_no互斥，二者只能传一个
        :param col_no: 列号，从1开始
        :param table_ele: 表格元素
        :return: 表格内容的list对象
        """
        start = timeit.default_timer()
        self.table_ele.refresh_element()
        ele = self.switch_elem(table_ele)
        tr_elems = ele.find_elements_by_tag_name('tr')
        list_str = []
        # if len(tr_elems) == 0:
        #     return list_str
        if line_no:
            line_ele = tr_elems[line_no-1]
            td_elems = line_ele.find_elements_by_tag_name('td')
            for x in range(len(td_elems)):
                list_str.append(td_elems[x].find_element_by_tag_name('div').text)
        elif col_no:
            for y in range(len(tr_elems)):
                td_elems = tr_elems[y].find_elements_by_tag_name('td')
                list_str.append(td_elems[col_no-1].find_element_by_tag_name('div').text)
        else:
            print("抛出异常，参数传递有误")
        end = timeit.default_timer()
        logging.info('运行时长：%s' % (end-start))
        return list_str

    def connect_elem(self, source_elem, target_elem):
        """
        模拟两个元素进行连线的方法
        :param source_elem: 源元素
        :param target_elem: 目标元素
        :return:
        """
        ActionChains(self.driver).click_and_hold(self.switch_elem(source_elem)).release(
            self.switch_elem(target_elem)).perform()

    @staticmethod
    def upload_file(filepath):
        """
        通过pyautogui键盘输入的方式控制模拟不同系统的上传文件的方式
        :return:
        """
        time.sleep(1)
        platform_str = platform.platform().lower()  # 首先获取到操作系统
        pyperclip.copy(filepath)  # 中文输入法导致不允许直接输入字符串，故采用复制粘贴的形式
        if 'mac' in platform_str:
            pyautogui.hotkey('shift', 'command', 'g')  # 打开mac的搜索框，可以直接输入文件全路径定位到具体文件
            pyautogui.hotkey('command', 'v')
            pyautogui.press('enter')
            time.sleep(1)  # 必须停留一下，从粘贴到连续键入两个回车键有问题
            pyautogui.press('enter')
        elif 'windows' in platform_str:
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            pyautogui.press('enter')
        else:
            print('抛出异常，目前只支持mac和Windows的操作系统')

    @staticmethod
    def switch_elem(elem):
        """
        将poium里面的Element对象转成selenium里面的WebElement对象
        :return:
        """
        # 需要增加一个判断，如果elem是selenium的WebElement对象就不转了
        if isinstance(elem, Element):
            return elem._Element__get_element(elem.k, elem.v)
        else:
            return elem
