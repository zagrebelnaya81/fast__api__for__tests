from selenium.webdriver import DesiredCapabilities

from app.selenium_autotest.utils.test_form import test_form

from selenium import webdriver

data_set = {
    "input": {
        "contactUs_ltk": "klymchuk.96@gmail.com",
        "phone": "+380502542145",
        "name": "Test",
        "surname": "Testorovets",
        "description": "If you receive this email TEST finish successful!!!!!!!!!",
    },
    "select": {"subject": 1},
}


class test_manager:
    def __init__(self, platform, time_delay=1):
        self.time_delay = time_delay
        if platform == "Chrome":
            # language = "en"
            options = webdriver.ChromeOptions()
            options.add_argument("no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=800,600")
            options.add_argument("--disable-dev-shm-usage")
            host = "chrome"
            self.driver = webdriver.Remote(
                command_executor=f"http://{host}:4444/wd/hub",
                desired_capabilities=DesiredCapabilities.CHROME,
                options=options,
            )
            # stealth(self.driver,
            #         languages=[language, "en"],
            #         vendor="Google Inc.",
            #         platform="Win32",
            #         )
            # self.driver = webdriver.Chrome(executable_path="chromedriver")
        elif platform == "Firefox":
            # fp = webdriver.FirefoxProfile()
            # fp.set_preference("privacy.trackingprotection.enabled", False)
            #
            # fp.update_preferences()
            #
            # self.driver = webdriver.Remote(
            #     command_executor='http://firefox:4444/wd/hub',
            #     desired_capabilities={'browserName': 'firefox', 'javascriptEnabled': True},
            #     browser_profile=fp
            # )
            self.driver = webdriver.Firefox(executable_path="geckodriver")

        self.test_contactus = test_form(
            self.driver, "https://www.store.od.atncorp.com/contactus", data_set, "test_contactus", "contact-form-submit"
        )

    def change_platform(self, platform):
        self.driver.close()
        if platform == "Chrome":
            self.driver = webdriver.Chrome(executable_path="chromedriver")
        elif platform == "Firefox":
            self.driver = webdriver.Firefox(executable_path="geckodriver")

    def get_tests_name(self):
        return [log for log in self.__dict__.keys() if log.find("test") != -1]

    def start_all_test(self, time_delay=None):
        if time_delay is None:
            time_delay = self.time_delay
        for test in self.get_tests_name():
            result = {}
            result[test] = self.start_test(test, time_delay)
        return result

    def start_test(self, test_name, time_delay):
        if time_delay is None:
            time_delay = self.time_delay
        if test_name in self.get_tests_name():
            test = getattr(self, test_name)
            result = test.run(time_delay)
        return result

    def get_log(self, test_name):
        return getattr(self, test_name).log.log_test

    def print_log(self):
        names_obj = self.get_tests_name()
        for obj in names_obj:
            real_obj = getattr(self, obj)
            print(real_obj.log.log_test_task)
