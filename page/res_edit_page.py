from poium import Element
from .res_page import ResPage


class ResEditPage(ResPage):
    add_res_button = Element(xpath='//*[@id="sourceManage"]/div/div[2]/button', describe='新建资源按钮')
    res_name_input = Element(xpath='//*[@id="pane-baseInfoTab"]/div[1]/form[1]/div[1]/div/div/input',
                             describe='资源名输入框')
    res_type_select = Element(xpath='//*[@id="pane-baseInfoTab"]/div[1]/form[1]/div[2]/div/div/div[1]/input',
                              describe='资源类型下拉框')
    db_host_input = Element(xpath='//input[@placeholder="请输入服务地址"]', describe='数据库服务器名输入框')
    db_port_input = Element(xpath='//input[@placeholder="请输入端口"]', describe='数据库端口输入框')
    db_server_input = Element(xpath='//input[@placeholder="请输入服务名"]', describe='数据库服务名输入框')
    db_username_input = Element(xpath='//input[@placeholder="请输入用户名"]', describe='数据库用户名输入框')
    db_password_input = Element(xpath='//input[@placeholder="请输入密码"]', describe='数据库密码输入框')
    core_site_upload_button = Element(xpath='//div[@class="upload-btn"]/div/button', describe='core-site文件上传按钮')
    hdfs_site_upload_button = Element(xpath='//div[@class="upload-demo"]/div/button', describe='hdfs-site文件上传按钮')
    hdfs_username_input = Element(xpath='//input[@placeholder="请输入用户名"]', describe='hdfs用户名输入框', index=1)
    hive_hdfs_select = Element(xpath='//input[@placeholder="请绑定HDFS"]', describe='hdfs下拉框')
    hive_bind_hdfs = Element(
        xpath='//form[@class="el-form demo-hiveForm"]/div[1]/div/div/div[2]/div[1]/div[1]/ul/li[1]',
        describe='hive绑定第一个hdfs')
    hive_username_input = Element(xpath='//input[@placeholder="请输入Hive用户"]', describe='hive用户名输入框')
    hive_service_model_select = Element(xpath='//input[@placeholder="请选择服务模式"]', describe='hive服务模式下拉框')
    hive_ha_service = Element(xpath='//span[text()="HA模式"]', describe='hive HA模式')
    hive_common_service = Element(xpath='//span[text()="普通模式"]', describe='hive 普通模式')
    hive_host_input = Element(xpath='//input[@placeholder="请输入服务地址"]', describe='hive服务地址输入框', index=1)
    hive_port_input = Element(xpath='//input[@placeholder="请输入端口"]', describe='hive端口输入框', index=1)
    hive_space_name_input = Element(xpath='//input[@placeholder="请输入命名空间"]', describe='hive命名空间输入框')
    zk_add_button = Element(class_name='el-icon-circle-plus', describe='zk地址第一个添加按钮')
    zk_delete_button = Element(class_name='el-icon-remove', describe='zk地址第一个删除按钮')
    first_zk_input = Element(xpath='//input[@placeholder="请输入Zookeeper地址"]', describe='第一个zk地址输入框')
    second_zk_input = Element(xpath='//input[@placeholder="请输入Zookeeper地址"]', describe='第二个zk地址输入框', index=1)
    third_zk_input = Element(xpath='//input[@placeholder="请输入Zookeeper地址"]', describe='第三个zk地址输入框', index=2)
    hbase_username_input = Element(xpath='//input[@placeholder="请输入用户名"]', describe='hbase用户名输入框', index=2)
    hbase_port_input = Element(xpath='//input[@placeholder="请输入端口"]', describe='hbase端口输入框', index=2)
    znode_input = Element(xpath='//input[@placeholder="请输入Znode目录"]', describe='hbase znode输入框')
    protocol_select = Element(xpath='//input[@placeholder="请输入协议"]', describe='ftp协议选择下拉框')
    protocol_ftp = Element(xpath='/html/body/div[last()]/div/div/ul/li[1]', describe='ftp协议')
    protocol_sftp = Element(xpath='/html/body/div[last()]/div/div/ul/li[2]', describe='sftp协议')
    ftp_host_input = Element(xpath='//input[@placeholder="请输入服务地址"]', describe='ftp服务器名输入框', index=2)
    ftp_port_input = Element(xpath='//input[@placeholder="请输入端口"]', describe='ftp端口输入框', index=3)
    ftp_username_input = Element(xpath='//input[@placeholder="请输入用户名"]', describe='ftp用户名输入框', index=3)
    ftp_password_input = Element(xpath='//input[@placeholder="请输入密码"]', describe='ftp密码输入框', index=1)
    s3_accesskey_input = Element(xpath='//input[@placeholder="请输入AccessKey"]', describe='s3 accesskey输入框')
    s3_secretkey_input = Element(xpath='//input[@placeholder="请输入SecretKey"]', describe='s3 secretkey输入框')
    s3_region_select = Element(xpath='//input[@placeholder="请选择Regions"]', describe='s3 region选择下拉框')
    s3_region_china = Element(xpath='/html/body/div[last()]/div/div/ul/li[last()]', describe='s3 region 中国北部')
    max_connects_input = Element(xpath='//input[@placeholder="最大连接数最多为200"]', describe='最大连接数输入框')
    connect_button = Element(xpath='//*[@id="pane-baseInfoTab"]/div[2]/div[1]/button', describe='测试连接按钮')
    connect_finish_sign = Element(xpath='//*[@id="pane-baseInfoTab"]/div[2]/div[1]/button/following-sibling::i',
                                  describe='测试连接完成标识')
    save_button = Element(xpath='//div[@class="btns"]/button[2]', describe='保存按钮')
    connect_success_sign = Element(class_name='el-icon-circle-check', describe='测试连接通过标志')
    connect_fail_sign = Element(class_name='el-icon-circle-close', describe='测试连接失败标志')
    connect_fail_box = Element(xpath='//div[@aria-label="连接失败"]/div[1]', describe='测试连接失败弹窗')

