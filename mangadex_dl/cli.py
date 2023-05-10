'''
mangadex-dl CLI

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
from mangadex_dl.organiser import Organiser
from mangadex_dl.manga import Manga
from mangadex_dl.chapter import MangaChapter
from mangadex_dl.constants import VERSION
from mangadex_dl.library import add_item, library
import os
from shutil import rmtree
from random import randint
import argparse
import sys

SUPPRESS = '==SUPPRESS=='


class LibraryAction(argparse.Action):

    def __init__(self,
                 option_strings,
                 dest=SUPPRESS,
                 default=None,
                 help="start a library session where you can view and modify your local library"):
        super(LibraryAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        library()
        parser.exit()


parser = argparse.ArgumentParser(prog='mangadex-dl',
                                 formatter_class=argparse.RawDescriptionHelpFormatter, usage='mangadex-dl [options]',
                                 description='Python CLI that downloads manga from mangadex.org as PDF or images', epilog='in case of suggestions or bugs, please open an issue on the project github :\nhttps://github.com/john-erinjery/mangadex-dl')
parser.add_argument('-v', '--version', action="version",
                    version=f'mangadex-dl {VERSION}')
parser.add_argument('-lib', '--library', action=LibraryAction)
parser.add_argument('-t', '--manga-url', action='store',
                    help='the manga homepage url', type=str, dest='manga_url', metavar='')
parser.add_argument('-tcode', '--manga-code', type=int,
                    help='The library code of the manga, as stored in local lib', dest='tcode', metavar='', action='store', default=None)
parser.add_argument('-c', '--chapter-url',
                    help='the chapter url', dest='chapter_url', metavar='')
parser.add_argument('-pdf', help='organise manga into chapterwise PDFs',
                    dest='pdf', action='store_true', default=False)
parser.add_argument('-m', '--merge', help="merge chapter PDFs into single PDF (-pdf must be provided)",
                    dest='merge', action='store_true', default=False)
parser.add_argument('-img', help="organise manga into chapterwise image folders",
                    dest='img', action='store_true', default=False)
parser.add_argument('-s', '--single-folder', help="organise manga into chapterwise image folders (-img must be provided)",
                    dest='single_folder', action='store_true', default=False)
parser.add_argument('--data', help='enable data saver (default)',
                    action='store_true', dest='data_saver', default=True)
parser.add_argument('-r', '--range', action='extend', nargs=2,
                    help='range of chapters to download, eg: -r 1 5 (download chapters 1 - 4)', dest='range', metavar='', type=int)
parser.add_argument('-tl', '--translated-language', action='store', default='en',
                    help='language code of translation (default : en, others availiable on github homepage)', metavar='', dest='tl')
arg_dict = dict(parser.parse_args()._get_kwargs())


def main():
    '''
    Main Entry Point of the CLI
    '''
    organiser = Organiser(args_dict=arg_dict)

    if not organiser.args_evaluvator():
        sys.exit()

    folder_name = 'manga' + str(randint(10000, 99999))
    os.mkdir(folder_name)
    os.chdir(folder_name)

    if organiser.chapter_url != None:
        chp = MangaChapter(organiser.chapter_url)
        if chp.chapter_name != None:
            print(
                f'\nStarting download of Chapter {chp.chapter_number} : {chp.chapter_name}')
        print(
            f'initialising download in folder : {os.getcwd()}')

        chp.download_chapter(organiser.data_saver)
        if organiser.pdf:
            ch_img_dict = eval(open('all_images_paths_ch_dict.txt').read())
            organiser.convert_chapter_images_to_pdf(ch_img_dict)
            os.rename(f'pdf/{chp.chapter_number}.pdf',
                      f'../Chapter {chp.chapter_number}.pdf')
        else:
            os.rename(str(chp.chapter_number),
                      f'../Chapter {chp.chapter_number}')
        print('deleting cache and temp folder..')
        os.chdir('..')
        rmtree(folder_name)
        print('done!')
        sys.exit()

    manga = Manga(organiser.manga_url, translation=organiser.tl)
    if manga.title:
        print('\nStarting download of {}..'.format(manga.title))
        add_item((manga.title, organiser.range_, organiser.manga_url))
    else:
        add_item(('<no-eng-title>', organiser.range_, organiser.manga_url))
    print('initialising download in folder : {}'.format(os.getcwd()))
    print('getting chapters and volumes..')
    ch_dict = manga.get_chapter_dict(organiser.range_)

    for i in ch_dict:
        chapter = MangaChapter(
            'https://mangadex.org/chapter/{}'.format(ch_dict[i]))

        try:
            all_ch_imgs_dict = chapter.download_chapter(organiser.data_saver)
        except:
            if organiser.pdf:
                print('\nconverting downloaded chapters to pdf..')
            else:
                organiser.range_[1] = float(i) - 1.0
                print('organising downloaded image folders..')
            rmtree(i)
            break

        if organiser.pdf:
            organiser.convert_chapter_images_to_pdf(all_ch_imgs_dict)
    if organiser.pdf:
        if organiser.merge:
            organiser.pdf_merger()
        else:
            os.rename(
                'pdf', f'../chapter {organiser.range_[0]}-{organiser.range_[1]}')
    if organiser.img:
        if organiser.single_folder:
            organiser.single_folder_images()
            os.rename(
                'imgs', f'../chapter {organiser.range_[0]}-{organiser.range_[1]}')
        else:
            print('organising image folders..')
            for i in os.listdir('.'):
                if os.path.isfile(i):
                    os.remove(i)
            os.chdir('..')
            os.rename(
                folder_name, f'Chapter {organiser.range_[0]}-{organiser.range_[1]}')
            print('done!')
            sys.exit()
    print('deleting cache and temp folders..')
    os.chdir('..')
    rmtree(folder_name)
    print('done!')


if __name__ == '__main__':
    main()
