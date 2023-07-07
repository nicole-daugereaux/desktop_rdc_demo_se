####################################################################
# Skeleton for Appium tests on Sauce Labs Real Devices - Unified Platform
# This is currently in BETA and will only work for private devices
####################################################################

###################################################################
# Imports that are good to use
###################################################################
from appium import webdriver
from time import sleep
import os
import urllib3
import multiprocessing
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
    androidTest = True
    iosTest = False
    useApp = False
    appLocation = 'storage:fe971d04-a830-4554-a50c-162ef002935c'
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
    superhero_names_url = urllib3.PoolManager().request('GET', 'https://raw.githubusercontent.com/sindresorhus/superheroes/main/superheroes.json')
    superhero_names = json.loads(superhero_names_url.data.decode('utf-8'))
    random_superhero = random.choice(superhero_names)

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
    region = 'US-West'

    ###################################################################
    # Common parameters (desired capabilities)
    ###################################################################
    projectParameters = {
        # 'tags':['Case', 'Investigation',],
        # The following are not required
        # ''tunnelIdentifier': 'exampletunnel'
        # 'app': 'storage:610f9e00-9415-44a2-94f1-a1f418663cd3',
        # 'app': 'storage:8a8b7702-f4fb-4788-93fa-8a8a3e631c74',
        }

    androidParameters = {
        'browserName': 'Chrome',
        'platformName': 'Android',
        # 'platformVersion': '10',
        # 'deviceName': 'Google.*',
        'sauce:options': {'name': 'Android Smoke Test'},
        # 'name': random_superhero,
        # 'extendedDebugging': True,

        # 'phoneOnly': 'true',
        # Define Android parameters here
        # 'deviceName' : 'Google.*',
        # 'deviceName' : 'Samsung Galaxy S10\+',
        # 'deviceName' : '(Samsung.*)|(Huawei.*)|(Xiaomi.*)|(OnePlus.*)|(Google.*)',
        # 'deviceName' : 'Google Pixel 3 .*',
        # 'orientation' : 'LANDSCAPE',
        # 'platformName' : 'Android',
        # 'browserName' : 'Chrome',
        # 'platformVersion' : '11',
        # 'otherApps': 'storage:5471e3e8-5be6-48f7-8968-47ffc574b2f6',
        # 'appiumVersion': '1.14.0',
        # 'deviceOrientation': 'portrait',
    }

    iosParameters = { # Define iOS Parameters here
        # 'deviceName' : 'iPhone [6-8]',
        # 'deviceName' : 'iPhone 12 Pro Max',
        'platformVersion' : '13',
        'platformName' : 'iOS',
        # 'automationName' : 'XCUITest',
        # 'tabletOnly': 'true',
        # 'extendeDebugging': True,

        # 'phoneOnly': 'true',
        'name': 'appium 1.22.0 test',
        'appiumVersion': '1.22.0',
        # 'autoDismissAlerts': 'true',
        # 'connectHardWareKeyboard' : 'true',
        'browserName' : 'safari',
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
        region = ''

    if region == 'US-West':
        print(Fore.MAGENTA + 'You are using the US-West data center for an RDC test, so a bald eagle is obviously running your tests.' + Style.RESET_ALL)
        driver = webdriver.Remote(
            command_executor='https://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.us-west-1.saucelabs.com:443/wd/hub',
            desired_capabilities=sauceParameters)
    elif region == 'EU':
        print (Fore.CYAN + 'You are using the EU data center for an RDC test, you beautiful tropical fish!' + Style.RESET_ALL)
        driver = webdriver.Remote(
            command_executor='https://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.eu-central-1.saucelabs.com:443/wd/hub',
            desired_capabilities=sauceParameters)
    elif region == 'US-East':
        print (Fore.GREEN + 'You are using the US-East data center for an RDC test, you noble, majestic land mermaid!' + Style.RESET_ALL)
        driver = webdriver.Remote(
            command_executor='https://'+os.environ['SAUCE_USERNAME']+':'+os.environ['SAUCE_ACCESS_KEY']+'@ondemand.us-east-4.saucelabs.com:443/wd/hub',
            desired_capabilities=sauceParameters)

    ###################################################################
    # Test logic goes here
    ###################################################################
    # # # Navigating to a website
    # driver.get_window_size()
    driver.get('https://www.google.com')

    # # #
    # # # # Finding an element
    interact = driver.find_element("xpath",'//input[@name="q"]')
    sleep(3)

    # #
    # # # # Using the selected element
    interact.send_keys('puppies')
    driver.press_keycode(66)
    #interact.click()

    # # # Saving an extra screenshot
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


###################################################################
# This is the command to use multiprocessing to run the desired
# amount of times
###################################################################
if __name__ == '__main__':
    jobs = [] # Array for the jobs
    for i in range(run): # Run the amount of times set above
        jobRun = multiprocessing.Process(target=run_sauce_test) # Define what function to run multiple times.
        jobs.append(jobRun) # Add to the array.
        jobRun.start() # Start the functions.
        # print('this is the run for: '+ str(i))
