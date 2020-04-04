"""

Python 3.7.6
Dependencies:
    1. need to install yagmail -> used for sending emails from a Gmail account
    2. need to install re -> used for splitting with multiple arguments
    3. need to install psycopg2 -> PostgreSQL db connector 
    4. need to install itertools - > used for converting list of tuples into a list: https://www.geeksforgeeks.org/python-convert-list-of-tuples-into-list/
    5. need to install BeautifulSoup -> used for accessing and reading page elements
    6. need to install urllib

About the project:
The script is designed connect to a DB from where it gets its list of urls which are going
to be accessed. From the accessed url the script will scrape the product name, product 
availability and product price. 
After scraping the product name, availability and price the script will send an email alert
containing product name, price, availability and url for all products that are available (in stock).
The script also stores in a secondary table from the same db information about price availabilty and price each time it is run.

See db_settings file for details about db tables, columns an the relation between them.


"""
import yagmail
import smtplib
import re #used for multiple splits
import psycopg2 as pg2
import itertools  #library to create a list of elements from a list of tuples
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import date


#accesses the url and reads all the html code from the page
def bsoup(url):
    req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    return soup

#uses the data from bsoup to identify specific html tags that contain pproduct price, name and availbility (stock)
def store(soup):
    try:
    #define item title
        item_title_section = str(soup.find_all(class_='page-title'))
        item_title_pre = re.split('>|<',item_title_section)[2]
        item_title =re.split('\n                            |\n',item_title_pre)[1]
    #define item price
        item_price_section = str(soup.find_all(class_='product-new-price'))
        item_price_main = re.split('>|<',item_price_section)[2].split('                                    ')[1]
        item_price_sec = re.split('<sup>|</sup>', item_price_section)[1]
        store.item_price = float(item_price_main+'.'+item_price_sec)
    #define item availability (stock)
        item_stock_section = str(soup.find_all(class_='product-highlight product-page-pricing'))
        item_stock_reduced = re.split('>|<', item_stock_section)
        if 'Stoc epuizat' in item_stock_reduced: #if clause is used for filtering only available products that will be added to a list("prod"). This list will be used 
            store.item_stock = 'Stoc epuizat'    #by the smail method to send a mail with the product details (name, price, avialbility and url to product)
        else:
            store.item_stock = 'In stoc'
        prod = item_title + ' este acum disponibil la pretul de '+ str(store.item_price) +'lei \n'+url
        return prod
    except:
        pass

#sends a mail from a Gmail account with product details for all available products
def smail(prod):
    try:
        yag = yagmail.SMTP(user='your.email.address@gmail.com',password='yourPassword')
        content = [prod]
        yag.send(to='destination.maill.address@hotmail.com', subject='Store - Produs in stoc', contents=content)
    except:
        pass

#DB connection and data selection 
conn = pg2.connect(database='your_db', user='db_user_name',password='db_password') # db connection
conn.autocommit  = True
db_links = conn.cursor()
query = 'select p_url from prod_detail' #query to select from the DB the urls that will be scraped

db_links.execute(query) #returns a list of tuples that contain the product links

url_list = list(itertools.chain(*db_links.fetchall())) #itertools converts the list of tuples into a list of elements


def pid(url): # pid variable is used to create a link between prod_detail and prod_history table(pid = foreign key)
    pid_query = "select pid from prod_detail where p_url = '{}'".format(url)
    pid_list = conn.cursor()
    pid_list.execute(pid_query)
    pd = list(itertools.chain(*pid_list.fetchall()))
    pid_list.close()
    pid = int(pd[0])
    return pid


def prod_history(pid,price,stock): #writes data to the prod_history table ()
    insert = 'INSERT INTO prod_history(pid, p_price,p_stock,p_date) '+ "VALUES({},{},'{}',CURRENT_TIMESTAMP)".format(pid,price,stock)
    v_insert = conn.cursor()
    v_insert.execute(insert)
    v_insert.close()


for url in url_list:
    soup = bsoup(url)
    prod = store(soup)
    p = pid(url)
    prod_history(p,store.item_price,store.item_stock)
    if 'Stoc epuizat' in store.item_stock:
        pass
    else:
        mail = smail(prod)

db_links.close()
conn.close()
