from bs4 import BeautifulSoup   # scraping library
import requests                 # fetching data from web
import re                       # regular expressions library
import datetime                 # date and time parsing
import os                       # file management
import time                     # timers

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as Options  #for headless firefox
from selenium.webdriver.common.keys import Keys

import warnings

# Beautiful soup tends to send warnings for executing https requests
# This line ignores these warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

'''
**************
* FUNCTIONS  *
**************
'''
# Used for fetching category URL-s
# Returns Absolute URL-s that can be used for further crawling

def category_crawler(assign_url):
    
    soup = BeautifulSoup(assign_url, 'html.parser')
    
    # Creates a list to put category URL-s in
    category_list = []

    # find all horizontal navigation elements with class 
    # by using regex
    navs = soup.find_all(class_ = re.compile('boja-nav menu-item menu-item-type-taxonomy menu-item-object-category menu-item-has-children td-menu-item td-normal-menu menu-item-(427|478|477|457|463|434)'))
    #print(navs)    #string output of all elements contining class
    
    print('Categories found:\n')
    for nav in navs:
         
         category_url = nav.find('a')['href']
         
         category_list.append(category_url)
         print(category_url)    #Test categories output
         
    print('\n')
    return category_list


def scroll_category(scroll_counter):
    
    for i in range(scroll_counter):
    
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        print("Loaded " + str(i+1) + " out of " + str(scroll_counter) + " automated scrolls")


# Used for fetching URL-s in a news portal category
# takes a list of category URL-s and fowards them requests
# returns article URL in a list

def article_crawler(assign_url):
 
     # Creates a list to put article URL-s in
     article_list = []
    
     # Number of articles found counter set to 0
     counter = 0


     print('\n' + 'Loading website: ' + assign_url + '\n')
     
     driver.get(assign_url) 


     # Go to assigned url through Selenium
     if  (assign_url == 'https://www.dalmacijadanas.hr/rubrika/dalmacija/'):
        scroll_category(1500)
        #scroll_category(5)
     elif(assign_url == 'https://www.dalmacijadanas.hr/rubrika/vijesti/'):
        scroll_category(1500)
        #scroll_category(5)
     elif(assign_url == 'https://www.dalmacijadanas.hr/rubrika/sport/'):
        scroll_category(800)
        #scroll_category(5)
     elif(assign_url == 'https://www.dalmacijadanas.hr/rubrika/relax/'):
        scroll_category(800)
        #scroll_category(5)
     elif(assign_url == 'https://www.dalmacijadanas.hr/rubrika/specijali/'):
        scroll_category(500)
        #scroll_category(5)
     elif(assign_url == 'https://www.dalmacijadanas.hr/rubrika/kolumne/'):
        scroll_category()
     else:
         print('Error: Category not found')

 

     # html contains whole page html for further URL parsing
     html = driver.page_source
     soup = BeautifulSoup(html, 'html.parser')
     
     # Finds all elements containing class, used  for finding all article URLS
     art_urls = soup.find_all(class_ = 'entry-title td-module-title')     

    # In a list of HTML containing articles, isolate 
    # href urls under a tags
     for art_url in art_urls:
        
        link = art_url.find('a')['href']
        counter = counter + 1   
        
        # add article URL to to article list
        article_list.append(link)         
        
     print('================================================')
     print('Articles Fetched: ' + str(counter))
     print('from category: ' + assign_url)
     print('Fetching next category URL-s...')
     print('================================================')

     article_log = open('portal_log.txt', 'a')
     article_log.write('================================================\n')
     article_log.write('Articles Fetched: ' + str(counter) + '\n')
     article_log.write('from category: ' + assign_url + '\n')
     article_log.write('================================================\n')
     article_log.close()

     for article in article_list:
        
        # Sends HTTP request to each article, enters article
        # and finds needed metadata
        article_scraper_response = requests.get(article, 
        headers={'User-Agent': 'Mozilla/5.0'})
        article_scraper_response.encoding = 'utf-8'

        # print(article)
        # checks article_scraper status
        # breaks the loop if last article is found
        if(article_scraper(article_scraper_response)):
            break
        else: 
            continue

     print('Fetching from a category finished.')



# Used for collecting metadata from news articles
# and collects metadata for articles published between
# 1.1.2020 and 30.11.2020 and writes links to .txt
# and metadata to .csv file

def article_scraper(assign_url):

    # Declaration of start and finish article scrap date
    start_date = datetime.date(2020, 1, 1)
    finish_date = datetime.date(2020, 11, 30)

    last_article = False

    # Output file declaration, used for article URL-s
    portal_urls = open('portal_urls.txt', 'a')

    soup = BeautifulSoup(assign_url.text, 'html.parser')

    # Loops through metadata and finds article publishing date
    for tags in soup.find_all('meta', property='article:published_time'):
        
        date_raw = tags.get('content')
        # Date formating - from string to date_time structure
        date_time_obj = datetime.datetime.strptime(date_raw, '%Y-%m-%dT%H:%M:%S%z')
        # Assign article date to a variable
        article_date = date_time_obj.date()
        print(article_date)         #testing

        # checks if currently looped date is between conditions
        if (start_date  <= article_date <= finish_date ): 
            
            print("date ok")        #testing
            scraped_url = soup.find('meta', property='og:url').get('content')
            portal_urls.write(scraped_url + '\n')
            print(scraped_url)            
        else:
           
            print('date skipped')   #testing
            # If last article found, returns True value, terminates the loop
            last_article = True
            return last_article
    
    # Close connection to portal_urls.txt file
    portal_urls.close()



'''
**************
*    MAIN    *
**************
'''

start = time.time()

# Removes portal_urls.txt if exists for having a clean
# portal_urls.txt file on each run
if os.path.exists('portal_urls.txt'):
    os.remove('portal_urls.txt')
if os.path.exists('portal_log.txt'):
    os.remove('portal_log.txt')

# Main news portal URL
url = 'https://dalmacijadanas.hr'
headers = "headers={'User-Agent': 'Mozilla/5.0'}'"

# Firefox driver for Selenium
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
options.headless = True

print('\n' + 'Webdriver initialized...')

driver.get(url)

print('\n' + 'Loading website: ' + url + '\n')
page_source = driver.page_source

categories = category_crawler(page_source)

# Iterate through categories and 
for category in categories:
    # Initialize article_crawler function with category URL
    # as an argument
    articles = article_crawler(category)
         
#Time spent gathering data
end = time.time()
print("Time spent gathering data: " + str(end - start))