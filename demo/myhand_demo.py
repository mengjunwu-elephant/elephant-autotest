from time import sleep

from Myhand.MyHand import MyGripper_H100

m = MyGripper_H100("com3",debug=1,recv_timeout=20)

# print(m.set_gripper_baud(0))
# print(m.get_gripper_Id())
# print(m.set_gripper_joint_calibration(2))

# for i in range(6):
#     m.set_gripper_joint_D(4,150)
#     print(m.get_gripper_joint_D(i + 1))
while 1:

    m.set_gripper_angles([30,60,60,30,30,30],100)
    sleep(2)
    m.set_gripper_angles([0,0,0,0,0,0],1)
    sleep(2)
# m.set_gripper_pose(2,5)
# m.set_gripper_joint_angle(2,0)
# m.set_gripper_joint_speed(1,40)
# m.set_gripper_joint_angle(4,60)
# print(m.get_gripper_angles())
# print(m.get_gripper_joint_speed(4))
# m.set_gripper_enable(0)

# while 1:
#     # m.set_gripper_pose(4,15,1)
#     # sleep(5)
#     # m.set_gripper_pose(0,5)
#     # sleep(5)
#     m.set_gripper_joint_angle(5,100)
#     sleep(1)
#     m.set_gripper_joint_angle(6,100)
#     sleep(1)
#     m.set_gripper_joint_angle(5,0)
#     sleep(1)
#     m.set_gripper_joint_angle(6,0)
#     sleep(1)
# print(m.set_gripper_joint_speed(6,5))
#
# print(m.set_gripper_joint_speed(5,5))
# m.set_gripper_joint_calibration(5)
# m.set_gripper_pose(4,15,1)
# m.set_gripper_joint_mini_pressure(2,24)
# m.set_gripper_joint_mini_pressure(4,24)
# print(m.get_gripper_joint_mini_pressure(4))