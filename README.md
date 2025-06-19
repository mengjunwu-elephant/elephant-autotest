# 自动化脚本测试须知

## 1.脚本注意事项：

### 1.1 requirements

```
import BeautifulReport
import openpyxl
import ddt
```

### 1.2修改ddt源码

```
# 注释原有代码 # test_data_docstring = _get_test_data_docstring(func, v) 
# 添加自定义逻辑 test_data_docstring = v["title"] #测试报告描述项改为excel表格中的title列
```

### 1.3替换BeautifulReport的CDN版本

当测试报告显示有误时，将报告中引用的Bootstrap、FontAwesome、animate.css、chosen.css等静态资源文件替换为CDN版本。同时，更新jQuery、bootstrap.min.js、echarts.min.js和chosen.jquery.js等脚本文件。

```
第一部分
    <link href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.css" rel="stylesheet">
    <link href="https://cdn.bootcdn.net/ajax/libs/font-awesome/5.0.0-beta3/css/fontawesome.css" rel="stylesheet">
    <link href="https://cdn.bootcdn.net/ajax/libs/animate.css/4.1.1/animate.min.css" rel="stylesheet">
    <link href="https://cdn.bootcdn.net/ajax/libs/chosen/1.8.8.rc6/chosen.css" rel="stylesheet">
 
 
第二部分
<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script src="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.6.1/js/bootstrap.min.js"></script>
<script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.2.2/echarts.min.js"></script>
<script src="https://cdn.bootcdn.net/ajax/libs/chosen/1.8.8.rc6/chosen.jquery.js"></script>
```

### 1.4 自动化脚本函数说明

#### 1.4.1 get函数校验：此函数用于校验get接口返回值是否正确

```
    def test_get_max_acc(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameter:{}'.format(case['parameter']))

        # 左臂请求发送
        l_response = self.device.ml.get_max_acc()

        # 右臂请求发送
        r_response = self.device.mr.get_max_acc()
        try:
            # 请求结果类型断言
            if type(l_response) == int:
                self.logger.debug('左臂请求类型断言成功')
            else:
                self.logger.debug('左臂请求类型断言失败，实际类型为{}'.format(type(l_response)))
            if type(r_response) == int:
                self.logger.debug('右臂请求类型断言成功')
            else:
                self.logger.debug('右臂请求类型断言失败，实际类型为{}'.format(type(r_response)))
            # 请求结果断言
            self.assertEqual(case['r_expect_data'], r_response)
            self.assertEqual(case['l_expect_data'], l_response)
        except AssertionError as e:
            self.logger.exception('请求结果断言失败')
            self.logger.debug('左臂期望数据：{}'.format(case['l_expect_data']))
            self.logger.debug('右臂期望数据：{}'.format(case['r_expect_data']))
            self.logger.debug('左臂实际结果：{}'.format(l_response))
            self.logger.debug('右臂实际结果：{}'.format(r_response))
            raise e
        else:
            self.logger.info('请求结果断言成功，用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))
```

#### 1.4.2 set函数校验：此函数用于校验超限值报错是否正常

```
    def test_out_limit(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameter:{}'.format(case['parameter']))
        # 请求发送
        try:
            with self.assertRaises(MercuryDataException,
                                   msg="用例{}未触发value错误，参数为{}".format(case['title'], case['parameter'],case['mode'])):
                self.device.ml.set_max_acc(case['parameter'],case['mode'])
                self.device.mr.set_max_acc(case['parameter'],case['mode'])
        except AssertionError:
            self.logger.error("断言失败：用例{}未触发异常".format(case['title']))
            raise  # 重新抛出异常，让测试框架捕获
        except Exception as e:
            self.logger.exception("未预期的异常发生：{}".format(str(e)))
            raise
        else:
            self.logger.info('请求结果断言成功，用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))
```

#### 1.4.3 掉电是否保存校验：此函数用于校验参数是否掉电保存

```
    def test_save_or_not(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameter:{}'.format(case['parameter']))
        self.logger.debug('test_mode:{}'.format(case['mode']))
        # 左臂请求发送
        l_response = self.device.ml.set_max_acc(case['parameter'],case['mode'])
        # 右臂请求发送
        r_response = self.device.mr.set_max_acc(case['parameter'],case['mode'])

        # 设置机械臂重启
        self.device.reset()

        # 读取默认值
        l_get_res = self.device.ml.get_max_acc(case['mode'])
        r_get_res = self.device.mr.get_max_acc(case['mode'])
        try:
            # 请求结果类型断言
            if type(l_response) == int:
                self.logger.debug('左臂请求类型断言成功')
            else:
                self.logger.debug('左臂请求类型断言失败，实际类型为{}'.format(type(l_get_res)))
            if type(r_response) == int:
                self.logger.debug('右臂请求类型断言成功')
            else:
                self.logger.debug('右臂请求类型断言失败，实际类型为{}'.format(type(r_get_res)))
            # 请求结果断言
            self.assertEqual(case['r_expect_data'], r_get_res)
            self.assertEqual(case['l_expect_data'], l_get_res)
        except AssertionError as e:
            self.logger.exception('请求结果断言失败')
            self.logger.debug('左臂期望数据：{}'.format(case['l_expect_data']))
            self.logger.debug('右臂期望数据：{}'.format(case['r_expect_data']))
            self.logger.debug('左臂实际结果：{}'.format(l_get_res))
            self.logger.debug('右臂实际结果：{}'.format(r_get_res))
            raise e
        else:
            self.logger.info('请求结果断言成功，用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))
```



## 2.三指灵巧手注意事项：

### 2.1 设置零位时，需将夹爪竖立放置

<img src=".\images\img.png" alt="img" style="zoom:25%;" />

### 2.2 目前用例覆盖率95%+，涉及运动指令，需观察夹爪角度以及速度是否运行正常，运动时是否抖动

### 2.3 IO需使用IO开关单独测试

## 3.力控夹爪注意事项：

### 3.1 目前用例覆盖率95%+，涉及运动指令，需观察夹爪角度以及速度是否运行正常，运动时是否抖动

### 3.2 获取当前队列的数据量接口（GetQueueCount）接口需配合串口助手手动测试

