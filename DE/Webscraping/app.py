import requests
from pages.page import BooksPage

import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level= logging.DEBUG,
                    filename='log.txt'
                    )
logger = logging.getLogger('scraping')
logger.info('Loading books list .. ')

page_content = requests.get("https://books.toscrape.com").content
page = BooksPage(page_content)
book = page.books ##list of books with details
print(page.page_count)

for page_count in range(1,page.page_count):
    page_name = f'https://books.toscrape.com/catalogue/page-{page_count}.html' ##
    page_content = requests.get(page_name).content
    page = BooksPage(page_content)
    logger.debug('Creating Bookspage from page content')
    book.extend(page.books)#list



#for b in book:
    #print(b)
