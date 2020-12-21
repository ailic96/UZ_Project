import os               # For deleting old files 
import csv              # .CSV manipulation
import pandas as pd     # Advanced data manipulation


'''
Deletes files if they exist on a given path.
Input: file path
Output: Warning! Destructive action!
'''
def delete_if_exists(path):
    if os.path.exists(path):
        os.remove(path)



def file_to_list(input_file):
    """Creates a list from input file by reading .txt file by row.

    Args:
        input_file ([file]): .txt file with '\n' delimiter.

    Returns:
        [list]: A list of elements from .txt.
    """
    list = []
    file = open(input_file, 'r', encoding='utf-8')
    
    for row in file:
        row = row.rstrip()      # Remove \n at the end of row
        list.append(row)
    
    return list



def covid_identifier():
    """Identifies COVID-19 related articles by searching through
    a dictionary of common expressions used in this kind of articles.

    Input:
        CSV File

    Output:
        The same csv file with added binary value column (0,1).

    """

    covid_dict = file_to_list('input/covid_dictionary.txt')
    csv_input = 'output/portal_articles.csv'
    csv_output = 'output/portal_articles_covid.csv' 

    article_counter = 0
    covid_counter = 0
    #print(covid_dict)

    with open(csv_input, 'r', encoding = 'utf-8') as csv_read, \
         open(csv_output, 'a', encoding = 'utf-8') as csv_write:

        csv_reader = csv.reader(csv_read, delimiter = ',')
        csv_writer = csv.writer(csv_write,
            delimiter=',', 
            quotechar='"', 
            quoting = csv.QUOTE_MINIMAL, 
            lineterminator='\n')  
        
        #Add header for new columns
        headers = ['ID', 'Title', 'Subtitle', 'URL', 
        'Section','Article_text', 'Published_time', 'Modified_time',
        'Author', 'Comments', 'Reaction_love',
        'Reaction_laugh', 'Reaction_hug', 'Reaction_ponder',
        'Reaction_sad', 'Reaction_mad', 'Reaction_mind_blown', 'COVID']
        
        # Skip old header, add new a new one
        next(csv_reader, None)
        csv_writer.writerow(headers)

        print('Modifying portal_articles.csv...')
        print('Calculating the number of COVID articles...')

        for row in csv_reader:

            # Rows turned to lower_case
            row[1] = row[1].lower()
            row[2] = row[2].lower()
            row[5] = row[5].lower()

            # Identifies covid articles, based on a list of words
            # in covid_dictionary.txt
            if (any(map(row[1].__contains__, covid_dict)) 
                or any(map(row[2].__contains__, covid_dict))
                     or any(map(row[5].__contains__, covid_dict))):

                #print('found COVID-19 article at id:', row[0])     # Testing
                covid_counter += 1
                row.append(1)
                csv_writer.writerow(row)
            else:
                row.append(0)
                csv_writer.writerow(row)

            # print(row)            
            # Sum of articles
            article_counter += 1



    print('Total articles:', article_counter)
    print('COVID-19 articles:', covid_counter)



def articles_by_day():
    """Counts total and COVID related articles by date. 

    Input:
        CSV File from path
    
    Output:
        CSV File from path
    """
    csv_input = 'output/portal_articles_covid.csv'
    csv_output = 'output/tables_categorized/portal_articles_day.csv'
    
    # Uses pandas method 'read_csv' for openin a .csv file
    csv_reader = pd.read_csv(csv_input, sep = ',', encoding = 'utf-8')

    # Define a new dataframe using initial dataframe
    dataframe = pd.DataFrame(csv_reader, columns = ['Published_time', 'COVID'])
    #print(dataframe)

    # Defines a privot table containing unique keys sorted by 'Published_time',
    # contains functions which count articles on each date.
    # Article numbers contain COVID and TOTAL number of articles.
    article_day = dataframe.pivot_table(index = ['Published_time'], 
                                            aggfunc = {'Published_time':len, 
                                                'COVID':lambda x: (x>0).sum()})
    
    # Correcting column names
    article_day.columns = ['COVID_articles', 'Total_articles']
    article_day.index.name = 'Date'

    # Append modified dataframe to .csv file
    article_day.to_csv(csv_output, sep = ',', mode = 'a')
    
    print('\n************************************************************************')
    print('Articles by day')
    print('************************************************************************')

    print(article_day)



def articles_by_category():
    """Counts total and COVID related articles by categories. 

    Input:
        CSV File from path
    
    Output:
        CSV File from path
    """
    
    csv_input = 'output/portal_articles_covid.csv'
    csv_output = 'output/tables_categorized/portal_articles_category.csv'

    # Uses pandas method 'read_csv' for openin a .csv file
    csv_reader = pd.read_csv(csv_input, sep = ',', encoding = 'utf-8')

    # Define a new dataframe using initial dataframe
    dataframe = pd.DataFrame(csv_reader, columns = ['Section', 'COVID'])

    article_category = dataframe.pivot_table(index = ['Section'], 
                                            aggfunc = {'Section':len, 
                                                'COVID':lambda x: (x>0).sum()})
    
    # Correcting column names
    article_category.columns = ['COVID_articles', 'Total_articles']
    article_category.index.name = 'Section'

    # Removing mistakenly added category input, add it to 'Kolumne'
    article_category = article_category.drop('TIHOMIR BRALIĆ')
    article_category.loc[['Kolumne'], ['Total_articles']] += 1

    article_category.to_csv(csv_output, sep = ',', mode = 'a')

    print('\n************************************************************************')
    print('Articles by category')
    print('************************************************************************')
    print(article_category)



def articles_by_month():
    """Counts total and COVID related articles by month. 

    Input:
        CSV File from path
    
    Output:
        CSV File from path
    """
    
    csv_input = 'output/portal_articles_covid.csv'
    csv_output = 'output/tables_categorized/portal_articles_month.csv'

    csv_reader = pd.read_csv(csv_input, sep = ',', encoding = 'utf-8')

    # Define a new dataframe using initial dataframe
    dataframe = pd.DataFrame(csv_reader, columns = ['Published_time', 'COVID'])

    # Adds a 'Month' column for further processing
    dataframe['Month'] = pd.DatetimeIndex(dataframe['Published_time']).month

    article_month = dataframe.pivot_table(index = ['Month'], 
                                                aggfunc = {'Month':len, 
                                                    'COVID':lambda x: (x>0).sum()})    
    # Correcting column names
    article_month.columns = ['COVID_articles', 'Total_articles']

    # Changing month format to croatian
    s = pd.Series(['Siječanj', 'Veljača', 'Ožujak', 'Travanj',
                    'Svibanj', 'Lipanj', 'Srpanj', 'Kolovoz',
                    'Rujan', 'Listopad', 'Studeni'])
    article_month.set_index(s, inplace= True)
    article_month.index.name = 'Month'

    article_month.to_csv(csv_output, sep = ',', mode = 'a', encoding = 'utf-8')
    
    print('\n************************************************************************')
    print('Articles by month')
    print('************************************************************************')
    print(article_month)



#Function calls

delete_if_exists('output/portal_articles_covid.csv')
delete_if_exists('output/tables_categorized/portal_articles_day.csv')
delete_if_exists('output/tables_categorized/portal_articles_category.csv')
delete_if_exists('output/tables_categorized/portal_articles_month.csv')


covid_identifier()
articles_by_day()
articles_by_category()
articles_by_month()