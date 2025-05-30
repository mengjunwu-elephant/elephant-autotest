import unittest

from BeautifulReport import BeautifulReport

import settings
from settings import CASES_DIR

if __name__ == '__main__':
    product_name = input("请输入数字选择需要测试的产品：1:mercury,2：pro_gripper,3:my_hand,4:mercury_pro_gripper")
    ts = unittest.TestLoader().discover(CASES_DIR[product_name])
    br = BeautifulReport(ts)
    br.report(**settings.REPORT_CONFIG)

