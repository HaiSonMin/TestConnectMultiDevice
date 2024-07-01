from utils import get_adb_device_ids, open_device
import threading, sys, schedule, time, signal, qtpy
from key_code import keycodeClearApp
from type_arg import TypeDevice
from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

devices_running = {}


def run_task(
    device_id: str, device_name: str, number_devices: int, app_port: int = 4723
):

    driver = open_device(
        device_id=device_id, device_name=device_name, app_port=app_port
    )
    devices_running[device_id] = True


    time.sleep(5)

    keycodeClearApp(driver=driver)

    time.sleep(5)

    WebDriverWait(driver=driver, timeout=60).until(
        EC.presence_of_element_located(
            (
                AppiumBy.XPATH,
                '//android.widget.TextView[@content-desc="Facebook"]',
            )
        )
    ).click()





def connect_multi_devices():
    listDevices: list[TypeDevice] = get_adb_device_ids()
    startPost = 4723
    for device in listDevices:
        threadTask = threading.Thread(
            target=run_task,
            args=(
                device.get("deviceId"),
                device.get("deviceName"),
                len(listDevices),
                startPost + device.get("deviceIndex") * 2,
            ),
        )
        threadTask.start()


connect_multi_devices()
