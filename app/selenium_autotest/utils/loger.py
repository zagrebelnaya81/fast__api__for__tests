import json
from datetime import datetime


class loger:
    def __init__(self, driver, Test_page, test_name):
        self.Test_page = Test_page
        self.driver = driver
        self.test_name = test_name
        self.log_test = {}

    def save_log(self):
        try:
            f = open("log_test.txt")
        except Exception:
            with open("log_test.txt", "w", encoding="utf8") as f:
                json.dump(self.log_test, f, ensure_ascii=False)
        else:
            with open("log_test.txt", "rb+") as f:
                f.seek(-1, 2)
                s = json.dumps(self.log_test, ensure_ascii=False)
                b = bytes(f",{s[1:]}", "utf-8")
                f.write(b)

    def make_screenshot(self):
        self.driver.save_screenshot(f"scr_shot/new_{self.test_name}.png")

    def add_log(self, log_string, event):
        full_log_string = f'{datetime.now().strftime("%Y_%m_%d-%I:%M:%S")} - {self.test_name}::>{log_string}'
        self.log_test = {
            "test_name": self.test_name,
            "event": event,
            "log_string": full_log_string,
            "url": self.Test_page,
            "scr_shot": f"new_{self.test_name}.png",
            "canonic_scr_shot": "",
            "dif_scr_shot": 0,
        }

    def print_log(self):
        with open("log_test.txt") as f:
            s = json.loads(f.read())
            print(s)
