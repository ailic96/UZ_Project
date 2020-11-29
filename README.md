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

* ID
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
* Reaction 4 (Ponder)
* Reaction 5 (Sad)
* Reaction 6 (Mad)
* Reaction 7 (Mind blown)

<hr>

## Platform
* Windows 10

 ## Requirements
 * Visual Studio Code
 * Windows WSL 1 (Optional)
 * pip 20.0.2 from /home/user/.local/lib/python3.6/site-packages/pip (python 3.6)
 * Python 3.6.9
 * Libraries
    * selenium
    * BeautifulSoup
    * requests
    * re (Regular expressions)
    * time
    * datetime
    * os
    * csv

<hr>

## Running instructions

__NOTE:__

It is worth mentioning that every time you run each of these scripts, all previously collected data in _.txt_ and _.csv_ will be __overwritten__! This could become a problem because execution time is __very long__.

<hr>

From terminal/cmd:

```
python url_scraping.py
```

This will create a _portal_urls.txt_ file and scrape article URL-s into it.
A file _portal_log.txt_ is also created in order to track how many articles were loaded in each category, since terminal is unable to carry so many informations. At the end of execution, timer will display how much time has passed since script initiation

For further article scraping run:
```
python article_scraper.py
```

This will create a _portal_articles.csv_ which contains scraped article metadata and data. Script will automatically parse needed data and save it in a project folder. At the end of execution, timer will display how much time has passed since script initiation
