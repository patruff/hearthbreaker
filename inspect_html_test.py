import os

from selenium import webdriver
import time

# options = webdriver.ChromeOptions()
# options.add_argument("--user-data-dir=C:/Users/patru/AppData/Local/Google/Chrome/User Data/Profile {#}/")
# options.add_argument("--user-data-dir=C:/Users/patru/AppData/Local/Google/Chrome/User Data/Default/")

# browser = webdriver.Chrome("C:/bin/chromedriver.exe", chrome_options=options)
browser = webdriver.Chrome(executable_path='chromedriver.exe') # , chrome_options=options)

browser.get('https://hsreplay.net/account/login/?next=/games/mine/')
browser.find_element_by_xpath('//button[@type="submit"]').click()
#element = browser.find_element_by_class_name('container')
# searchform.send_keys('cefuroxim')
#button = browser.find_element_by_class_name('account-login login-bnet').click()

time.sleep(10)

username = browser.find_element_by_id("accountName")
password = browser.find_element_by_id("password")

mybnetuser = os.environ['BLIZZARD_USERNAME']
mybnetpassword = os.environ['BLIZZARD_PASSWORD']

username.send_keys(mybnetuser)
password.send_keys(mybnetpassword)

browser.find_element_by_id("submit").click()

time.sleep(10)

#browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
#print(browser.execute_script("return navigator.userAgent;"))
#element = browser.find_element_by_id('body')
#print(element)
#html = element.get_attribute('innerHTML')

html = browser.page_source


# html = browser.execute_script("return document.body.innerHTML;")
# print(browser.page_source.encode('utf-8'))
# print(html)
with open("latest_replays_chron.html", "w", encoding='utf-8') as file:
    file.write(str(html))

#with open("latest_replays_chron.html", "w") as file:
#    file.write(html)

browser.close()


# print(html)

