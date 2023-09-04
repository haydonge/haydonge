import csv
import tabulate

filename = 'data.csv'

data = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        data.append(row[:5]) # 只取前6列数据

print(tabulate.tabulate(data, headers='firstrow', tablefmt='grid'))