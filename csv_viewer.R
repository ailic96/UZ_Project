library('readr')
# Used for viewing generated .csv file

setwd('C:\\Users\\usisavac\\Python\\UZ_Scraping')

csv_file <- read_csv(file = 'portal_articles.csv')

View(csv_file)
glimpse(csv_file)


