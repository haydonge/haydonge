import csv
#import tabulate
import math
import PySimpleGUI as sg

file1 = 'data1.csv'
file2 = 'data2.csv'

result = []

with open(file1) as f1, open(file2) as f2:
    rdr1 = csv.reader(f1)
    rdr2 = csv.reader(f2)

    headers1 = next(rdr1)
    headers2 = next(rdr2)

    headers = headers1[:4] + ['X', 'Y', '矢量']
    result.append(headers)

    for row1 in rdr1:
        row2 = next(rdr2)

        new_row = row1[:4] + [row1[4], row2[4]]

        v5 = row1[4]
        v6 = row2[4]

        try:
            v5 = float(v5)
            v6 = float(v6)
        except ValueError:
            print(f"Warning: Could not convert {v5} or {v6} to float")
            v5 = v6 = 0

        new_value = math.sqrt(v5 ** 2 + v6 ** 2)

        new_row.append(new_value)

        result.append(new_row)

# print(tabulate.tabulate(result, headers='firstrow', tablefmt='grid'))

layout = [[sg.Table(result)]]

window = sg.Window('Table', layout)
event, values = window.read()

new_data = []
new_data.append(result[0])  # 添加表头

for row in result[1:33]:
    try:
        val = float(row[6])
    except ValueError:
        val = 0

    if val > 0.3:
        new_data.append(list(row))

layout = [[sg.Table(new_data)]]
window = sg.Window('New Data', layout)
event, values = window.read()
