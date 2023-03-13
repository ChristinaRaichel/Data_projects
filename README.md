# Data_projects

#1. Webscraping project using BeautifulSoup HTML parser

The site 'books.toscrape.com' is scraped for book name, price and ratings to provide results on user chocies inputted using a menu. Logging done at debug level. Page and book locators are used to identify the books at page level and to acquire each book detail. The total page count is also scraped from the website to access all the pages from the site using a PAGER locator.

#2. Data modeling Netflix weekly data

Netflix's "Top 10" TV Shows and Films database(based on the weekly data of popular TV shows/films viewed by subscribers in a number of countries) is extracted into 3 pandas dataframes and stored to a postgresDB, 'mydb' located in the host.  

#3. Formatting twitter data and moving the formatted version to s3 bucket with airflow orchestration

A twitter user's profile details from twitter are undergone ETL process using tweepy. The resulting data is moved to an s3 bucket using Airflow hosted on an AWS EC2 instance (t3.medium).

#4. Data engineering project on AWS cloud

The youtube dataset is  imported to the s3 buckets on AWS. The data stored in s3 buckets are moved through the Glue crawlers to create tables on athena. A lambda function for file format conversions (json to parq) and a legacy glue etl spark script (glue job for converting csv to parq) are carried out. The cleaned (parq) files are moved to the same s3 cleaned-bucket using glue crawler. A lambda trigger is added on to the lambda function to get it triggered everytime a json event happens. Moreover, a reporting layer is created from the cleaned-bucket using glue studio for quickly generating routine query data. Data visualisations are created on AWS Quicksight from the reporting layer data stored in s3 buckets.
