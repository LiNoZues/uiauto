[感谢]

Poium项目	https://github.com/SeldomQA/poium

[环境准备]
python > 3.10

[安装依赖包]
mac m1  :arch -arm64 pip install -r requirement.txt
其他： pip install -r requirement.txt

[原则]

1. 一个页面一个Page类（页面元素基本上相同的可以归为一个类）
2. 通用组件可以抽离放在common_compnent里面
3. po二层封装，page（xxx_page.py） bus(xxx_page_bus.py)     【page层 ->bus层】
4. 为了避免用例之间相互影响，每个用例执行完成后需要回到初始页面（具体情况具体对待）
5. 失败监控恢复的装饰器，在有ui操作的地方加上（仅限于setup，teardown）【装饰器代码路径 libs/utils/decorate,具体使用方法可以参考已有用例代码】
6. po封装中一定要加注释!!!! 每个函数，每个Element都需要加描述
7. 单个元素使用Element，元素集合使用Elements

[fail_to_main 函数流程示意图]
![image-20240305213215237](/Users/cz/Library/Application Support/typora-user-images/image-20240305213215237.png)



[allure用例描述]

@allure.epic（系统级别）>@allure.feature（子系统级别）>@allure.story（业务模块）

| 使用方法                  |       参数值       |                           参数说明                           |
| ------------------------- | :----------------: | :----------------------------------------------------------: |
| @allure.epic()            |      epic描述      |         用于定义被测用的项目/系统；往下级别是feature         |
| @allure.feature()         |      模块名称      |       用于定义被测的功能/需求点/模块；往下级别是story        |
| @allure.story()           |      用户故事      |           用于定义被测的用户场景用例；往下是title            |
| @allure.title(用例的标题) |     用例的标题     |                      重命名html报告名称                      |
| @allure.testcase()        | 测试用例的链接地址 |                对应功能测试用例系统里面的case                |
| @allure.issue()           |        缺陷        |                  对应缺陷管理系统里面的链接                  |
| @allure.description()     |      用例描述      |                        测试用例的描述                        |
| @allure.step()            |      操作步骤      |                        测试用例的步骤                        |
| @allure.severity()        |      用例等级      | blocker 阻塞缺陷（功能未实现，无法下一步）<br/>critical 严重缺陷（功能点缺失）<br/>normal 一般缺陷（边界情况，格式错误）<br/>minor 次要缺陷（界面错误与ui需求不符）<br/>trivial 轻微缺陷（必须项无提示，或者提示不规范） |
| @allure.link()            |        链接        |                 定义一个链接，在测试报告展现                 |
| @allure.attachment()      |        附件        |                         报告添加附件                         |



[一些元素命名的约定俗成]

输入框： xxx_edit

按钮： xxx_btn

下拉框：xxx_dropdown

勾选框：xxx_checkbox

[page层元素命名规范及元素定位]

如果是列表元素 需要以list/group结尾


# 获取ios app 包名
ideviceinstaller -l



# Appium 问题记录&修复
Q:  An unknown server-side error occurred while processing the command. Original error: Could not proxy command to remote server. Original error: Error: Socket Hang up

Fix:  

1. 关闭Appium Server
2. 保证设备已连接pc  `adb devices`
3. 执行卸载命令 ` adb uninstall io.appium.uiautomator2.server` 和 ` adb uninstall io.appium.uiautomator2.server.test`
4. 重启appium server
5. 执行

Q: StaleElementReferenceException

Fix:  (这是由于当前页面是动态页面刷新太快导致的报错)

​	在caps配置里面加上 settings[waitForIdleTimeout]: 100    把这个值设置小点（单位是 毫秒 默认 10*1000 ms = 10s）


## Todo

1. 分布式执行
2. ios封装
