import unittest
from time import sleep

from ddt import ddt, data
import settings
from common1.test_data_handler import get_test_data_from_excel
from common1 import logger
from settings import TestMyHand

# 从Excel中提取数据
cases = get_test_data_from_excel(TestMyHand.TEST_DATA_FILE, "set_gripper_pose")


@ddt
class TestSetGripperPose(unittest.TestCase):
    # 实例化日志模块
    logger = logger

    # 初始化测试环境
    @classmethod
    def setUpClass(cls):
        cls.device = TestMyHand() #实例化夹爪
        cls.logger.info("初始化完成，接口测试开始")


    # 清理测试环境
    @classmethod
    def tearDownClass(cls):
        cls.device.m.set_gripper_pose(0,5)
        cls.device.m.close()
        cls.logger.info("环境清理完成，接口测试结束")

    def tearDown(self):
        sleep(5)  #等待手指动作完成，不能小于5s


    @data(*[case for case in cases if case.get("test_type") == "normal"]) #筛选有效等价类用例
    def test_set_gripper_pose(self, case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_pose:{}'.format(case['pose']))
        self.logger.debug('test_rank:{}'.format(case['rank']))
        # 请求发送
        set_res = self.device.m.set_gripper_pose(case["pose"],case["rank"],case["is_free"])
        # 请求结果类型断言
        if type(set_res) == int:
            self.logger.debug('请求类型断言成功')
        else:
            self.logger.debug('请求类型断言失败，实际类型为{}'.format(type(set_res)))

        # 请求结果断言
        try:
            self.assertEqual(case['expect_data'], set_res)
        except AssertionError as e:
            self.logger.exception('请求结果断言失败')
            self.logger.debug('期望数据：{}'.format(case['expect_data']))
            self.logger.debug('实际结果：{}'.format(set_res))
            raise e
        else:
            self.logger.info('请求结果断言成功，用例【{}】测试成功'.format(case['title']))
        finally:
            self.logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))


    @data(*[case for case in cases if case.get("test_type") == "exception"]) #筛选无效等价类用例
    def test_out_limit(self,case):
        self.logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        self.logger.debug('test_api:{}'.format(case['api']))
        self.logger.debug('test_pose:{}'.format(case['pose']))
        # 请求发送
        try:
            with self.assertRaises(ValueError, msg="用例{}未触发value错误，pose值为{}".format(case['title'], case['pose'])):
                self.device.m.set_gripper_pose(case["pose"],case["rank"],case["is_free"])
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




