import unittest
from ddt import ddt, data
import settings
from common1.test_data_handler import get_test_data_from_excel
from common1 import logger
from settings import TestMercury

# 从Excel中提取数据
cases = get_test_data_from_excel(TestMercury.TEST_DATA_FILE, "get_limit_switch")


@ddt
class TestGetSystemVersion(unittest.TestCase,TestMercury):
    # 实例化日志模块
    logger = logger

    @classmethod
    def setUpClass(cls):
        cls.logger.info("接口测试开始")

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("接口测试结束")

    @data(*cases)
    def test_get_limit_switch(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameters:{}'.format(case['parameters']))
        # 左臂请求发送
        l_response = self.ml.get_limit_switch()
        if l_response is None:
            raise self.logger.error("左臂发送请求失败，请检查是否上电成功")
        else:
            self.logger.debug("左臂发送请求成功")
        # 右臂请求发送
        r_response = self.mr.get_limit_switch()
        if r_response is None:
            raise self.logger.error("右臂发送请求失败，请检查是否上电成功")
        else:
            self.logger.debug("右臂发送请求成功")
        # 请求结果类型断言
        if type(l_response) == list:
            self.logger.debug('左臂请求类型断言成功')
        else:
            self.logger.debug('左臂请求类型断言失败，实际类型为{}'.format(type(l_response)))
        if type(r_response) == list:
            self.logger.debug('右臂请求类型断言成功')
        else:
            self.logger.debug('右臂请求类型断言失败，实际类型为{}'.format(type(r_response)))

        # 请求结果断言
        try:
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



