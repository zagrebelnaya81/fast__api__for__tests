from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
from app.selenium_autotest.utils.check_recaptcha import check_captcha
from app.selenium_autotest.utils.loger import loger
import traceback


class test_form:
    def __init__(self, driver, url, data_set, name_test, submit=""):
        self.driver = driver
        self.name_test = name_test
        self.url = url
        self.data_set = data_set
        self.submit = submit
        self.log = loger(self.driver, url, name_test)

    def run(self, time_delay):
        try:
            self.driver.get(self.url)
            for type_elm, attr_set in self.data_set.items():
                if type_elm == "input":
                    for id, value in attr_set.items():
                        self.driver.find_element(By.ID, id).send_keys(value)
                elif type_elm == "select":
                    for id, value in attr_set.items():
                        Select(self.driver.find_element(By.ID, id)).select_by_index(value)
                else:
                    self.log.add_log('Not have type element in "if" section', "failed")
                    return 0
        except Exception as exception:
            print("".join(traceback.format_stack()))

            self.log.add_log("".join(traceback.format_stack()), "{}".format(exception.__getattribute__("msg")))

        else:
            for type_elm, attr_set in self.data_set.items():
                if type_elm == "input":
                    for id, value in attr_set.items():
                        self.driver.find_element(By.ID, id).send_keys(value)
                elif type_elm == "select":
                    for id, value in attr_set.items():
                        Select(self.driver.find_element(By.ID, id)).select_by_index(value)
                else:
                    self.log.add_log('Not have type element in "if" section', "failed")
                    return 0
            if check_captcha(self.driver, time_delay, self.log):
                time.sleep(2)
                if self.submit:
                    pass
                    # driver.find_element(By.ID, submit).submit()
                time.sleep(time_delay)
                res_on_page = self.driver.find_element(By.XPATH, "//div[@class='message']")
                if res_on_page.text:  # text = Ticket has been submitted
                    self.log.make_screenshot()
                    self.log.add_log(self.driver.find_element(By.XPATH, "//div[@class='message']/p[1]").text, "success")
                    self.log.add_log("Ticket submitted", "success")
                    return 1
                else:
                    self.log.make_screenshot()
                    self.log.add_log("Ticket dont submitted", "failed")
                    return 0
            else:
                return 0
