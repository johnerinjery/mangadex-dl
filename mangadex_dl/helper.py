'''
MangaDex-dl CLI

This Command Line Client uses the ManagDex API to download manga
and store it in image or PDF format.

You can choose whether to have the software merge all the chapters
downloaded into a single PDF, or have it in Chapterwise PDFs

If you choose to download manga in image format, you can choose
whether to save it in chapterwise folders or as a single large folder.
- this option is made to make it more convinient for readers to scroll
  through and read manga
- another feature is that if the files are named in a format that
  Andriod phones and PC's will be able to sort easily.
- it names files in the format aaa-1.jpg, aab-2.jpg...ect.
  if not, the file order will be quite messed up

This software is completely open source.
Feel free to use it as you like!

'''
import os
from mangadex_dl.constants import VERSION
abc = 'abcdefghijklmnopqrstuvwxyz'
base = os.path.dirname(os.path.abspath(__file__))


def make_sortable(stack):
    lenght = len(stack)
    prefixes = name_gen(lenght)
    result_stack = []
    for i in range(lenght):
        result_stack.append(prefixes[i] + '-' + str(stack[i]))
    return result_stack


def name_gen(lenght):
    n1 = 0
    n2 = 0
    n3 = 0
    name_list = []
    while n1 < 26:
        while n2 < 26:
            while (n3 < 26) and (len(name_list) < lenght):
                name_list.append(abc[n1] + abc[n2] + abc[n3])
                n3 += 1
            n2 += 1
            n3 = 0
        n1 += 1
        n2 = 0
        n3 = 0
    return name_list


def ret_float_or_int(num):
    if '.' in num:
        if (num.split('.')[1] != '0') and (num.split('.')[1] != '00'):
            return float(num)
        else:
            return int(num.split('.')[0])
    else:
        try:
            return int(num)
        except:
            return False


def path_prettify(path: str):
    new_path = path.replace('/', '\\')
    return new_path


def obj_at_next_index(obj, stack, steps=1):
    index = stack.index(obj) + 1
    if steps == 1:
        return stack[index]
    else:
        return stack[index: index + steps]
