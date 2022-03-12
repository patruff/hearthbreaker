# import module
from selenium import webdriver
import time
import os.path

# Create the webdriver object. Here the
# chromedriver is present in the driver
# folder of the root directory.

# driver = webdriver.Chrome(r"./driver/chromedriver")
#options = webdriver.ChromeOptions()
#options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Firefox(executable_path=r'C:/Users/patru/PycharmProjects/hearthbreaker/geckodriver.exe')
# driver.get('https://hsreplay.net/replay/9wwmRqhJXPfwuBRNWfGVnf')

# get https://www.geeksforgeeks.org/
# replay_name = "9wwmRqhJXPfwuBRNWfGVnf"

count = 1
with open('replay_strings.txt') as file:
    for replay_name in file:
        stripped_replay = replay_name.rstrip()

        good_replay_name = "https://hsreplay.net/replay/" + replay_name.rstrip()

        final_replay_path = "./hsreplays_xml/" + stripped_replay + ".xml"

        if os.path.exists(final_replay_path):
            print("xml for " + good_replay_name + "found " + str(count))
            count = count + 1
            continue

        driver.get(good_replay_name)

        print("INSIDE REPLAY " + good_replay_name)

        # Maximize the window and let code stall
        # for 10s to properly maximise the window.
        driver.maximize_window()
        time.sleep(20)

        # Obtain button by link text and click.
        # button = driver.find_element_by_link_text("Donwload Replay XML")

        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            # print(elem.get_attribute("href"))
            element_i_want = elem.get_attribute("href")
            if element_i_want.startswith("https://hsreplaynet-replays.s3.amazonaws.com"):
                # print(element_i_want)
                elem.click()

                page_text = driver.page_source

                #page_text = driver.find_element_by_tag_name('HSReplay').text
                # page_text = driver.find_element('body').text
                # print(page_text)

                text_file = open("./hsreplays_xml/" + stripped_replay + ".xml", "w", encoding='utf-8')
                n = text_file.write("This XML file does not appear to have any style information associated with it. The document tree is shown below.\n")
                n = text_file.write(page_text)
                text_file.close()

                break

                # print("got the replay!!")

# button.click()
