import unittest
from BeautifulReport import BeautifulReport
import settings
from settings import CASES_DIR

if __name__ == '__main__':
    product_name = input("请输入数字选择需要测试的产品:\n"
                     "1: mercury\n"
                     "2: mercury_pro_gripper\n"
                     "3: mercury_my_hand\n"
                     "4: pro_gripper\n"
                     "5: my_hand\n"
                     "6: mycobot280\n"
                     )
    ts = unittest.TestLoader().discover(CASES_DIR[product_name])
    br = BeautifulReport(ts)
    br.report(**settings.REPORT_CONFIG)

