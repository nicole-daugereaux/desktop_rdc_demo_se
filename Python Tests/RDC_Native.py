####################################################################
# Skeleton for Appium tests on Sauce Labs Real Devices - Unified Platform
# This is currently in BETA and will only work for private devices
####################################################################

###################################################################
# Imports that are good to use
###################################################################
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import multiprocessing
from time import sleep
import os
import urllib3
import json
import random
import sys
from colorama import Fore, Back, Style

###################################################################
# This makes the functions below execute 'run' amount of times
###################################################################
run = 10

###################################################################
# Declare as a function in order to do multiple runs
###################################################################
def run_sauce_test():
    androidTest = False
    iosTest = True
    useApp = True
    appLocation = 'storage:186331eb-fffd-4f25-900a-7cbb8f9b6b7f'
    # appLocation = 'storage:filename=NetworkSpeed 2.zip'

    ###################################################################
    # Selenium with Python doesn't like using HTTPS correctly
    # and displays a warning that it uses Unverified HTTPS request
    # The following disables that warning to clear the clutter
    # But I should find a way to do the proper requests
    ###################################################################
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    ###################################################################
    # Pull a random Pokemon name to use as the test name
    ###################################################################
    # pokemon_names_url = urllib3.PoolManager().request('GET', 'https://raw.githubusercontent.com/sindresorhus/pokemon/master/data/en.json')
    # pokemon_names = json.loads(pokemon_names_url.data.decode('utf-8'))
    # random_pokemon = random.choice(pokemon_names)

    ###################################################################
    # Choose if you want Android of iOS capabilities
    # Uncomment one of those lines
    ###################################################################
    # androidTest = True
    # iosTest = True

    ###################################################################
    # Select Data Center
    # Set region to 'US' or 'EU'
    # Test will default to 'US' if left blank or set to any other than 'US' or 'EU'
    ###################################################################
    region = 'US'

    ###################################################################
    # Common parameters (capabilities)
    ###################################################################
    projectParameters = {

        }

    androidParameters = {
            'browserName': 'Chrome',
            'platformName': 'Android',
            'appium:platformVersion': '11',
            # 'phoneOnly': 'true',
            'appium:deviceName' : 'Samsung.*Galaxy.*',
            # 'deviceName' : 'Samsung Galaxy S10\+',
            # 'deviceName' : '(Samsung.*)|(Huawei.*)|(Xiaomi.*)|(OnePlus.*)|(Google.*)',
            # 'deviceName' : 'Google Pixel 3 .*',
            'appium:orientation' : 'PORTRAIT',
            # 'platformName' : 'Android',
            # 'browserName' : 'Chrome',
            # 'platformVersion' : '11',
            # 'otherApps': 'storage:5471e3e8-5be6-48f7-8968-47ffc574b2f6',
            # 'appiumVersion': '1.14.0',
            # 'deviceOrientation': 'portrait',
            'sauce:options':{
                'name': 'Regex W3C Test',
                'appiumVersion': '1.21.0',

                # 'tags':['Case', 'Investigation',],
                # ''tunnelIdentifier': 'exampletunnel'
                }
    }

    iosParameters = { # Define iOS Parameters here
        'deviceName' : 'iPhone.*',
        # 'deviceName' : 'iPhone 12 Pro Max',
        # 'platformVersion' : '16',
        'platformName' : 'iOS',
        # 'automationName' : 'XCUITest',
        # 'tabletOnly': 'true',
        # 'phoneOnly': 'true',
        'name': 'automated native app test',
        'sauce:options':{
            'name': 'Automated Native App Example'
        },
        # 'appiumVersion': '1.22.0',
        # 'autoDismissAlerts': 'true',
        # 'connectHardWareKeyboard' : 'true',
        # 'browserName' : 'safari',
        # 'newCommandTimeout' : '0',
        # 'nativeWebTap': 'true',
    }

    ###################################################################
    # Merge parameters into a single capability dictionary

    ###################################################################
    sauceParameters = {}
    if androidTest != True and iosTest != True:
        print('You need to specify a platform to test on!')
        sys.exit()
    elif androidTest == True and iosTest == True:
        print('Don\'t be greedy! Only choose one platform!')
        sys.exit()
    elif androidTest:
        sauceParameters.update(androidParameters)
        if useApp:
            sauceParameters['app'] = appLocation # Use app if it's specified
        else:
            sauceParameters['browserName'] = 'Chrome' # Otherwise use Chrome
            #Note! Replace 'Chrome' with 'Browser' for older versions of Android to use the stock browser
    elif iosTest:
        sauceParameters.update(iosParameters)
        if useApp:
            sauceParameters['app'] = appLocation
        else:
            sauceParameters['browserName'] = 'safari'



    # This concatenates the tags key above to add the build parameter
    sauceParameters.update({'build': 'Investigation'})

    ###################################################################
    # Connect to Sauce Labs
    ###################################################################
    try:
        region
    except NameError:
        region = 'US'

    if region != 'EU':
        print(Fore.MAGENTA + 'You are using the US data center for an RDC test, so a bald eagle is obviously running your tests.' + Style.RESET_ALL)
        driver = webdriver.Remote(
            command_executor='https://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.us-west-1.saucelabs.com:443/wd/hub',
            desired_capabilities=sauceParameters)
    elif region == 'EU':
        print (Fore.CYAN + 'You are using the EU data center for an RDC test, you beautiful tropical fish!' + Style.RESET_ALL)
        driver = webdriver.Remote(
            command_executor='https://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.eu-central-1.saucelabs.com:443/wd/hub',
             desired_capabilities=sauceParameters)

    ###################################################################
    # Test logic goes here
    ###################################################################
    backpack = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Sauce Labs Backpack")
    backpack.click()
    sleep(2)
    addToCart = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Add To Cart button")
    addToCart.click()
    sleep(2)
    cart = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "tab bar option cart")
    cart.click()
    # # # Navigating to a website
    # driver.get_window_size()
    # driver.get('https://www.google.com')
    # # # #
    # # # # # Finding an element
    # interact = driver.find_element_by_name('q')
    # # # sleep(3)
    # #
    # # #
    # # # # # Using the selected element
    # interact.send_keys('puppies')
    # interact.submit()
    # # # interact.click()
    #
    # # # # Saving an extra screenshot
    # driver.save_screenshot('screenshot.png')
    # #
    # # # Using Action chains
    # # # ActionChains(driver).move_to_element(interact).perform()
    # #
    # # # Sauce Labs specific executors
    # # # driver.execute_script('sauce: break')
    # # # driver.execute_script('sauce:context=Notes here')
    #
    #
    # # Setting the job status to passed
    driver.execute_script('sauce:job-result=passed')
    #
    # # Ending the test session
    driver.quit()
if __name__ == '__main__':
    jobs = [] # Array for the jobs
    for i in range(run): # Run the amount of times set above
        jobRun = multiprocessing.Process(target=run_sauce_test) # Define what function to run multiple times.
        jobs.append(jobRun) # Add to the array.
        jobRun.start() # Start the functions.
        # print('this is the run for: '+ str(i))
