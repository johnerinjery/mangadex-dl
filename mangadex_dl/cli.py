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

from sys import argv
from mangadex_dl.helper import *
from mangadex_dl.organiser import Organiser
from mangadex_dl.manga import Manga
from mangadex_dl.chapter import MangaChapter
import os
from shutil import rmtree
from random import randint
from time import sleep

VERSION = '1.3.0'
args = argv
arg_dict = get_arguments(args)


def main():
    '''
    Main Entry Point of the CLI
    '''
    if arg_dict != None:
        pass
    else:
        return

    organiser = Organiser(args_dict=arg_dict)

    if organiser.args_evaluvator():
        folder_name = 'manga' + str(randint(10000, 99999))
        os.mkdir(folder_name)
        os.chdir(folder_name)

        if organiser.pdf:

            if organiser.chapter_url != None:
                chapter = MangaChapter(organiser.chapter_url)
                print(
                    f'\nStarting download of Chapter {chapter.chapter_number} : {chapter.chapter_name}')
                print(
                    f'initialising download in folder : {os.getcwd()}')

                ret = chapter.download_chapter(organiser.data_saver)
                if ret == 1:
                    ch_img_path_dict = eval(
                        open('all_images_paths_ch_dict.txt').read())
                    organiser.convert_chapter_images_to_pdf(ch_img_path_dict)
                    os.rename(f'pdf/{chapter.chapter_number}.pdf',
                              f'../Chapter {chapter.chapter_number}.pdf')
                    print('deleting cache and temp folder..')
                    os.chdir('..')
                    rmtree(folder_name)
                    print('done!')

                else:
                    sleep(5.0)
                    ret = chapter.download_chapter(organiser.data_saver)
                    if ret != 1:
                        print(
                            'ERROR: Could not download chapter. Check your network connection and try again later.')

            else:
                manga = Manga(organiser.manga_url, translation=organiser.tl)
                print('\nStarting download of {}..'.format(manga.title))
                print('initialising download in folder : {}'.format(os.getcwd()))
                print('getting chapters and volumes..')
                ch_dict = manga.get_chapter_dict(organiser.range_)
                for i in ch_dict:
                    chapter = MangaChapter(
                        'https://mangadex.org/chapter/{}'.format(ch_dict[i]))
                    chapter.download_chapter(organiser.data_saver)
                    ch_images = None
                    with open('all_images_paths_ch_dict.txt') as f:
                        all_images_paths_ch_dict = eval(f.read())
                    for j in all_images_paths_ch_dict:
                        if str(i) == str(j):
                            ch_images = {
                                str(i): all_images_paths_ch_dict[str(i)]}
                            organiser.convert_chapter_images_to_pdf(ch_images)
                if organiser.merge:
                    organiser.pdf_merger()
                else:
                    os.rename(
                        'pdf', f'../Chapter {organiser.range_[0]}-{organiser.range_[1]}')
                print('\ndeleting cache and temp folder..')
                os.chdir('..')
                rmtree(folder_name)
                print('done!')

        else:

            if organiser.chapter_url != None:
                chapter = MangaChapter(organiser.chapter_url)
                print(
                    f'\nStarting download of Chapter {chapter.chapter_number} : {chapter.chapter_name}')
                print(
                    f'initialising download in folder : {os.path.join(os.getcwd(), folder_name)}')
                chapter.download_chapter(organiser.data_saver)
                for i in os.listdir('.'):
                    if os.path.isdir(i):
                        print('Organising image folder..')
                        os.rename(i, f'../Chapter {i}')
                print('deleting cache and temp folders..')
                os.chdir('..')
                rmtree(folder_name)
                print('done!')

            else:

                manga = Manga(organiser.manga_url, translation=organiser.tl)
                print('\nStarting download of {}..'.format(manga.title))
                print('initialising download in folder : {}'.format(os.getcwd()))
                print('getting chapters and volumes..')
                ch_dict = manga.get_chapter_dict(organiser.range_)
                for i in ch_dict:
                    chapter = MangaChapter(
                        'https://mangadex.org/chapter/{}'.format(ch_dict[i]))
                    chapter.download_chapter(organiser.data_saver)
                print('Organising Image folders..')
                if organiser.single_folder:
                    organiser.single_folder_images()
                    os.rename(
                        'imgs', f'../Chapter {organiser.range_[0]}-{organiser.range_[1]}')
                else:
                    for i in os.listdir('.'):
                        if os.path.isfile(i):
                            os.remove(i)
                    os.chdir('..')
                    os.rename(
                        folder_name, f'Chapter {organiser.range_[0]}-{organiser.range_[1]}')
                print('done!')


if __name__ == '__main__':
    main()
