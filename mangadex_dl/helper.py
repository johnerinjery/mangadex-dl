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
VERSION = '1.3.0'
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


help_dict = {
    'general,': '''
MangaDex-dl CLI, a manga download software powered by MangaDex API
Usage : mangadex_dl [OPTION]

Startup:
    -h, --help              print this help message and exit
    -V, --version           display the version of MangaDex-dl

Download:
    -t, --manga-url                 the mangadex manga url (url is title page url)
    -c, --chapter-url               the mangadex chapter url (url is chapter url) (currently unavailiable)
    -r, --range                     the range of chapters to download. (if manga url provided)
    -pdf                            download manga as chapterwise pdfs (default)
    -img                            download manga as chapterwise images
    --data                          download manga in high quality
    -tl, --translated-language      the language code for managdex translations, run mangadex_dl --help -tl for more info

Post-Download-Processing:
    -m, --merge-pdf         merges all chapter pdfs into one file
    -s, --single-folder     collect all images into a single folder

for more information about an option,
Run mangadex_dl --help <option>

in case of bugs/issues/discussions please open an issue at
https://github.com/john-erinjery/mangadex-dl
''',
    '-h,--help': '''
MangaDex-dl CLI, a manga download software powered by MangaDex API
Usage : mangadex_dl [OPTION]

Startup:
    -h, --help              print this help message and exit
    -V, --version           display the version of MangaDex-dl

Download:
    -t, --manga-url                 the mangadex manga url (url is title page url)
    -c, --chapter-url               the mangadex chapter url (url is chapter url)
    -r, --range                     the range of chapters to download. (if manga url provided)
    -pdf                            download manga as chapterwise pdfs (default)
    -img                            download manga as chapterwise images
    --data                          download manga in high quality
    -tl, --translated-language      the language code for managdex translations, run mangadex_dl --help -tl for more info (default en)

Post-Download-Processing:
    -m, --merge-pdf         merges all chapter pdfs into one file
    -s, --single-folder     collect all images into a single folder

for more information about an option,
Run mangadex_dl --help <option>

in case of bugs/issues/discussions please open an issue at
https://github.com/john-erinjery/mangadex-dl
''',
    '-V,--version': f'current version of MangaDex-dl is {VERSION}',
    '-t,--manga-url': '\nThe MangaDex manga homepage url.\nNote that this is different from the chapter url. Manga URLs are of the form:\n\nhttps://mangadex.org/title/<manga-id>/<manga-name>\n\nfor eg: https://mangadex.org/title/9417ab7d-b231-4481-8279-34a873cc820f/chicchai-senpai-ga-kawaisugiru',
    '-c,--chapter-url': '\nThe MangaDex chapter url\nNote that this is different from the manga url. Chapter URLs are of the form:\n\nhttps://mangadex.org/chapter/<chapter-id>\n\nfor eg: https://mangadex.org/chapter/23deab8b-8866-401a-925d-115788a0027c',
    '-r,--range': 'The chapter range to be downloaded. Use only when providing Manga URLs.\n\nFormat : -r/--range <chapter-start> <chapter-end>\n\nTo download a single chapter pass the same value twice eg: --range 100 100',
    '-pdf': 'Downloads manga as chapter-wise pdfs. Output will be a folder "pdf" containing pdf files of the chapters.',
    '-img': 'Downloads mangs as chapter-wise image folders. Output will be an "imgs" folder containing image chapter folders',
    '-s,--single-folder': 'Option only availiable when downloading as image files. All images will be sorted and stored in a single folder.',
    '-m,--merge-pdf': 'Option only availiable when downloading as pdf files. All pdfs will be merged into a single pdf.',
    '--data': 'downloads manga in higher quality. note that the program might become slower with this option.',
    '-tl,--translated-language': 'the language code for managdex translations.\nall codes availiable here : '
}


def help_(func='general'):
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
    tl = 'en'
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
            elif i == '-tl' or i == '--translated-launguage':
                tl = obj_at_next_index(i, args)
            elif i == tl:
                continue
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
    return {'manga_url': manga_url, 'chapter_url': chapter_url, 'range': range_, 'pdf': pdf, 'img': img, 'merge': merge, 'single_folder': single_folder, 'data_saver': data_saver, 'tl': tl}
