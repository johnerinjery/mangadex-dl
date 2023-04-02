#!env python
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
VERSION = '2.0.0'
abc = 'abcdefghijklmnopqrstuvwxyz'


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


def help_(func='general'):
    with open('help-dict.txt') as f:
        help_dict = eval(f.read())
        help_dict_ops = []
        help_dict_all_ops = []
        for i in help_dict.keys():
            help_dict_ops.append(i.split(','))
            for j in i.split(','):
                if j != '':
                    help_dict_all_ops.append(j)
    if func not in help_dict_all_ops:
        print('ERROR : Invalid Option')
    else:
        for i in help_dict_ops:
            if func in i:
                print(help_dict[list(help_dict.keys())
                      [help_dict_ops.index(i)]])


def obj_at_next_index(obj, stack, steps=1):
    index = stack.index(obj) + 1
    if steps == 1:
        return stack[index]
    else:
        return stack[index: index + steps]


def get_arguments(args):
    manga_url = None
    chapter_url = None
    range_ = []
    range_1 = []
    pdf = True
    img = False
    merge = False
    single_folder = False
    data_saver = True
    if len(args) == 1:
        help_()
        return None
    elif len(args) == 2:
        if args[-1] == '-V' or args[-1] == '--version':
            help_('-V')
            return None
        elif args[-1] == '-h' or args[-1] == '--help':
            help_()
            return None
        else:
            print('ERROR: Invalid Syntax')
            return None
    elif len(args) == 3 and (('--help' in args) or ('-h' in args)):
        help_(args[-1])
        return None
    else:
        for i in args[1:]:
            if i == '-t' or i == '--manga-url':
                manga_url = obj_at_next_index(i, args)
            elif i == '-c' or i == '--chapter-url':
                chapter_url = obj_at_next_index(i, args)
            elif i == '-r' or i == '--range':
                range_1 = obj_at_next_index(i, args, 2)
                for i in range_1:
                    range_.append(ret_float_or_int(i))
                range_.sort()
            elif i == '-pdf':
                continue
            elif i == '-img':
                pdf = False
                img = True
            elif i == '-m' or i == '--merge-pdf':
                merge = True
            elif i == '--data':
                data_saver = False
            elif i == '-s' or i == '--single-folder':
                single_folder = True
            elif i in range_1:
                continue
            elif i == manga_url or i == chapter_url:
                continue
            else:
                print('ERROR: Invalid Option', i)
                return None
    return {'manga_url': manga_url, 'chapter_url': chapter_url, 'range': range_, 'pdf': pdf, 'img': img, 'merge': merge, 'single_folder': single_folder, 'data_saver': data_saver}
