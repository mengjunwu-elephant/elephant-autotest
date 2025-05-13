import unittest
from time import sleep

from ddt import ddt, data

from common1.test_data_handler import get_test_data_from_excel
from common1 import logger
from settings import TestMercury

# 从Excel中提取数据
cases = get_test_data_from_excel(TestMercury.TEST_DATA_FILE, "over_limit_return_zero")


@ddt
class TestOverLimitReturnZero(unittest.TestCase):
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

    @data(*cases)
    def test_over_limit_return_zero(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameter:{}'.format(case['parameter']))
        # 先移动机械臂
        self.device.ml.send_angles(self.device.coords_init_angles,self.device.speed)
        self.device.ml.send_angles(self.device.coords_init_angles, self.device.speed)
        # 左臂请求发送
        l_response = self.device.ml.over_limit_return_zero()
        l_get_res = self.device.ml.get_angles()
        # 右臂请求发送
        r_response = self.device.mr.over_limit_return_zero()
        r_get_res = self.device.mr.get_angles()
        sleep(2)
        # 判断机械臂是否回到零位
        try:
            self.device.ml.is_in_position([0, 0, 0, 0, 0, 90, 0], l_get_res) and self.device.mr.is_in_position([0, 0, 0, 0, 0, 90, 0],
                                                                                           r_get_res) == 1
        except Exception as e:
            self.logger.debug("左臂未回到零位，当前角度值为{}".format(l_get_res))
            self.logger.debug("右臂未回到零位，当前角度值为{}".format(r_get_res))
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
