from utils import get_adb_device_ids, connect_device
import threading, sys, schedule, time, signal, qtpy
from key_code import keycodeClearApp
from type_arg import TypeDevice
from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

devices_running = {}

import subprocess


def open_virtual_device(device_name: str):
    subprocess.call(f"ldconsole launch --name {device_name}", shell=True)

    print("Waiting For Opening And Connecting LDPlayer")


def close_virtual_device(device_name: str):
    subprocess.call(f"ldconsole quit --name {device_name}", shell=True)
    print("Close ld is:", device_name)


class Abc:
    def __init__(self) -> None:
        self.listDeviceRunning = []  # Global [{deviceId:12312312,de}]
        self.deviceHaveRun = []  # DeviceId [emulator-5554,emulator-5556]

    def run_task(
        self,
        device_id: str,
        device_name: str,
        app_port: int = 4723,
    ):

        driver = connect_device(
            device_id=device_id, device_name=device_name, app_port=app_port
        )
        devices_running[device_id] = True

        time.sleep(5)

        keycodeClearApp(driver=driver)

        time.sleep(3)
        ################

        WebDriverWait(driver=driver, timeout=60).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//android.widget.TextView[@content-desc="Facebook"]',
                )
            )
        ).click()

    def run_multi_devices(self):
        startPost = 4723
        for device in self.listDeviceRunning:
            threadTask = threading.Thread(
                target=self.run_task,
                args=(
                    device.get("deviceId"),
                    device.get("deviceName"),
                    startPost + device.get("deviceIndex") * 2,
                ),
            )
            threadTask.start()

    def run(self, devicesNameForRunning: list):
        trackingDevice = 0  # = 5
        numberDeviceError = 0

        while trackingDevice + numberDeviceError < len(devicesNameForRunning):
            print("devicesNameForRunning:::", devicesNameForRunning)
            isOpenedDevice = False
            isOpening = False
            timeOut = 0
            while not isOpenedDevice:
                listDevices: list[TypeDevice] = get_adb_device_ids()
                print(
                    "-----------------------------------------------------------------"
                )
                print("listDevices:::", listDevices)
                print("deviceHaveRun:::", self.deviceHaveRun)
                print("listDeviceRunning:::", self.listDeviceRunning)

                # 1. Clone and open device
                if not isOpening:
                    open_virtual_device(
                        device_name=devicesNameForRunning[
                            trackingDevice + numberDeviceError
                        ]
                    )
                    isOpening = True

                if trackingDevice != len(listDevices):
                    for device in listDevices:
                        if device.get("deviceId") not in self.deviceHaveRun:
                            deviceInfo: TypeDevice = {
                                "deviceId": device.get("deviceId"),
                                "deviceName": devicesNameForRunning[
                                    trackingDevice + numberDeviceError
                                ],
                                "deviceIndex": trackingDevice,
                            }
                            self.listDeviceRunning.append(deviceInfo)
                            self.deviceHaveRun.append(device.get("deviceId"))
                            trackingDevice += 1
                            isOpenedDevice = True
                            break

                time.sleep(5)
                timeOut += 5
                print("timeOut:::", timeOut)
                print("trackingDevice:::", trackingDevice)
                print("numberDeviceError:::", numberDeviceError)
                if timeOut >= 60:
                    close_virtual_device(
                        device_name=devicesNameForRunning[
                            trackingDevice + numberDeviceError
                        ]
                    )
                    numberDeviceError += 1
                    isOpenedDevice = True

            time.sleep(2)

    def run_action(self):
        self.run(listDeviceNames)
        self.run_multi_devices()


listDeviceNames = ["Root-1", "Root-2", "Root-3", "Root-4", "Root-5", "Root-6", "Root-7"]

Abc().run_action()
