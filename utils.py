import subprocess, threading, time
from appium import webdriver
from appium.options.common import AppiumOptions

appium_processes = {}
appium_processes_lock = threading.Lock()


def open_appium(app_port: int):
    try:
        process = subprocess.Popen(
            f"appium -p {app_port}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        with appium_processes_lock:
            appium_processes[app_port] = process
        time.sleep(3)
        # Check if the process is still running

        # Wait for a few seconds to allow the server to start
    except Exception as e:
        print(f"Error starting Appium server: {e}")


def open_device(device_id: str, device_name: str, app_port: int = 4723):
    open_appium(app_port=app_port)
    desired_caps = {
        "udid": device_id,
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "appActivity": ".Main",
        "deviceName": device_name,
        "noReset": True,
        "skipServerInstallation": False,  # Ensure server installation is not skipped
        "skipDeviceInitialization": False,  # Ensure device initialization is not skipped
    }

    url = f"http://localhost:{app_port}"
    print("url::: ", url)
    print("desired_caps::: ", desired_caps)
    driver = webdriver.Remote(
        command_executor=url,
        options=AppiumOptions().load_capabilities(desired_caps),
    )
    print(f"Connect Device {device_name} Successfully!!!")

    driver.implicitly_wait(time_to_wait=10)
    return driver


def get_adb_device_ids() -> list:
    try:
        result = subprocess.run(
            ["adb", "devices", "-l"], capture_output=True, text=True
        )
        lines = result.stdout.splitlines()
        devicesList = []
        for index, line in enumerate(lines):
            if "device " in line:
                parts = line.split()
                device_id = parts[0]
                model_info = [part for part in parts if part.startswith("model:")]
                device_name = model_info[0].split(":")[1] if model_info else "Unknown"
                device_info = {
                    "deviceId": device_id,
                    "deviceName": device_name,
                    "deviceIndex": index - 1,
                }
                devicesList.append(device_info)

        return devicesList
    except FileNotFoundError:
        print(
            "Error: adb command not found. Please ensure that the Android SDK Platform Tools are installed and in your system's PATH."
        )
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
