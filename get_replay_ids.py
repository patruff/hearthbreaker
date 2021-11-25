# import module
from selenium import webdriver
import time

# Create the webdriver object. Here the
# chromedriver is present in the driver
# folder of the root directory.

# driver = webdriver.Chrome(r"./driver/chromedriver")
driver = webdriver.Chrome(executable_path='C:/Users/patru/PycharmProjects/hearthbreaker/chromedriver.exe')

# get https://www.geeksforgeeks.org/
replay_name = "9wwmRqhJXPfwuBRNWfGVnf"
driver.get("https://hsreplay.net/games/mine/?utm_source=hdt&utm_medium=client&utm_campaign=menu/games/mine")

# Maximize the window and let code stall
# for 10s to properly maximise the window.
driver.maximize_window()
time.sleep(10)

# Obtain button by link text and click.
# button = driver.find_element_by_link_text("Donwload Replay XML")

elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    print(elem.get_attribute("href"))

# button.click()
