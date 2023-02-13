from locators.page_locator import PageLocator
from bs4 import BeautifulSoup
from parsers.parser import BookParser
import re
import logging

logger = logging.getLogger('scraping.page')

class BooksPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')
        logger.debug('Parsing page content with BeautifulSoup HTML parser')
    @property
    def books(self):
        book = self.soup.select(PageLocator.BOOK)
        logger.debug(f'Finding all books in th page using `{PageLocator.BOOK}`')
        return [BookParser(b) for b in book]
    @property
    def page_count(self):
        content =self.soup.select_one(PageLocator.PAGER).string
        logger.info(f'Found number of caalogue pages available: `{content}`')
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        page = int(matcher.group(1))
        logger.debug(f'Extracted number of pages as integer: `{page}`')
        return page
