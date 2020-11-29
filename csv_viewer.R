library('readr')
# Used for viewing generated .csv file

setwd('C:\\Users\\usisavac\\Python\\UZ_Scraping')
#Radi
csv_file <- read_csv(file = 'portal_articles.csv')
# Encoding ne hvata
csv_file <- read.csv(file= 'portal_articles.csv',sep = ',', header=T, encoding='utf-8')


View(csv_file)
glimpse(csv_file)
