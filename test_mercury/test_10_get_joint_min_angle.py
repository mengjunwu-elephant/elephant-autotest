import unittest
from time import sleep

from ddt import ddt, data

from common1.test_data_handler import get_test_data_from_excel
from common1 import logger
from settings import TestMercury

# 从Excel中提取数据
cases = get_test_data_from_excel(TestMercury.TEST_DATA_FILE, "get_joint_min_angle")


@ddt
class TestGetJointMinAngle(unittest.TestCase):
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

    def tearDown(self):
        self.device.go_zero()
        sleep(3)

    @data(*[case for case in cases if case.get("test_type") == "normal"])  # 筛选有效等价类用例
    @data(*cases)
    def test_get_joint_min_angle(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_id:{}'.format(case['id']))
        # 左臂请求发送
        l_response = self.device.ml.get_joint_min_angle(case["id"])
        self.device.ml.send_angle(case["id"], case["l_expect_data"], self.speed)  # 使机械臂运动到软件限位，判断是否能够到达
        sleep(3)
        l_get_res = self.device.is_in_position(case["l_expect_data"], self.device.ml.get_angle(case["id"]))
        # 右臂请求发送
        r_response = self.device.mr.get_joint_min_angle(case["id"])
        self.device.mr.send_angle(case["id"], case["r_expect_data"])
        sleep(3)
        r_get_res = self.device.is_in_position(case["l_expect_data"], self.device.mr.get_angle(case["id"]))

        # 机械臂是否到达软件限位判断
        try:
            self.assertEqual(l_get_res, 1)
            self.assertEqual(r_get_res, 1)
        except AssertionError as e:
            self.logger.exception("{}关节未到位软件限位，断言失败".format(case["id"]))
            self.logger.debug("左臂{}关节软件限位值为{}，当前角度值为{}".format(case['id'], case["l_expect_data"],
                                                                               self.device.ml.get_angle(case["id"])))
            self.logger.debug("右臂{}关节软件限位值为{}，当前角度值为{}".format(case['id'], case["r_expect_data"],
                                                                               self.device.mr.get_angle(case["id"])))
            raise e
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
            self.logger.info('请求结果断言成功,用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))

    @data(*[case for case in cases if case.get("test_type") == "exception"])  # 筛选无效等价类用例
    def test_out_limit(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_id:{}'.format(case['id']))
        # 请求发送
        try:
            with self.assertRaises(ValueError, msg="用例{}未触发value错误，id值为{}".format(case['title'], case['id'])):
                self.device.ml.get_joint_min_angle(case["id"])
                self.device.mr.get_joint_min_angle(case["id"])
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
