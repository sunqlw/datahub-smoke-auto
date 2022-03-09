from poium import Element
from .load_rds_page import LoadRdsPage
from .load_hdfs_page import LoadHdfsPage
from .load_hbase_page import LoadHbasePage


class LoadComponentPage(LoadRdsPage, LoadHdfsPage, LoadHbasePage):
    hive_load_component = Element(xpath='//span[text()="Hive加载"]', describe='Hive加载组件')
    hdfs_load_component = Element(xpath='//span[text()="HDFS加载"]', describe='HDFS加载组件')
    rds_load_component = Element(xpath='//span[text()="RDS加载"]', describe='RDS加载组件')
    tab_name_input = Element(xpath='//div[@class="target-box color-box"]/div/div/input', describe='目标表名输入框')