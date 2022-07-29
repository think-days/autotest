# pytestDemo

本项目实现接口自动化技术选型：**Python+Requests+Pytest+YAML+Allure。Python+Request发送和处理HTTP接口请求，Pytest作为测试执行器，YAML管理测试数据，Allure生成测试报告

## 项目说明

本项目在实现过程中，把整个项目拆分成请求方法封装、HTTP封装，关键字封装，测试用例等模块。

先利用Python吧HTTP接口封装成Python接口，然后把这些接口组装成关键字，再把这些关键字装成测试用例；测试数据则通过YAML文件进行统一管理，接着通过Pytest测试执行器来运行这些脚本，通过命令执行Allure输出测试报告。

未来将会集成到Jenkins中实现自动运行

## 项目结构

- config ===>> 配置文件
- log ===>> 日志文件
- testcase ===>> 测试用例
- testdata ===>> 测试数据
- testreport ===>> 测试报告
- utils ===>> 测试工具
- pytest.ini ===>> pytst配置文件
- requirement.txt ===>> 依赖包

## 测试报告

在执行命令：```pytest```运行用例后，会得到一个测试报告的原始文件，但这个时候还不鞥打开HTML的报告，还需要在项目的根目录下执行命令启动```Allure```服务：

```
# 需要提前配置Allure环境，才可以执行命令行
allur serve./report
```