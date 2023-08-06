from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class driver_main() :

    desired_caps = {}

    def __init__(self, platformVersion, udid, appActivity, appPackage):
        self.desired_caps['platformName'] = 'Android'
        self.desired_caps['platformVersion'] = platformVersion
        self.desired_caps["automationName"] = "uiautomator2"
        self.desired_caps['udid'] = udid
        self.desired_caps['appActivity'] = appActivity
        self.desired_caps['appPackage'] = appPackage
        self.desired_caps['unicodeKeyboard'] = "false"
        self.desired_caps['resetKeyboard'] = "true"
        self.desired_caps['noReset'] = "true"

    def initialization(self, port) -> webdriver:
        self.driver = webdriver.Remote(f'http://localhost:{port}/wd/hub', self.desired_caps)
        self.driver.implicitly_wait(5)
        return self.driver

    def webDriverWait(self, timeout):
        return WebDriverWait(self.driver, timeout)
