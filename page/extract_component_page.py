from poium import Element
from .extract_rds_page import ExtractRdsPage
from .extract_file_system_page import ExtractFileSystemPage


class ExtractComponentPage(ExtractRdsPage, ExtractFileSystemPage):
    rds_extract_component = Element(xpath='//span[text()="RDS抽取"]', describe='RDS抽取组件')
    hdfs_extract_component = Element(xpath='//span[text()="HDFS文件抽取"]', describe='HDFS文件抽取组件')
    ftp_extract_component = Element(xpath='//span[text()="FTP文件抽取"]', describe='FTP文件抽取组件')
    local_extract_component = Element(xpath='//span[text()="本地文件抽取"]', describe='本地文件抽取组件')
    s3_extract_component = Element(xpath='//span[text()="AWS S3"]', describe='AWS S3抽取组件')
