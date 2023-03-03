# Data_projects

#1. Webscraping project using BeautifulSoup HTML parser

The site 'books.toscrape.com' scraped for book name, price and ratings to provide results on user chocies inputted using a menu. Logging done at debug level. Page and book locators are used to identify the books at page level and to acquire each book detail. The total page count is also scraped from the website to access all the pages from the site using a PAGER locator.

#2. Data modeling Netflix weekly data

Netflix's "Top 10" TV Shows and Films database(based on the weekly data of popular TV shows/films viewed by subscribers in a number of countries) is extracted into 3 pandas dataframes and stored to a postgresDB, 'mydb' located in the host.  

#3. Formatting twitter data and moving the formatted version to s3 bucket with airflow orchestration

A twitter user's profile details from twitter are undergone ETL process using tweepy. The resulting data is moved to an s3 bucket using Airflow hosted on an AWS EC2 instance (t3.medium).
