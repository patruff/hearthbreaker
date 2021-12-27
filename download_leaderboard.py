#import requests

#url = 'https://playhearthstone.com/en-us/community/leaderboards/?region=US&leaderboardId=CLS&seasonId=93&page=2'
#r = requests.get(url)

from selenium import webdriver
import time

browser = webdriver.Chrome()

browser.get('https://playhearthstone.com/en-us/community/leaderboards/?region=US&leaderboardId=CLS&seasonId=93&page=2')

body_html = browser.find_element_by_xpath("/html/body")
just_html = browser.page_source
# source_code = elem.get_attribute("outerHTML")
# print(element)

with open("test_leaderboard_html.html", "w", encoding='utf-8') as outfile:
    outfile.write(just_html.html)

with open("test_leaderboard_text.txt", "w", encoding='utf-8') as outfile:
    outfile.write(body_html.text)