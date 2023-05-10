import csv
from prettytable import PrettyTable
import os
base = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(base, 'static/library.csv')


def _get_lib_data(tcode=False, return_both=False):
    reader = csv.reader(open(lib_path))
    data = [x for x in reader]
    if not tcode:
        return data
    else:
        for i in data:
            if i[0] == str(tcode):
                if not return_both:
                    return i
                else:
                    return data, i


def add_item(params: tuple):
    name = params[0]
    last_downloaded_str = f"{params[1][0]}-{params[1][1]}"
    part_url = params[2].split('/title/')[-1]
    part_url = part_url if part_url[-1] != '/' else part_url[:-1]
    data = _get_lib_data()
    for index, i in enumerate(data):
        if i[-1] == part_url:
            data[index][-2] = last_downloaded_str
            with open(lib_path, 'w') as f:
                writer = csv.writer(f, delimiter=',', lineterminator='\n')
                writer.writerows(data)
                print('manga updated in library..')
                return
    with open(lib_path, 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        sno = len(lines)
        f.seek(1)
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow([sno, name, last_downloaded_str, part_url])
        print('manga added to library')


def remove_item(code):
    data, dt = _get_lib_data(tcode=code, return_both=True)
    data.remove(dt)
    with open(lib_path, 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerows(data)
        print('item removed!')


def modify_item(code):
    data, dt = _get_lib_data(code, return_both=True)
    index = data.index(dt)
    op = input('''
enter the option of the detail you want to modify:

1. name
2. last-dowloaded range
3. url

(cant change the code, no)

Enter option : ''')
    if op == '1':
        new_name = input('enter new name : ')
        dt[1] = new_name
    elif op == '2':
        range_1 = input('enter first value : ')
        range_2 = input('enter second value : ')
        dt[2] = '-'.join([range_1, range_2])
    elif op == '3':
        url = input('enter new url : ')
        part_url = url.split('/title/')[-1]
        part_url = part_url if part_url[-1] != '/' else part_url[:-1]
        dt[3] = part_url

    data[index] = dt
    with open(lib_path, 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerows(data)
        print('item modified!')


def display_library():
    data = _get_lib_data()
    table = PrettyTable()
    table.hrules = 1
    table.left_padding_width = 1
    table.right_padding_width = 1
    table.field_names = data[0]
    table.max_width = 30
    for i in range(1, len(data)):
        table.add_row(data[i])
    print(table)


def library():
    while True:
        opn = input('''
mangadex-dl library

1. add manga
2. remove manga
3. modify manga in library
4. display library
5. quit

Enter option : ''')
        if opn == '1':
            name = input('enter manga name : ')
            read = input('enter how much you have read (ch num): ')
            url = input('enter the manga url : ')
            try:
                read = eval(read)
                if isinstance(read, list):
                    add_item((name, read, url))
                else:
                    read = [1, read]
                    add_item((name, read, url))
            except:
                read = [1, read]
                add_item((name, read, url))
            break
        elif opn == '2':
            code = input('enter library code of the manga : ')
            remove_item(code)
            break
        elif opn == '3':
            code = input('enter library code of the manga : ')
            modify_item(code)
        elif opn == '4':
            display_library()
            break
        elif opn == '5':
            break
        else:
            print('invalid option try again')
