import os                           # Deleting files for fresh start 
import glob                         # Dictionary file merging
import pandas as pd                 # Handling dataframes
import csv                          # Handling csv files
from collections import Counter     # Counting word frequency

import matplotlib.pyplot as plt     # Plotting
from wordcloud import WordCloud     # Plotting

import nltk                         # Natural language manipulation
from nltk.tokenize import word_tokenize               
from nltk.corpus import stopwords
#nltk.download('punkt')
#nltk.download('stopwords')


def delete_if_exists(path):
    """Deletes a file from input path if file exists.
    WARNING: Potentialy destructive action
    Args:
        path ([string]): Path variable or string
    """
    if os.path.exists(path):
        os.remove(path)



def dictionary_editor(input_file, output_file):
    """Turns raw stop word file to machine readable version

    Args:
        input_file ([file]): Raw input file
        output_file ([file]): Clean output file
    """
    delete_if_exists(output_file)  

    file_reader = open(input_file, 'r', encoding='utf-8')
    file_writer = open(output_file, 'a', encoding='utf-8')

    print('Processing file: ' + str(input_file) + '...')

    for row in file_reader:
        row = row.replace('(', '')
        row = row.replace(')', '')
        row = row.replace(', ', '\n')
        row = row.lower()

        file_writer.write(row)

    print('Writing to ' + str(output_file) + '...\n')

    file_reader.close()
    file_writer.close()
    


def dictionary_merger():
    """Merges all files which start with 'clean_' to form
    a single stop_words_merged dictionary

    Input:
        input/clean_stopw/clean_*.txt
    
    Output:
        input/stop_words_merged.txt
    """

    path = 'input/stop_words_merged.txt'
    delete_if_exists(path)

    # Returns a list of paths for merging
    file_reader = glob.glob('input/clean_stopw/clean_*.txt')

    print('Found files:\n', file_reader)

    with open('input/stop_words_merged.txt', 'wb') as file_writer:
        for f in file_reader:
            with open(f, 'rb') as infile:
                file_writer.write(infile.read())

    print('\nMerging complete, results saved at:', path)



def isolate_covid_articles():
    """Saves rows to another .csv file if they are covid related 
    by comparing a 'COVID' column value. 
    Used for cleaning rows and for editing the dataframe structure.

    Input:
        output/portal_articles_covid.csv

    Output:
        output/discourse_csv/portal_covid_isolated.csv
    """
    delete_if_exists('output/discourse_csv/portal_covid_isolated.csv')

    input_path = 'output/portal_articles_covid.csv'
    output_path = 'output/discourse_csv/portal_covid_isolated.csv'

    df = pd.read_csv(input_path)

    # Isolating articles with COVID value equal to 1
    df = df[df['COVID'] == 1]

    # Combining article text to one column
    df['Text'] = df['Title'] + ' ' + df['Subtitle'] + ' ' + df['Article_text']

    # Isolating columns needed for further analysis
    df = df[['Published_time', 'Text']]
    df.index.name = 'ID'
    
    df.to_csv(output_path) 

    print('Created new .csv file containing COVID-19 articles at', output_path)



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



def clear_stop_words():
    """Used for clearing stop words from portal_covid_isolated which are
    predefined in stop_words_merged.txt
    Input: 
        input/stop_words_merged.txt
        output/discourse_csv/portal_covid_clean.csv'
    Output:
        output/discourse_csv/portal_covid_clean.csv   
    """

    delete_if_exists('output/discourse_csv/portal_covid_clean.csv')

    stop_words = set(file_to_list('input/stop_words_merged.txt'))
    
    input_path = 'output/discourse_csv/portal_covid_isolated.csv'
    output_path = 'output/discourse_csv/portal_covid_clean.csv'

    ID = 0

    print('Cleaning file ' + str(input_path) + ' of stop words...')

    with open(input_path, 'r', encoding = 'utf-8') as csv_read, \
        open(output_path, 'a', encoding = 'utf-8') as csv_write:

        csv_reader = csv.reader(csv_read, delimiter = ',')
        csv_writer = csv.writer(csv_write,
            delimiter=',', 
            quotechar='"', 
            quoting = csv.QUOTE_MINIMAL, 
            lineterminator='\n')

        headers = ['ID', 'Date', 'Text']

        csv_writer.writerow(headers)

        # Skip old header, add new a new one
        next(csv_reader, None)

        for row in csv_reader:
            row[2] = row[2].lstrip('"')
            word_tokens = word_tokenize(row[2])
            filtered_sentence = []

            for word in word_tokens:
                if word not in stop_words:
                    filtered_sentence.append(word)
            
            ID += 1
                        
            filtered_sentence = (' ').join(filtered_sentence)

            csv_writer.writerow([ID, row[1], filtered_sentence])
            #print(filtered_sentence)

    print('Clean file saved at: ' + output_path)



def word_frequency(input_month):
    """Calculates word frequency from portal_covid_clean.csv by month.

    Args:
        input_month ([int]): Used for filtering values by month

    Output: output/word_frequencies/word_frequency_{month}.csv 
    which contains words and their frequency.
    """
    
    input_path = 'output/discourse_csv/portal_covid_clean.csv'
    output_path = 'output/word_frequencies/word_frequency_' + str(input_month) + '.csv'

    df = pd.read_csv(input_path, sep=',', encoding='utf-8')
    #df = df.set_index(df['Date'])
    
    del df['ID']
    df['Date'] = pd.DatetimeIndex(df['Date']).month
    df = df.rename(columns = {'Date' : 'Month'})

    df = df[df['Month'] == input_month]

    a = df['Text'].str.lower().str.cat(sep=' ')
    words = nltk.tokenize.word_tokenize(a)
    word_dist = nltk.FreqDist(words)
    
    result = pd.DataFrame(word_dist.most_common(25),
                    columns=['Word', 'Frequency'])
    
    result['Month'] = input_month
    result.index.name = 'ID'
    result = result[['Month', 'Word', 'Frequency']]

    print('\n',result)

    result.to_csv(output_path, sep = ',', mode = 'w', encoding = 'utf-8')



