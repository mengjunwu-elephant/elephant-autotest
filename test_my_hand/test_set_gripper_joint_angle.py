import unittest
from time import sleep

from ddt import ddt, data
import settings
from common1.test_data_handler import get_test_data_from_excel
from common1 import logger
from settings import TestMyHand

# 从Excel中提取数据
cases = get_test_data_from_excel(TestMyHand.TEST_DATA_FILE, "set_gripper_joint_angle")


@ddt
class TestSetGripperJointAngle(unittest.TestCase):


    # 初始化测试环境
    @classmethod
    def setUpClass(cls):
        cls.device = TestMyHand()  # 实例化夹爪
        logger.info("初始化完成，接口测试开始")

    # 清理测试环境
    @classmethod
    def tearDownClass(cls):
        for i in range(6):
            cls.device.m.set_gripper_joint_angle(i + 1, 0)
            sleep(2)
        cls.device.m.close()
        logger.info("环境清理完成，接口测试结束")

    @data(*[case for case in cases if case.get("test_type") == "normal"])  # 筛选有效等价类用例
    def test_set_gripper_joint_angle(self, case):
        logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        logger.debug('test_api:{}'.format(case['api']))
        logger.debug('test_joint:{}'.format(case['joint']))
        logger.debug("test_angle:{}".format(case["angle"]))
        # 请求发送
        self.set_res = self.device.m.set_gripper_joint_angle(case["joint"], case["angle"])
        sleep(2)
        self.get_res = self.device.m.get_gripper_joint_angle(case["joint"])
        try:
            # 请求结果类型断言
            if type(self.set_res) == int:
                logger.debug('请求类型断言成功')
            else:
                logger.debug('请求类型断言失败，实际类型为{}'.format(type(self.set_res)))
            # 请求结果断言
            self.assertEqual(case['expect_data'], self.set_res)
            self.assertEqual(self.get_res, case["angle"])
        except AssertionError as e:
            logger.exception('请求结果断言失败')
            logger.debug('期望数据：{}'.format(case['angle']))
            logger.debug('实际结果：{}'.format(self.get_res))
            self.fail("用例【{}】断言失败".format(case['title']))
        else:
            logger.info('请求结果断言成功，用例【{}】测试成功'.format(case['title']))
        finally:
            logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))

    @data(*[case for case in cases if case.get("test_type") == "exception"])  # 筛选无效等价类用例
    def test_out_limit(self, case):
        logger.info('》》》》》用例【{}】开始测试《《《《《'.format(case['title']))
        # 调试信息
        logger.debug('test_api:{}'.format(case['api']))
        logger.debug('test_joint:{}'.format(case['joint']))
        logger.debug("test_angle:{}".format(case["angle"]))
        # 请求发送
        try:
            with self.assertRaises(ValueError,
                                   msg="用例{}未触发value错误，joint_angle值为{}".format(case['title'], case['angle'])):
                self.device.m.set_gripper_joint_angle(case["joint"], case["angle"])
        except AssertionError:
            logger.error("断言失败：用例{}未触发异常".format(case['title']))
            raise  # 重新抛出异常，让测试框架捕获
        except Exception as e:
            logger.exception("未预期的异常发生：{}".format(str(e)))
            raise
        else:
            logger.info('请求结果断言成功，用例【{}】测试成功'.format(case['title']))
        finally:
            logger.info('》》》》》用例【{}】测试完成《《《《《'.format(case['title']))
