import os

from pymycobot import *

from Myhand.MyHand import MyGripper_H100
from elegripper.elegripper import Gripper

# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 产品名称
CASES_DIR = {
    "1": "test_mercury",
    "2": "test_pro_gripper",
    "3": "test_my_hand",
    "4": "test_mercury_pro_gripper",
}

# 日志配置
LOG_CONFIG = {
    'name': 'elephant',
    'filename': os.path.join(BASE_DIR, r'log/log.log'),
    'debug': True,
    'mode': 'a',
    'encoding': 'utf-8'
}

# 测试报告
REPORT_CONFIG = {
    'description': 'elephant-test',
    'filename': 'reports/elephant测试报告.html'
}


# 水星x1七轴配置
class TestMercury:
    # 机械臂运动数据
    speed = 50
    init_angles = [0, 0, 0, 0, 0, 90, 0]
    coords_init_angles = [0, 20, 0, -90, 0, 90, 0]
    # 七轴软件限位
    max_limit = [165,120,165,1,165,255,165]
    min_limit = [-165,-50,-165,-165,-165,-75,-165]
    ex_max_limit = [0,245,160]
    ex_min_limit = [-55,-70,-160]

    # 测试数据配置
    TEST_DATA_FILE = os.path.join(BASE_DIR, r'test_data/test_mercury.xlsx')
    PRO_GRIPPER_TEST_DATA_FILE = os.path.join(BASE_DIR, r'test_data/test_mercury_pro_gripper.xlsx')

    def __init__(self, left_port="/dev/left_arm", right_port="/dev/right_arm"):
        self.ml = Mercury(left_port,save_serial_log=1)
        self.mr = Mercury(right_port,save_serial_log=1)

    def close(self):
        self.ml.close()
        self.mr.close()

    def go_zero(self):
        self.ml.send_angles(self.init_angles, self.speed)
        self.mr.send_angles(self.init_angles, self.speed)

    def init_coords(self):
        self.ml.send_angles(self.coords_init_angles, self.speed)
        self.mr.send_angles(self.coords_init_angles, self.speed)

    def reset(self):
        self.mr.power_off()
        self.ml.power_off()
        self.ml.power_on()
        self.mr.power_on()

    def power_on_only(self):
        self.mr.power_off()
        self.ml.power_off()
        self.ml.power_on_only()
        self.mr.power_on_only()

    def power_off(self):
        self.mr.power_off()
        self.ml.power_off()

    def set_default_torque_comp(self):
        torque_comp = [0,0,0,0,10,30,30]
        for i,c in enumerate(torque_comp):
            self.ml.set_torque_comp(i+1,c)
            self.mr.set_torque_comp(i+1,c)

    def set_default_pos_over_shoot(self):
        self.ml.set_pos_over_shoot(50)
        self.mr.set_pos_over_shoot(50)

    @staticmethod
    def is_in_position(target, current):
        count = 0
        if isinstance(target, (float,int)):
            if abs(current) - 1 <= abs(target) <= abs(current) + 1:
                return 1
            else:
                return -1
        else:
            for i, c in zip(target, current):
                if abs(i) - 3 <= abs(c) <= abs(i) + 3:
                    count += 1
                    if count == len(target):
                        return 1
                else:
                    return -1


# Pro力控夹爪配置
class TestProGripper:
    # 夹爪速度
    speed = 100
    # 测试数据配置
    TEST_DATA_FILE = os.path.join(BASE_DIR, r'test_data/test_pro_gripper.xlsx')

    def __init__(self, port="com3", baudrate=115200):
        self.m = Gripper(port, baudrate=baudrate)

    def go_zero(self):
        self.m.set_gripper_value(0, self.speed)


# MyHand三指灵巧手配置
class TestMyHand:
    # 夹爪速度
    speed = 50

    # 测试数据配置
    TEST_DATA_FILE = os.path.join(BASE_DIR, r'test_data/test_my_hand.xlsx')

    def __init__(self, port="com3", baudrate=115200):
        self.m = MyGripper_H100(port, baudrate=baudrate)

    def go_zero(self):
        self.m.set_gripper_angles([0, 0, 0, 0, 0, 0], self.speed)

    def set_default_p(self):
        for i in range(6):
            self.m.set_gripper_joint_P(i + 1, 100)

    def set_default_d(self):
        for i in range(6):
            self.m.set_gripper_joint_D(i + 1, 120)

    def set_default_i(self):
        for i in range(6):
            self.m.set_gripper_joint_I(i + 1, 0)

    def set_default_cw(self):
        for i in range(6):
            self.m.set_gripper_joint_cw(i + 1, 5)

    def set_default_cww(self):
        for i in range(6):
            self.m.set_gripper_joint_cww(i + 1, 5)

    def set_default_mini_pressure(self):
        for i in range(6):
            self.m.set_gripper_joint_mini_pressure(i + 1, 0)

    def set_default_torque(self):
        for i in range(6):
            self.m.set_gripper_joint_torque(i + 1, 100)

    def set_default_speed(self):
        for i in range(6):
            self.m.set_gripper_joint_speed(i + 1, 100)


# mycobot280配置
class TestMycobot280:
    # 机械臂速度
    speed = 50
    # 测试数据配置
    TEST_DATA_FILE = os.path.join(BASE_DIR, r'test_data/test_mycobot280.xlsx.xlsx')

    def __init__(self, port="com3", baudrate=115200):
        self.mc = MyCobot280(port, baudrate=baudrate)
