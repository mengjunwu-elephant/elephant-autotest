import unittest
from ddt import ddt, data
import settings
from common1.test_data_handler import get_test_data_from_excel
from common1 import logger
from settings import TestMercury
from time import sleep

# 从Excel中提取数据
cases = get_test_data_from_excel(TestMercury.TEST_DATA_FILE, "set_limit_switch")


@ddt
class TestSetLimitSwitch(unittest.TestCase,TestMercury):
    # 实例化日志模块
    logger = logger

    @classmethod
    def setUpClass(cls):
        cls.logger.info("接口测试开始")

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("接口测试结束")

    @data(*cases)
    def test_position_close(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameter_1:{}'.format(case['parameter_1']))
        self.logger.debug('test_parameter_2:{}'.format(case['parameter_2']))
        # 左臂请求发送
        l_response = self.ml.set_limit_switch(case['parameter_1'],case['parameter_2'])
        if l_response is None:
            raise self.logger.error("左臂发送请求失败，请检查是否上电成功")
        else:
            self.logger.debug("左臂发送请求成功")
        # 右臂请求发送
        r_response = self.mr.set_limit_switch(case['parameter_1'],case['parameter_2'])
        if r_response is None:
            raise self.logger.error("右臂发送请求失败，请检查是否上电成功")
        else:
            self.logger.debug("右臂发送请求成功")
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
            self.logger.info('请求结果断言成功，用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))


    @data(*cases)
    def test_feedback_close(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameter_1:{}'.format(case['parameter_1']))
        self.logger.debug('test_parameter_2:{}'.format(case['parameter_2']))
        # 左臂请求发送
        l_response = self.ml.set_limit_switch(case['parameter_1'],case['parameter_2'])
        if l_response is None:
            raise self.logger.error("左臂发送请求失败，请检查是否上电成功")
        else:
            self.logger.debug("左臂发送请求成功")
        # 右臂请求发送
        r_response = self.mr.set_limit_switch(case['parameter_1'],case['parameter_2'])
        if r_response is None:
            raise self.logger.error("右臂发送请求失败，请检查是否上电成功")
        else:
            self.logger.debug("右臂发送请求成功")
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
            self.logger.info('请求结果断言成功，用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))

    @data(*cases)
    def test_feedback_logic_close(self,case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 逻辑判断到位反馈是否关闭
        l_res = self.ml.set_limit_switch(2,0)
        r_res = self.mr.set_limit_switch(2,0)
        if l_res and r_res == 1:
            self.logger.debug("到位反馈已关闭，开始控制1关节运动")
            r_angle_res = self.mr.send_angle(1,10,self.speed)
            l_angle_res = self.ml.send_angle(1,10,self.speed)
            if r_angle_res and l_angle_res is None:
                self.logger.debug("到位反馈测试成功")
                self.go_zero()
                sleep(2)
                self.ml.set_limit_switch([2, 1])
                self.mr.set_limit_switch([2, 1])
                self.logger.debug("已恢复默认设置")
                self.logger.info('用例【{}】测试成功'.format(case['title']))
                self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))
            else:
                self.logger.exception("到位反馈测试失败")
        else:
            self.logger.exception("到位反馈关闭失败，请检查接口返回值")


    @data(*cases)
    def test_feedback_logic_open(self,case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 逻辑判断到位反馈是否打开
        l_res = self.ml.set_limit_switch(2,1)
        r_res = self.mr.set_limit_switch(2,1)
        if l_res and r_res == 1:
            self.logger.debug("到位反馈已关闭，开始控制1关节运动")
            r_angle_res = self.mr.send_angle(1,10,self.speed)
            l_angle_res = self.ml.send_angle(1,10,self.speed)
            if r_angle_res and l_angle_res is None:
                self.logger.debug("到位反馈测试成功")
                self.go_zero()
                sleep(2)
                self.ml.set_limit_switch([2, 1])
                self.mr.set_limit_switch([2, 1])
                self.logger.debug("已恢复默认设置")
                self.logger.info('用例【{}】测试成功'.format(case['title']))
                self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))
            else:
                self.logger.exception("到位反馈测试失败")
        else:
            self.logger.exception("到位反馈打开失败，请检查接口返回值")
