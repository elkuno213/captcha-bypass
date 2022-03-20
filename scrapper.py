import logging
from telnetlib import KERMIT
from time import sleep
# from seleniumwire import webdriver  # Import from seleniumwire
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pathlib import Path


HOME = Path.home()
EXT_METAMASK = f'{HOME}/.chrome-extensions/metamask-chrome-10.11.1_0.crx'
# EXT_METAMASK = 'misc/metamask-chrome-10.11.1.crx'

# CHROME_PROFILE = 'C:\\Users\\Tuan\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 8'
USER_DATA_DIR = 'test_profiles'
PROFILE_DIR = 'profile_3'

METAMASK_HOME = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#'


def main():
    # https://stackoverflow.com/questions/48533462/metamask-automation-with-selenium-webdriver
    # Chrome profile: https://sessionbuddy.com/chrome-profile-location/


    # Create directory to store the profile from that selenium will launch chrome
    profile_dir = Path(USER_DATA_DIR) /  Path(PROFILE_DIR)
    profile_dir.mkdir(parents=True, exist_ok=True)

    # Create a new instance of the Chrome driver
    options = webdriver.ChromeOptions()
    # options.add_extension(EXT_METAMASK) # -> load metamask from .crx, commented if it's installed directly
    options.add_argument(f'profile-directory={PROFILE_DIR}')
    options.add_argument(f'user-data-dir={USER_DATA_DIR}')
    service = Service(ChromeDriverManager().install()) # install correct chromedriver binary and create service
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://play.crabada.com/')

        # driver.switch_to.window(driver.window_handles[0]) # if metamask is loaded, we need to switch to the right tab before go to metamask home
        driver.get(METAMASK_HOME)
        sleep(2) # sleep and wait for all UI elements are loaded

        # find elements
        buttons = driver.find_elements(by=By.XPATH, value="//button[text()='Unlock']")
        print(buttons)
        inputs = driver.find_elements(by=By.XPATH, value="//input")
        print(inputs)
        # inputs[0].send_keys("12345678")
        # buttons[0].click()

        ## first time flow -> create wallet or restored from recovery phrase
        ## Not tested yet
        # driver.find_element(by=By.XPATH, value='//button[text()="Get Started"]').click()
        # driver.find_element(by=By.XPATH, value='//button[text()="Import wallet"]').click()
        # driver.find_element(by=By.XPATH, value='//button[text()="No Thanks"]').click()
        # inputs = driver.find_elements(by=By.XPATH, value='//input')
        # print(inputs)
        # inputs[0].send_keys(SECRET_RECOVERY_PHRASE)
        # inputs[1].send_keys(NEW_PASSWORD)
        # inputs[0].send_keys("NEW_PASSWORD")
        # driver.find_element_by_css_selector('.first-time-flow__terms').click()

        # # Access requests via the `requests` attribute
        # for request in driver.requests:
        #     if request.response:
        #         print(
        #             request.url,
        #             request.response.status_code,
        #             request.response.headers['Content-Type']
        #         )

        sleep(1000)
        driver.quit()
    except KeyboardInterrupt:
        print('quitting...')
        driver.quit()
    except Exception as e:
        logging.exception(e)
        driver.quit()


if __name__ == "__main__":
    main()