from locators.book_locator import BookLocator
import re
import logging

logger = logging.getLogger('scraping.book_parser')

class BookParser:

    RATINGS = {
        'One' : 1,
        'Two' : 2,
        'Three' : 3,
        'Four' : 4,
        'Five' : 5
    }

    def __init__(self, parent):
        self.parent = parent
        logger.debug(f'New book parser created from `{parent}`')
    def __repr__(self):
       return f'<"{self.name}", price: {self.price}, (rating: {self.rating} stars)>'
    @property
    def name(self):
        logger.debug('Finding book name...')
        bname = self.parent.select_one(BookLocator.NAME)
        logger.debug('Found book name `{bname}`')
        return bname.attrs['title']
    @property
    def rating(self):
        logger.debug('Finding book rating...')
        brating = self.parent.select_one(BookLocator.RATING)
        brating = brating.attrs['class']
        brating = [p for p in brating if p != "star-rating"]
        logger.debug(f'Found book rating `{brating}`')
        return self.RATINGS.get(brating[0])

    @property
    def price(self):
        logger.debug('Finding book price...')
        bprice = self.parent.select_one(BookLocator.PRICE)
        pattern = "£([0-9]+\.[0-9]+)"
        bprice = re.search(pattern, bprice.string).group(1)
        logger.debug('Found book price `{bprice}`')
        return bprice

