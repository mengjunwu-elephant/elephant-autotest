import unittest
from time import sleep
from ddt import ddt, data
from pymycobot.error import MercuryDataException

from common1.test_data_handler import get_test_data_from_excel
from common1 import logger
from settings import TestMercury

# 从Excel中提取数据
cases = get_test_data_from_excel(TestMercury.TEST_DATA_FILE, "send_angle")


@ddt
class TestSendAngle(unittest.TestCase):
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
        cls.device.go_zero()
        cls.device.mr.power_off()
        cls.device.ml.power_off()
        cls.logger.info("环境清理完成，接口测试结束")

    def tearDown(self):
        self.device.go_zero()
        self.device.mr.send_angle(11,0,50)
        self.device.mr.send_angle(12, 0, 50)
        self.device.mr.send_angle(13, 0, 50)

    @data(*[case for case in cases if case.get("test_type") == "normal"])
    def test_send_angle_left(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_joint:{}'.format(case['joint']))
        self.logger.debug('test_parameter_1:{}'.format(case['parameter']))
        self.logger.debug('test_parameter_2:{}'.format(case['speed']))
        # 左臂请求发送
        l_response = self.device.ml.send_angles(eval(case["parameter"]),case["speed"])
        try:
            # 请求结果类型断言
            if type(l_response) == int:
                self.logger.debug('左臂请求类型断言成功')
            else:
                self.logger.debug('左臂请求类型断言失败，实际类型为{}'.format(type(l_response)))
            # 请求结果断言
            self.assertEqual(case['l_expect_data'], l_response)
        except AssertionError as e:
            self.logger.exception('请求结果断言失败')
            self.logger.debug('左臂期望数据：{}'.format(case['l_expect_data']))
            self.logger.debug('左臂实际结果：{}'.format(l_response))
            raise e
        else:
            self.logger.info('请求结果断言成功,用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))

    @data(*[case for case in cases if case.get("test_type") in {"normal","right"}])
    def test_send_angle_right(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_joint:{}'.format(case['joint']))
        self.logger.debug('test_parameter_1:{}'.format(case['parameter']))
        self.logger.debug('test_parameter_2:{}'.format(case['speed']))
        # 右臂请求发送
        r_response = self.device.mr.send_angles(eval(case["parameter"]),case["speed"])
        try:
            # 请求结果类型断言
            if type(r_response) == int:
                self.logger.debug('右臂请求类型断言成功')
            else:
                self.logger.debug('右臂请求类型断言失败，实际类型为{}'.format(type(r_response)))
            # 请求结果断言
            self.assertEqual(case['r_expect_data'], r_response)
        except AssertionError as e:
            self.logger.exception('请求结果断言失败')
            self.logger.debug('右臂期望数据：{}'.format(case['r_expect_data']))
            self.logger.debug('右臂实际结果：{}'.format(r_response))
            raise e
        else:
            self.logger.info('请求结果断言成功,用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))

    @data(*[case for case in cases if case.get("test_type") == "exception"])  # 筛选无效等价类用例
    def test_out_limit(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_joint:{}'.format(case['joint']))
        self.logger.debug('test_parameter_1:{}'.format(case['parameter']))
        self.logger.debug('test_parameter_2:{}'.format(case['speed']))
        # 请求发送
        try:
            with self.assertRaises(MercuryDataException,
                                   msg="用例{}未触发value错误，角度，速度为{}{}".format(case['title'], case['parameter'],case['speed'])):
                # 左臂请求发送
                self.device.ml.send_angle(eval(case["parameter"]), case["speed"])
                # 右臂请求发送
                self.device.mr.send_angle(eval(case["parameter"]), case["speed"])
                _assert = input(print("请检查关节报错超限范围是否正确，正确输入1，不正确输入任意数字，点击回车继续"))
                if _assert != "1":
                    raise AssertionError
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