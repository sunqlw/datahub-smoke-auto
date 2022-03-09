import os
import pytest
import time
import allure
from py.xml import html
from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as CH_Options
from selenium.webdriver.firefox.options import Options as FF_Options
from config import RunConfig
from time import sleep
from page import LoginPage

# 项目目录配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "test_report")


# 定义基本测试环境
@pytest.fixture(scope='function')
def base_url():
    return RunConfig.url

# 以下两个方法是用来控制用例表格里面多设置一列以及列值


# 设置用例描述表头
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()


# 设置用例描述表格
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.pop()


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    解决控制台用例名称中文乱码问题
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = description_html(item.function.__doc__)  # 这一步就是在将方法里面的注释转成html上的描述列
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            case_path = report.nodeid.replace("::", "_") + ".png"
            if "[" in case_path:
                # case_name = case_path.split("-")[0] + "].png"  # 这句话干什么用的？为什么要
                case_name = case_path
            else:
                case_name = case_path
            # 判断测试用例执行失败时触发截图，其实截图本质上还是走的selenium的截图方法
            capture_screenshots(case_name)
            # 不忘报告里面添加截图，因为在jenkins和发了邮件也看不到截图
            img_path = "image/" + case_name.split("/")[-1]
            if img_path:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % img_path
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No test_case description"
    desc_ = ""
    for i in range(len(desc)):
        if i == 0:
            pass
        elif desc[i] == '\n':
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i]

    desc_lines = desc_.split(";")
    desc_html = html.html(
        html.head(
            html.meta(name="Content-Type", value="text/html; charset=latin1")),
        html.body(
            [html.p(line) for line in desc_lines]))
    return desc_html


def capture_screenshots(case_name):
    """
    配置用例失败截图路径
    :param case_name: 用例名
    :return:
    """
    global driver
    file_name = case_name.split("/")[-1]
    if RunConfig.NEW_REPORT is None:
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
        RunConfig.NEW_REPORT = os.path.join(REPORT_DIR, now_time)
        image_dir = os.path.join(RunConfig.NEW_REPORT, "image", file_name)
        RunConfig.driver.save_screenshot(image_dir)
    else:
        image_dir = os.path.join(RunConfig.NEW_REPORT, "image", file_name)
        RunConfig.driver.save_screenshot(image_dir)


def pytest_configure(config):
    config.addinivalue_line("markers", 'smoke')
    config.addinivalue_line("markers", '回归')
    config.addinivalue_line("markers", '日志埋点')

# 启动浏览器
@pytest.fixture(scope='session', autouse=True)
def browser():
    """
    全局定义浏览器驱动
    :return:
    """
    global driver

    if RunConfig.driver_type == "chrome":
        # 本地chrome浏览器
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')  # 忽视安全证书的验证问题
        driver = webdriver.Chrome(chrome_options=options)
        driver.maximize_window()

    elif RunConfig.driver_type == "firefox":
        # 本地firefox浏览器
        driver = webdriver.Firefox()
        driver.maximize_window()

    elif RunConfig.driver_type == "chrome-headless":
        # chrome headless模式
        chrome_options = CH_Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=chrome_options)

    elif RunConfig.driver_type == "firefox-headless":
        # firefox headless模式
        firefox_options = FF_Options()
        firefox_options.headless = True
        driver = webdriver.Firefox(firefox_options=firefox_options)

    elif RunConfig.driver_type == "grid":
        # 通过远程节点运行
        driver = Remote(command_executor='http://localhost:4444/wd/hub',
                        desired_capabilities={
                            "browserName": "chrome",
                        })
        driver.set_window_size(1920, 1080)

    else:
        raise NameError("driver驱动类型定义错误！")

    RunConfig.driver = driver
    # 开始登录
    page = LoginPage(driver)
    page.get(RunConfig.url)
    page.user_input = RunConfig.username
    page.password_input = RunConfig.password
    page.login_button.click()
    return driver


# 关闭浏览器
@pytest.fixture(scope="session", autouse=True)
def browser_close():
    # yield # 在fixture标记的固件中使用通过使用yield来表示执行teardown操作，所以此处表示此次会话结束前执行
    yield driver  # 在fixture标记的固件中使用通过使用yield来表示执行teardown操作，所以此处表示此次会话结束前执行
    driver.quit()
    print("所有用例执行完成")

