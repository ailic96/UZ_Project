library('dplyr')
library('readr')
# Used for viewing generated .csv file

setwd('C:\\Users\\usisavac\\Python\\UZ_Scraping')
#Radi
csv_file <- read_csv(file = 'portal_articles.csv')
#Zeza
#csv_file <- read.csv2(file = 'portal_articles.csv', header = TRUE, encoding = 'utf-8')

csv_file[5:4]
View(csv_file)
glimpse(csv_file)
