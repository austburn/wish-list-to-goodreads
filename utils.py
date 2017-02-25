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


def get_isbns(wish_list, access_key):
    api_base = "http://isbndb.com/api/v2/json/{}/books".format(access_key)
    successful_queries = []
    unsuccessful_queries = []
    for index, book in enumerate(wish_list):
        response = requests.get('{}/?q={}'.format(api_base, book['title'])).json()

        if response['error']:
            print(response['error'])
            continue

        matched_book = get_book_by_author(response.json()['data'], book['author'])
        if matched_book:
            book['isbn'] = matched_book['isbn10']
            successful_queries.append(book)
        else:
            unsuccessful_queries.append(book)

    return successful_queries, unsuccessful_queries



def get_book_by_author(result, author):
    author_split = author.split()
    fmt_author = '{}, {}'.format(author_split[-1], ' '.join(author_split[:-1]))
    for book in result:
        for author in book['author_data']:
            name_search = re.match(fmt_author, author['name'])
            if name_search and name_search.group():
                return book

    return None
