import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


path_day = 'output/portal_articles_day.csv'
path_cat = 'output/portal_articles_category.csv'
path_mon = 'output/portal_articles_month.csv'

# Reading csv from path
csv_day = pd.read_csv(path_day, sep = ',', encoding = 'utf-8')
csv_cat = pd.read_csv(path_cat, sep = ',', encoding = 'utf-8')
csv_mon = pd.read_csv(path_mon, sep = ',', encoding = 'utf-8')

# Converting .csv to DataFrame
df_day = pd.DataFrame(csv_day)
df_cat = pd.DataFrame(csv_cat)
df_mon = pd.DataFrame(csv_mon)

# #########################################
# TOTAL NUMBER PLOTS
# #########################################

# Sum of dataframe columns to series
total_sum = pd.Series([df_day['Total_articles'].sum()])
covid_sum = pd.Series([df_day['COVID_articles'].sum()])

# Creating a new value
non_covid = total_sum - covid_sum

# Creating a new DataFrame
covid_sum = covid_sum.append(non_covid)
covid_sum = covid_sum.to_frame()
covid_sum.reset_index(inplace = True)
covid_sum = covid_sum.rename(index = {0 : 'COVID_Articles', 1 : 'Non-COVID_Articles'},
                             columns = {0 :'Number'})     
                            
covid_sum = covid_sum.drop(columns = 'index')

# ######################
# BAR PLOT
# ######################

fig1= plt.subplots()

covid_sum.plot.bar()
plt.ylim(0,20000)
plt.xticks(rotation=360)

plt.title('Total ratio of COVID related and Non-COVID related articles')
plt.savefig('graphing/bar_total.png')

# ######################
# PIE PLOT
# ######################

fig2= plt.subplots()

covid_sum.plot(y = 'Number', 
            kind = 'pie', 
            label = '',
            explode = (0.1, 0),
            autopct ='%1.1f%%',
            figsize = (11,6),
            startangle = 0,
            shadow = True)

plt.title ('Total number of COVID related and Non-COVID related articles')
plt.legend(loc='lower right', bbox_to_anchor=(1.3,0))
plt.savefig('graphing/pie_total.png')


# Edit portal_articles_category.csv by reducing categories

# Grouping categories to smaller and bigger
small_cat = df_cat[df_cat['Total_articles'] <= 50]
big_cat = df_cat[df_cat['Total_articles'] > 50]

# Sum by column
small_cat_total = small_cat.sum()
small_cat_total['Section'] = 'Ostalo'

# Creating a new dataframe with fewer categories
big_cat = big_cat.append(small_cat_total, ignore_index = True)
big_cat = big_cat.set_index('Section')

# Converting index back to a column

big_cat['Section'] = big_cat.index


# #########################################
# DAY PLOTS
# #########################################

# ######################
# BOXX PLOT
# ######################

df_box_day = df_day[['COVID_articles', 'Total_articles']]
df_box_day.plot.box(widths = 0.9)
plt.yticks(np.arange(0, 120, step = 10))
plt.title('Box plot of COVID and Non-COVID related articles')
plt.savefig('graphing/box_day.png')

# ######################
# PLOT, REGULAR
# ######################

df_day.plot(x = 'Date', y = ['Total_articles', 'COVID_articles'])

plt.ylabel('Articles')
plt.xticks(rotation=30, fontsize = 6.5)
plt.title('Daily number of total articles and COVID related articles')
plt.savefig('graphing/plot_day.png')


# #########################################
# CATEGORY CHARTS
# #########################################


# ######################
# PIE CHART WITH ARTICLE CATEGORY RATIOS
# ######################

fig3 = plt.subplots()

big_cat.plot(y = 'Total_articles', 
            kind = 'pie', 
            label = '',
            explode = (0.1,0.35,0.2,0.2,0.1,0.1,0.1,0.1),
            autopct ='%1.1f%%',
            figsize = (11,6),
            startangle = 0)

plt.title ('Total articles ratio by category')
plt.legend(loc='lower right', bbox_to_anchor=(1.3,0))
plt.savefig('graphing/pie_category.png')

# ######################
# PIE CHART WITH COVID ARTICLE CATEGORY RATIOS
# ######################

big_cat.plot(y = 'COVID_articles', 
            kind = 'pie', 
            label = '',
            explode = (0.1,0.25,0.1,0.1,0.1,0.1,0.05,0.1),
            autopct ='%1.1f%%',
            figsize = (11,6),
            startangle = 0)

plt.title ('COVID related articles ratio by category')
plt.legend(loc='lower right', bbox_to_anchor=(1.3,0))
plt.savefig('graphing/pie_category_covid.png')

# ######################
# CATEGORY BAR PLOT, Total_articles, COVID_articles
# ######################


big_cat.plot(x = 'Section', y = ['Total_articles', 'COVID_articles'], kind = 'bar')

plt.ylabel('Articles')
plt.xticks(rotation=30, fontsize = 6.5)
plt.title('Comparement of a total number of articles and \nCOVID related articles by category')
plt.legend(loc='upper center')
plt.savefig('graphing/bar_category.png')


# #########################################
# MONTHLY BAR PLOT, Total_articles, COVID_articles
# #########################################


df_mon.plot(x = 'Month', 
            y = ['Total_articles', 'COVID_articles'], 
            kind = 'bar')

plt.ylabel('Articles')
plt.xticks(rotation=30, fontsize = 6.5)
plt.title('Total number of articles compared to COVID related articles')

plt.savefig('graphing/bar_month.png')