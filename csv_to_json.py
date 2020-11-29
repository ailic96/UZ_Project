import csv, json

csv_file_path = 'portal_articles.csv'
json_file_path = 'portal_articles.json'

data = {}
with open(csv_file_path, encoding = 'utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for rows in csv_reader:
        id = rows['ID']
        data[id] = rows

with open(json_file_path, 'w', encoding = 'utf-8') as json_file:
    json_file.write(json.dumps(data, indent=4, ensure_ascii=False))