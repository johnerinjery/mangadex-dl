import csv
from prettytable import PrettyTable
import os
base = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(base, 'static/library.csv')


def add_item(params: dict):
    with open(lib_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([params['code'], params['name'],
                        params['alternate'], params['last'], params['url']])


def remove_item(params: dict | None):
    with open(lib_path) as f:
        reader = csv.reader(f)
        data = [x for x in reader]
    for databit in data:
        datalist = databit.split(',')
        attrs = ['code', 'name', 'alternate', 'last', 'url']
        datadict = {attrs[datalist.index(x)]: x for x in datalist}
        for i in params:
            if params[i] == datadict[i]:
                data.remove(databit)
    print('Removed item form libra')


def display_library():
    reader = csv.reader(open(lib_path))
    data = [x for x in reader]
    table = PrettyTable()
    table.left_padding_width = 1
    table.right_padding_width = 1
    table.field_names = data[0]
    for i in range(1, len(data)):
        table.add_row(data[i])
    print(table)
