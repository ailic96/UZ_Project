# Data Scraping project
## Author: 
Anton Ilić

## Subject: 
Knowledge Management

## Details
Goal of this project is to research tools used for web scraping and to demonstrate them by gathering data on a news portal. 

<hr>

## Goal: <br>


## __1st phase__
Scrape news article URL-s from dates 1.1.2020 - 30.11.2020 and collect them to _.txt_ file.
Testing phase is done in smaller intervals. 

## __2st phase__
Gather metadata from URL-s obtained in a __.txt__ file and write them in a form of __.csv__ table.

__Proposed metadata:__

* Title
* Subtitle
* URL
* Section
* Article Text
* Published time
* Modified time
* Author
* Number of comments
* Reaction 1 (Love)
* Reaction 2 (Laugh)
* Reaction 3 (Blushy)
* Reaction 4 (Worried)
* Reaction 5 (Sad)
* Reaction 6 (Mad)
* Reaction 7 (Mind blown)

<hr>

## Platform
* Windows 10

 ## Requirements
 * Visual Studio Code
 * Windows WSL 1
 * pip 20.0.2 from /home/user/.local/lib/python3.6/site-packages/pip (python 3.6)
 * Python 3.6.9
 * Libraries
    * selenium
    * BeautifulSoup
    * requests
    * re (Regular expressions)
    * time
    * datetime

<hr>

## Running instructions

From terminal/cmd:

```
python url_scraping.py
```

This will create a _portal_urls.txt_ file and scrape article URL-s into it.
A file _portal_log.txt_ is also created in order to track how many articles were loaded in each category, since terminal is unable to carry so many informations.

For further article scraping run:
```
python article_scraper.py
```

This will create a _portal_articles.csv_ which contains scraped article metadata and data.