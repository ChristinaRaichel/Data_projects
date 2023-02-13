from app import book
import logging

logger = logging.getLogger('scraping.menu')

USER_CHOICE = ''' Enter one of the following
-'b' to look at 5-star books
-'c' for cheapest books
-'n' for next book in the catalogue
-'q' to exit
 Enter your choice '''

def print_best_books():
    logger.info('Finding best books by rating..')
    best_books = sorted(book, key= lambda x: x.rating * -1)[:5] ##
    for b in best_books:
        print(b)
def print_cheap_books():
    logger.info('Finding best books by price..')
    cheap_books = sorted(book, key=lambda x:x.price)[:5]
    for b in cheap_books:
        print(b)
def print_best_cheap_books():
    best_books = sorted(book, key= lambda x: (x.rating * -1,x.price))[:5] ##
    for b in best_books:
        print(b)


'''print("BEST")
print_best_books()
print("CHEAP")
print_cheap_books()
print("BEST CHEAP")
print_best_cheap_books()
'''
books_generator = (x for x in book)

def get_next_book():
    logger.info('Finding next books from generator..')
    print(next(books_generator))


def menu():
    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input == 'b':
            print_best_books()
        if user_input == 'c':
            print_cheap_books()
        if user_input == 'n':
            get_next_book()
        else:
            print("choose a valid input")
            user_input = input(USER_CHOICE)
    logger.debug('Terminating program..')
menu()