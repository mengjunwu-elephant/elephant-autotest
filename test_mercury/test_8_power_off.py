import unittest

from ddt import ddt, data

from common1 import logger
from common1.test_data_handler import get_test_data_from_excel
from settings import TestMercury

# 从Excel中提取数据
cases = get_test_data_from_excel(TestMercury.TEST_DATA_FILE, "power_off")


@ddt
class TestPowerOff(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        水星系列初始化先左臂上电，后右臂上电
        """
        cls.device = TestMercury()
        cls.device.ml.power_on()
        cls.device.mr.power_on()
        logger.info("初始化完成，接口测试开始")

    @classmethod
    def tearDownClass(cls):
        """
        下电顺序为先右臂下电，后左臂下电
        :return:
        """
        cls.device.mr.power_off()
        cls.device.ml.power_off()
        cls.device.close()
        logger.info("环境清理完成，接口测试结束")

    def tearDown(self):
        self.device.reset()

    @data(*[case for case in cases if case.get("test_type") == "normal"])
    def test_power_off(self, case):
        logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        logger.debug('test_api:{}'.format(case['api']))
        logger.debug('test_parameter:{}'.format(case['parameter']))
        input(print("请确认末端显示是否关闭，按回车键继续测试"))
        # 右臂请求发送
        r_response = self.device.mr.power_off()
        # 左臂请求发送
        l_response = self.device.ml.power_off()
        try:
            # 请求结果类型断言
            if type(l_response) == int:
                logger.debug('左臂请求类型断言成功')
            else:
                logger.debug('左臂请求类型断言失败，实际类型为{}'.format(type(l_response)))
            if type(r_response) == int:
                logger.debug('右臂请求类型断言成功')
            else:
                logger.debug('右臂请求类型断言失败，实际类型为{}'.format(type(r_response)))
            # 请求结果断言
            self.assertEqual(case['r_expect_data'], r_response)
            self.assertEqual(case['l_expect_data'], l_response)
        except AssertionError as e:
            logger.exception('请求结果断言失败')
            logger.debug('左臂期望数据：{}'.format(case['l_expect_data']))
            logger.debug('右臂期望数据：{}'.format(case['r_expect_data']))
            logger.debug('左臂实际结果：{}'.format(l_response))
            logger.debug('右臂实际结果：{}'.format(r_response))
            self.fail("用例【{}】断言失败".format(case['title']))
        else:
            logger.info('请求结果断言成功,用例【{}】测试成功'.format(case['title']))
        finally:
            logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))


    @data(*[case for case in cases if case.get("test_type") == "exception"])
    def test_emergency(self, case):
        logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        logger.debug('test_api:{}'.format(case['api']))
        logger.debug('test_parameter:{}'.format(case['parameter']))
        # 左臂请求发送
        input(print("请拍下急停，按回车键继续测试"))
        l_response = self.device.ml.power_off()

        # 右臂请求发送
        r_response = self.device.mr.power_off()
        input(print("请松开急停，按回车键继续测试"))

        # 请求结果断言
        try:
            self.assertEqual(case['r_expect_data'], r_response)
            self.assertEqual(case['l_expect_data'], l_response)
        except AssertionError as e:
            logger.exception('请求结果断言失败')
            logger.debug('左臂期望数据：{}'.format(case['l_expect_data']))
            logger.debug('右臂期望数据：{}'.format(case['r_expect_data']))
            logger.debug('左臂实际结果：{}'.format(l_response))
            logger.debug('右臂实际结果：{}'.format(r_response))
            self.fail("用例【{}】断言失败".format(case['title']))
        else:
            logger.info('请求结果断言成功,用例【{}】测试成功'.format(case['title']))
        finally:
            logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))