import json
import csvToInfluxdb
import csv
#import pandas as pd


with open('csv.json') as configdata:
    data = json.load(configdata)

print(data['mapping']['fieldSchema'])

listing = data['mapping']['fieldSchema']
for i in data['mapping']['fieldSchema']:
    print(i)
    print(data['mapping']['fieldSchema'][i]['from'])

print(bool(int('0')))

csvToInfluxdb.loadCsv('sample/SIM1_T_20200914.csv', 'csv.json')

#with open('sample/SIM1_T_20200914.csv', 'r', errors="replace") as csvfile:
#    csv_reader = csv.reader(csvfile)
#    
#    for row in csv_reader:
#        print(row)
