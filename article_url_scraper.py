from bs4 import BeautifulSoup   # scraping library
import requests                 # fetching data from web
import re                       # regular expressions library
import datetime                 # date and time parsing
import os                       # file management
import time                     # timers

from selenium import webdriver
from selenium.webdriver.firefox.options import Options  #for headless firefox
from selenium.webdriver.common.keys import Keys

import warnings

# Beautiful soup tends to send warnings for executing https requests
# This line ignores these warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')



def category_crawler(assign_url):
    """Used for fetching category URL-s on a news portal

    Args:
        assign_url ([str]): Web portal index URL.

    Returns:
        [str]: Returns Absolute URL-s that can be used for further crawling.
    """
    
    soup = BeautifulSoup(assign_url, 'lxml')
    
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
    """Scrolls a page to bottom to activate JS event (Automatic scroll).
    Contains a delay between scrolls for preventing bottlenecks.

    Args:
        scroll_counter ([int]): Number of automatic scrolls to be used.
    """
    
    for i in range(scroll_counter):
    
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        print("Loaded " + str(i+1) + " out of " + str(scroll_counter) + " automated scrolls")



def article_crawler(assign_url):
    """Used for fetching article URL-s in a news portal category.

    Args:
        assign_url ([string]): URL value which is forwarded to requests.
    """
 
    # Creates a list to put article URL-s in
    article_list = []

    # Number of articles found counter set to 0
    counter = 0


    print('\n' + 'Loading website: ' + assign_url + '\n')
    
    driver.get(assign_url) 


    # Go to assigned url through Selenium
    if  (assign_url == 'https://www.dalmacijadanas.hr/rubrika/dalmacija/'):
        #scroll_category(900)   #for reaching 1.1.2020
        scroll_category(20)
    elif(assign_url == 'https://www.dalmacijadanas.hr/rubrika/vijesti/'):
        #scroll_category(900)   #for reaching 1.1.2020
        scroll_category(20)      
    elif(assign_url == 'https://www.dalmacijadanas.hr/rubrika/sport/'):
        #scroll_category(400)   #for reaching 1.1.2020
        scroll_category(20)
    elif(assign_url == 'https://www.dalmacijadanas.hr/rubrika/relax/'):
        #scroll_category(350)   #for reaching 1.1.2020
        scroll_category(10)
    elif(assign_url == 'https://www.dalmacijadanas.hr/rubrika/specijali/'):
        #scroll_category(100)   #for reaching 1.1.2020 
        scroll_category(10)
    elif(assign_url == 'https://www.dalmacijadanas.hr/rubrika/kolumne/'):
        #scroll_category(30)    #for reaching 1.1.2020
        scroll_category(5)
    else:
        print('Error: Category not found')

    
    print('\nProcessing category: ' + assign_url + '\n')

    # html contains whole page html for further URL parsing
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Finds all elements containing class, used  for finding all article URLS
    art_urls = soup.find_all(class_ = 'entry-title td-module-title')     

# In a list of HTML containing articles, isolate 
# href urls under a tags
    for art_url in art_urls:
    
        link = art_url.find('a')['href']

    
    # add article URL to to article list
    article_list.append(link)         

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
            counter = counter + 1   
            continue
        

    print('Fetching from a category finished.')
    print('================================================')
    print('Articles Fetched: ' + str(counter))
    print('from category: ' + assign_url)
    print('Fetching next category URL-s...')
    print('================================================')

    article_log = open('output/portal_log.txt', 'a')
    article_log.write('================================================\n')
    article_log.write('Articles Fetched: ' + str(counter) + '\n')
    article_log.write('from category: ' + assign_url + '\n')
    article_log.write('================================================\n')
    article_log.close()



def article_scraper(assign_url):
    """Used for collecting metadata from news articles, collects 
    metadata from articles published between hardcoded date values.

    Args:
        assign_url ([str]): Article URL to be scraped.

    Returns:
        [bool]: Returns a False boolean value for loop breaking if
        last article is found.
    """

    # Declaration of start and finish article scrap date
    
    start_date = datetime.date(2020, 11, 30)
    finish_date = datetime.date(2020, 11, 25)

    last_article = False

    # Output file declaration, used for article URL-s
    portal_urls = open('output/portal_urls.txt', 'a')

    soup = BeautifulSoup(assign_url.text, 'html.parser')

    # Loops through metadata and finds article publishing date
    for tags in soup.find_all('meta', property='article:published_time'):
        
        date_raw = tags.get('content')
        # Date formating - from string to date_time structure
        date_time_obj = datetime.datetime.strptime(date_raw, '%Y-%m-%dT%H:%M:%S%z')
        # Assign article date to a variable
        article_date = date_time_obj.date()
        print('Processing date: ' + str(article_date))         #testing

        # If date is in a wanted interval of dates, write it to a .txt file
        if (finish_date <= article_date <= start_date): 
            
            print("date ok")        #testing
            scraped_url = soup.find('meta', property='og:url').get('content')
            portal_urls.write(scraped_url + '\n')
            print(scraped_url)      

        # If current date is bigger than a start date condition, skip URL
        elif(article_date > finish_date):

            print('Date before wanted date: ' + str(start_date))
            continue
        else:
           
            print('Last date detected!')   #testing
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
if os.path.exists('output/portal_urls.txt'):
    os.remove('output/portal_urls.txt')
if os.path.exists('output/portal_log.txt'):
    os.remove('output/portal_log.txt')

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