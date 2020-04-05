Scraping Script - Python 3.7.6
===============================


Dependencies:
-------------

    1. yagmail -> used for sending emails from a Gmail account
    2. re -> used for splitting with multiple arguments
    3. psycopg2
    4. itertools - > used for converting list of tuples into a list: https://www.geeksforgeeks.org/python-convert-list-of-tuples-into-list/
    5. BeautifulSoup
    6. urllib



About the project:
-------------------

The script is designed connect to a DB from where it gets its list of urls which are going to be accessed. From the accessed url the script will scrape the product name, product availability and product price. 

After scraping the product name, availability and price the script will send an email alert
containing product name, price, availability and url for all products that are available (in stock).

The script also stores in a second table from the same db information about product availabilty and price each time it is run.



SQL to create the DB tables in PostgreSQL
------------------------------------------






BI
--
https://mode.com/

https://www.holistics.io/

https://vizydrop.com/

