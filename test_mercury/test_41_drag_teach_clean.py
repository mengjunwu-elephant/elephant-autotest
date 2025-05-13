import unittest
from ddt import ddt, data

from common1.test_data_handler import get_test_data_from_excel
from common1 import logger
from settings import TestMercury

# 从Excel中提取数据
cases = get_test_data_from_excel(TestMercury.TEST_DATA_FILE, "drag_teach_clean")


@ddt
class TestDragTeachClean(unittest.TestCase):
    # 实例化日志模块
    logger = logger

    # 初始化测试环境
    @classmethod
    def setUpClass(cls):
        try:
            cls.device = TestMercury()  # 实例化机械臂
            cls.device.ml.power_on()  # 左臂上电
            cls.device.mr.power_on()  # 右臂上电
            cls.logger.info("机械臂初始化完成，接口测试开始")
        except ValueError as e:
            cls.logger.exception("机械臂上电失败")
            raise e

    # 清理测试环境
    @classmethod
    def tearDownClass(cls):
        cls.device.mr.power_off()  # 右臂需先下电
        cls.device.ml.power_off()  # 左臂下电
        cls.logger.info("环境清理完成，接口测试结束")

    @data(*cases)
    def test_drag_teach_clean(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_parameters:{}'.format(case['parameters']))
        # 左臂请求发送
        l_response = self.device.ml.clear_error_information()
        if l_response is None:
            raise self.logger.error("左臂发送请求失败，请检查是否上电成功")
        else:
            self.logger.debug("左臂发送请求成功")
        # 右臂请求发送
        r_response = self.device.mr.clear_error_information()
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
