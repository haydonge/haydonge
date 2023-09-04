# 2023 Sep 4 version 0.1  ， From Haydon Ge

import tkinter as tk
from tkinter import filedialog
import csv
import math
import PySimpleGUI as sg
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read(r'config.ini', encoding="utf-8")
cfg.sections()
z_limit = cfg.get('xyz', 'limit_z')
line_limit = cfg.get('xyz','line')
root = tk.Tk()


def select_file1():
    file1 = filedialog.askopenfilename()
    entry1.delete(0, tk.END)
    entry1.insert(0, file1)


def select_file2():
    file2 = filedialog.askopenfilename()
    entry2.delete(1, tk.END)
    entry2.insert(0, file2)


def quit():
    root.destroy()


def process():
    file1 = entry1.get()
    file2 = entry2.get()

    result = []

    with open(file1) as f1, open(file2) as f2:
        rdr1 = csv.reader(f1)
        rdr2 = csv.reader(f2)

        headers1 = next(rdr1)
        headers2 = next(rdr2)

        headers = headers1[:4] + ['X', 'Y', 'Result']
        result.append(headers)

        for row1 in rdr1:
            row2 = next(rdr2)

            new_row = row1[:4] + [row1[4], row2[4]]

            v1 = float(row1[4])
            v2 = float(row2[4])

            res = math.sqrt(v1 ** 2 + v2 ** 2)
            new_row.append(res)
            result.append(new_row)

    new_data = []
    new_data.append(result[0])  # 添加表头

    for row in result[1:int(line_limit)]:
        try:
            val = float(row[6])
        except ValueError:
            val = 0

        if val > float(z_limit):
            new_data.append(list(row))

    layout = [[sg.Table(new_data)]]
    window = sg.Window('New Data', layout)
    event, values = window.read()


tk.Label(root, text="CSV文件1:").grid(row=0, column=0)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

tk.Label(root, text="CSV文件2:").grid(row=3, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=3, column=1)

btn1 = tk.Button(root, text="选择文件1", command=select_file1)
btn1.grid(row=0, column=2)
btn1 = tk.Button(root, text="选择文件2", command=select_file2)
btn1.grid(row=3, column=2)
# 同样方式添加文件2的选择和Entry

btn_quit = tk.Button(root, text="退出程序", command=quit)
btn_quit.grid(row=6, column=2)

btn2 = tk.Button(root, text="处理程序", command=process)
btn2.grid(row=6, column=0)

root.mainloop()
