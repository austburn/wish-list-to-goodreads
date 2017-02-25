import re
from selenium import webdriver
from bs4 import BeautifulSoup
import requests


AUTHOR_REGEX = 'by (?P<author>(?:[A-Za-z\.]+\s?[A-Za-z\.]+\s?)+)'

def pull_wish_list(url):
    wish_list = []
    driver = webdriver.Chrome()
    driver.get(url)
    source = driver.page_source
    # hax
    if 'validateCaptcha' in source:
        driver.get(url)
        source = driver.page_source
    driver.close()
    soup = BeautifulSoup(source, 'html.parser')
    table = soup.find('table')
    entries = table.findAll('tr')[1:]
    for entry in entries:
        title = entry.find('h5').text
        author_str = entry.find('span').text.strip()
        author = re.match(AUTHOR_REGEX, author_str).groups()[0].strip()
        wish_list.append({'title': title, 'author': author})

    return wish_list
