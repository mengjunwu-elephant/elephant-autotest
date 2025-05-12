import unittest
from ddt import ddt, data
from common1.test_data_handler import get_test_data_from_excel
from common1 import logger
from settings import TestMercury

# 从Excel中提取数据
cases = get_test_data_from_excel(TestMercury.TEST_DATA_FILE, "get_system_version")


@ddt
class TestGetSystemVersion(unittest.TestCase):
    # 实例化日志模块
    logger = logger

    @classmethod
    def setUpClass(cls):
        """
        水星系列初始化先左臂上电，后右臂上电
        """
        cls.device = TestMercury()
        cls.device.ml.power_on()
        cls.device.mr.power_on()
        cls.logger.info("初始化完成，接口测试开始")

    @classmethod
    def tearDownClass(cls):
        """
        下电顺序为先右臂下电，后左臂下电
        :return:
        """
        cls.device.mr.power_off()
        cls.device.ml.power_off()
        cls.logger.info("环境清理完成，接口测试结束")

    @data(*[case for case in cases if case.get("test_type") == "power_on"])
    def test_get_system_version(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameters:{}'.format(case['parameters']))
        # 左臂请求发送
        l_response = self.device.ml.get_system_version()

        # 右臂请求发送
        r_response = self.device.mr.get_system_version()
        try:
            # 请求结果类型断言
            if type(l_response) == float:
                self.logger.debug('左臂请求类型断言成功')
            else:
                self.logger.debug('左臂请求类型断言失败，实际类型为{}'.format(type(l_response)))
            if type(r_response) == float:
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
            self.logger.info('请求结果断言成功,用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))
        # 恢复测试环境
        self.device.reset()

    @data(*[case for case in cases if case.get("test_type") == "power_on_only"])
    def test_power_on_only(self,case):
        # 机械臂进入仅上电模式
        self.device.power_on_only()

        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameters:{}'.format(case['parameters']))

        # 左臂请求发送
        l_response = self.device.ml.get_system_version()

        # 右臂请求发送
        r_response = self.device.mr.get_system_version()
        try:
            # 请求结果类型断言
            if type(l_response) == float:
                self.logger.debug('左臂请求类型断言成功')
            else:
                self.logger.debug('左臂请求类型断言失败，实际类型为{}'.format(type(l_response)))
            if type(r_response) == float:
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
            self.logger.info('请求结果断言成功,用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))
        # 恢复测试环境
        self.device.reset()

    @data(*[case for case in cases if case.get("test_type") == "power_off"])
    def test_power_off(self, case):
        # 机械臂进入断电模式
        self.device.power_off()

        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameters:{}'.format(case['parameters']))

        # 左臂请求发送
        l_response = self.device.ml.get_system_version()

        # 右臂请求发送
        r_response = self.device.mr.get_system_version()
        try:
            # 请求结果类型断言
            if type(l_response) == float:
                self.logger.debug('左臂请求类型断言成功')
            else:
                self.logger.debug('左臂请求类型断言失败，实际类型为{}'.format(type(l_response)))
            if type(r_response) == float:
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
            self.logger.info('请求结果断言成功,用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))
        # 恢复测试环境
        self.device.reset()