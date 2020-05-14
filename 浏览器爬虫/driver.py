import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Driver(object):

    def __init__(self):
        """调用无头浏览器，并登录到企查查，全局变量保证函数只被调用一次"""

        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.maximize_window()
        driver.get("https://www.qichacha.com/firm_3890e66b0c3b99eea9635a40ac4bd7f2.html")
        cookies = [
            {"name": "QCCSESSID", "value": "ojsp6hascb7rt1s00kfkvboke6"},
            {"name": "Hm_lpvt_3456bee468c83cc63fb5147f119f1075", "value": "%s" % int(time.time())},
        ]
        for cookie in cookies:
            driver.delete_cookie(cookie['name'])
            driver.add_cookie({
                'domain': '.qichacha.com',  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': '/',
                'expires': None
            })
        self.driver = driver


my_driver = Driver()
driver = my_driver.driver
