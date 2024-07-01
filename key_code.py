import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy


def keycodeHome(driver: WebDriver):
    return driver.press_keycode(3)


def keycodeMoveBack(driver: WebDriver):
    return driver.press_keycode(4)


def keycodeSwitch(driver: WebDriver):
    return driver.press_keycode(187)


# Clear all application on the phone
def keycodeClearApp(driver: WebDriver):
    print("Clear phone applications")
    keycodeSwitch(driver=driver)
    time.sleep(2)
    try:
        btnClear = driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.TextView[@resource-id="com.android.systemui:id/button"]',
        )
        if btnClear:
            btnClear.click()
    except NoSuchElementException:
        keycodeMoveBack(driver=driver)
