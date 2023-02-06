from fastapi import APIRouter
from app.selenium_autotest.utils.test_manager import test_manager

router = APIRouter()


@router.get("/get_tests_name/{platform}/{delay}")
async def get_tests_name(platform: str, delay: int = 1):
    testing = test_manager(platform, delay)
    test_names = testing.get_tests_name()
    return test_names


@router.get("/start/{platform}/{delay}")
async def start(platform: str, delay: int = 1):
    testing = test_manager(platform, delay)
    results = testing.start_all_test()
    return results


@router.get("/get_logs/{platform}/{delay}/{name_test}")
async def get_logs(platform: str, name_test: str, delay: int = 1):
    testing = test_manager(platform, delay)
    results = testing.get_log(name_test)
    return results
