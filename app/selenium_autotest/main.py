from utils.test_manager import test_manager

if __name__ == "__main__":
    test_ATN = test_manager("Chrome", time_delay=1)
    test_ATN.start_all_test()
    print(test_ATN.get_log("test_contactus"))
