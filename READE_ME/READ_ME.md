# 自动化脚本测试须知

## 1.脚本注意事项：

1.1 requirements

```
import BeautifulReport
import openpyxl
import ddt
```

1.2修改ddt源码

```
# 注释原有代码 # test_data_docstring = _get_test_data_docstring(func, v) 
# 添加自定义逻辑 test_data_docstring = v["title"] #测试报告描述项改为excel表格中的title列
```

1.3替换BeautifulReport的CDN版本

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



## 2.三指灵巧手注意事项：

2.1 设置零位时，需将夹爪竖立放置

<img src="img.png" alt="img.png" style="zoom: 25%;" />

2.2 目前用例覆盖率95%+，涉及运动指令，需观察夹爪角度以及速度是否运行正常，运动时是否抖动

2.3 IO需使用IO开关单独测试

## 3.力控夹爪注意事项：

3.1 目前用例覆盖率95%+，涉及运动指令，需观察夹爪角度以及速度是否运行正常，运动时是否抖动

3.2 获取当前队列的数据量接口（GetQueueCount）接口需配合串口助手手动测试