def to_word_cloud():
    """Generates a word cloud for every month. Word cloud consists of top 25
    used words on a news portal monthly. 
    
    Input files: Graphs are based on .csv files in output/word_frequencies/
    
    Output files: Graphs are saved in graphing/word_frequencies/
    """

    for i in range(1,12):
        input_path = 'output/word_frequencies/word_frequency_' + str(i) + '.csv'
        output_path =  'graphing/word_frequencies/word_frequency_' + str(i) + '.png'
        
        df = pd.read_csv(input_path, sep = ',', encoding = 'utf-8')

        #text = df.Word[1]
        text = " ".join(word for word in df.Word)

        wordcloud = WordCloud(width = 800, height = 800,

        max_words=25, 
        background_color="white").generate(text)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title('Month: ' + str(i) + ' - most frequent words')

        print('Generating ' + str(i) +  '. wordcloud at ' + output_path)
        wordcloud.to_file(output_path)



def jaccard_index(list1, list2):
    """Calculates jaccard index for input of numbers.

    Args:
        list1 ([list]): List of words from the first dataframe.
        list2 ([list]): List of words from the second dataframe.

    Returns:
        [float]: Returns a calculated value of jaccard index 
        rounded on 4 digits.
    """    
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    
    result = float(intersection) / union
    result = round(result, 4)

    return result



def calculate_jaccard(month_1, month_2):
    """Assigns a month number to path for fetching a .csv file which contains
    a column used for calculating the jaccard index.
    
    Generates jaccard_index.csv file

    Args:
        month_1 ([int]): First month number for comparision
        month_2 ([int]): First month number for comparision
    """    

    input_path_1 = 'output/word_frequencies/word_frequency_' + str(month_1) + '.csv'
    input_path_2 = 'output/word_frequencies/word_frequency_' + str(month_2) + '.csv'

    output_path = 'output/word_frequencies/jaccard_index.csv'

    df_1 = pd.read_csv(input_path_1, sep = ',', encoding = 'utf-8')
    df_2 = pd.read_csv(input_path_2, sep = ',', encoding = 'utf-8')

    df_list_1 = list(df_1['Word'])
    df_list_2 = list(df_2['Word'])

    print('Jaccard index for months: '+ str(month_1) + ', ' + str(month_2))
    jaccard = jaccard_index(df_list_1, df_list_2)
    print(jaccard)

    with open(output_path, 'a', encoding = 'utf-8') as output_file:

        csv_writer = csv.writer(output_file, delimiter=',', lineterminator = '\n')
        months = str(month_1) + '-' + str(month_2)
        row = [months, jaccard]

        if(os.stat(output_path).st_size == 0):
            headers = ['Months', 'Jaccard_index']
            csv_writer.writerow(headers)
            csv_writer.writerow(row)
        else:
            csv_writer.writerow(row)

def visualize_jaccard():
    """Visualizes output/word_frequencies/jaccard_index.csv for each pair
    of months through a bar plot
    """
                
    input_path = 'output/word_frequencies/jaccard_index.csv'

    df = pd.read_csv(input_path, sep = ',')

    df.plot(x = 'Months', y = 'Jaccard_index', kind = 'bar')

    plt.xlabel('Month comparison')
    plt.ylabel('Jaccard_index')
    plt.xticks(rotation=30, fontsize = 6.5)
    plt.title('Jaccard index monthly')
    plt.legend(loc='upper center')
    plt.savefig('output/word_frequencies/jacard_bar_plot.png')

# Create dictionary
dictionary_editor('input/raw_stopw/raw_zamjenice.txt', 'input/clean_stopw/clean_zamjenice.txt')
dictionary_editor('input/raw_stopw/raw_cestice.txt', 'input/clean_stopw/clean_cestice.txt')
dictionary_editor('input/raw_stopw/raw_usklici.txt', 'input/clean_stopw/clean_usklici.txt')
dictionary_editor('input/raw_stopw/raw_prijedlozi.txt', 'input/clean_stopw/clean_prijedlozi.txt')
dictionary_editor('input/raw_stopw/raw_prilozi.txt', 'input/clean_stopw/clean_prilozi.txt')
dictionary_editor('input/raw_stopw/raw_veznici.txt', 'input/clean_stopw/clean_veznici.txt')
dictionary_editor('input/raw_stopw/raw_other.txt', 'input/clean_stopw/clean_other.txt')
dictionary_merger()

# Isolating covid articles from a list of articles
isolate_covid_articles()

# Clear stop words defined in a .txt file
clear_stop_words()

# Generate a .csv file for each month containing 25 most frequent words
for i in range(1,12):
    word_frequency(i)

to_word_cloud()

# Necessery for reproductivity
delete_if_exists('output/word_frequencies/jaccard_index.csv')

# Calculate jaccard for month pairs
calculate_jaccard(1, 2)
calculate_jaccard(2, 3)
calculate_jaccard(3, 4)
calculate_jaccard(4, 5)
calculate_jaccard(5, 6)
calculate_jaccard(6, 7)
calculate_jaccard(7, 8)
calculate_jaccard(8, 9)
calculate_jaccard(9, 10)
calculate_jaccard(10,11)
calculate_jaccard(11,1)

visualize_jaccard()