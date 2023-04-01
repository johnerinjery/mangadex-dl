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
data_saver = True
single_folder = False
import mangadex
from PIL import Image, UnidentifiedImageError
import os
from random import randint
from shutil import rmtree, copyfileobj
from PyPDF2 import PdfMerger, PdfReader
import requests
import time

api = mangadex.Api()
merger = PdfMerger()
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

def path_prettify(path:str):
    new_path = path.replace('/', '\\')
    return new_path

'''
MangaDex Parent Class
'''

class Manga:
    def __init__(self, _url) -> None:
        self.url = _url
        self.id = self.url.split('/')[-2]
        self.title = self.name_of_manga()
        self.chapters = self.number_of_chaps_vols()[0]()
        self.volumes = self.number_of_chaps_vols()[1]
    
    def name_of_manga(self):
        try:
            return api.view_manga_by_id(manga_id=self.id).title['en']
        except:
            return ''

    def number_of_chaps_vols(self):
        manga_dict = api.get_manga_volumes_and_chapters(manga_id=self.id, translatedLanguage=['en'])
        last_volume = list(manga_dict.keys())
        def chapters():
            ch_dict = self.get_chapter_dict()
            output = []
            for i in ch_dict:
                output.append(i)
            return output
        return chapters, last_volume
    
    def get_chapter_dict(self):
        manga_dict = api.get_manga_volumes_and_chapters(manga_id=self.id, translatedLanguage=['en'])
        chapters_dict_ = {}
        for i in dict(manga_dict).keys():
            chapters_dict_.update(manga_dict[i]['chapters'])
        chapter_dict = {}
        for i in chapters_dict_:
            chapter_dict[i] = chapters_dict_[i]['id']
        return chapter_dict

class MangaChapter(Manga):

    def __init__(self, _id) -> None:
        self.id = _id
        self.chapter_number = str(api.get_chapter(_id).chapter)
            
    def download_chapter(self):
        ch_number = str(self.chapter_number)
        print('downloading images for chapter {}..'.format(ch_number))
        os.mkdir(ch_number)
        all_ch_image_path = []
        try:
            r = requests.get(url='https://api.mangadex.org/at-home/server/' + self.id)
            data = r.json()
            baseurl = data['baseUrl']
            hash = data['chapter']['hash']
        except:
            time.sleep(5.0)
            try:
                r = requests.get(url='https://api.mangadex.org/at-home/server/' + self.id)
                data = r.json()
                baseurl = data['baseUrl']
                hash = data['chapter']['hash']
            except:
                print('ERROR: server is too crowded please wait a bit and re-run the program')
                return 0
        
        image_list = []

        if data_saver:
            url = baseurl + '/data-saver/' + hash + '/'
            for j in data['chapter']['dataSaver']:
                image_list.append(url + j)
        else:
            url = baseurl + '/data/' + hash + '/'
            for j in data['chapter']['data']:
                image_list.append(url + j)
        
        overlay = name_gen(len(image_list))
        unable_to_download = []
        for j in image_list:
            try:
                r = requests.get(j, stream=True)
            except:
                n = 1
                while n < 10:
                    try:
                        r = requests.get(j, stream=True)
                        break
                    except:
                        n += 1
                        pass
                else:
                    unable_to_download.append(image_list.index(j) + 1)
                    continue
            
            with open(ch_number + '/' + overlay[image_list.index(j)] + '-' + str(image_list.index(j) + 1) + j[-4:], 'wb') as f:
                r.raw.decode_content = True
                copyfileobj(r.raw, f)

            all_ch_image_path.append(ch_number + '/' + overlay[image_list.index(j)] + '-' + str(image_list.index(j) + 1) + j[-4:])
            
        if unable_to_download:
            print('unable to download page(s) {}'.format(str(unable_to_download)))

        if os.path.exists('all_images_paths.txt'):

            with open('all_images_paths.txt', 'r') as f:
                all_images_paths_list = eval(f.read())
            with open('all_images_paths.txt', 'a'):
                f.write(str(all_images_paths_list.extend(all_ch_image_path)))
        
        else:

            with open('all_images_paths.txt', 'w') as f:
                f.write(str(all_ch_image_path))
        
    
        if os.path.exists('all_images_paths_ch_dict.txt'):
            ch_dict = {ch_number : all_ch_image_path}
            with open('all_images_paths_ch_dict.txt', 'r') as f:
                all_images_paths_ch_dict = eval(f.read())
            with open('all_images_paths_ch_dict.txt', 'a'):
                f.write(str(all_images_paths_ch_dict.update(ch_dict)))
        else:
            with open('all_images_paths_ch_dict.txt', 'w') as f:
                f.write(str({ch_number : all_ch_image_path}))
        
        return 1
        
class Organiser:
    
    def __init__(self, args_dict) -> None:
        # self.manga_url = args_dict['manga_url']
        # self.chapter_url = args_dict['chapter_url']
        # self.range_ = args_dict['range']
        # self.pdf = args_dict['pdf']
        # self.img = args_dict['img']
        # self.merge = args_dict['merge']
        # self.single_folder = args_dict['single_folder']
        # self.data_saver = args_dict['data_saver']
        pass
    
    def args_evaluvator(self):

        if self.manga_url == self.chapter_url == None:
            print('ERROR: manga or chapter url must be provided')
            return False
        elif self.manga_url != None and self.chapter_url != None:
            print('ERROR: both manga and chapter urls should not be provided')
            return False
        elif self.manga_url != None and self.range_ == []:
            print('ERROR: Range must be provided for manga urls')
            return False
        elif self.chapter_url != None and self.range_ != []:
            print('ERROR: Range should not be provided for chapter urls')
            return False
        elif self.pdf and self.img:
            print('ERROR: Manga cannot be stored as both image and pdf')
            return False
        elif self.merge and self.single_folder:
            print('ERROR: Cannot merge and single folder')
            return False
        elif self.pdf and self.single_folder:
            print('ERROR: Cannot be both pdf and single folder')
            return False
        elif self.img and self.merge:
            print('ERROR: Cannot be both img and merge')
            return False
        else:
            return True
    
    def conver_chapter_images_to_pdf(self, ch_image_path_:dict):
        ch_image_path = ch_image_path_
        image_list = list(ch_image_path.values())[0]
        image_objs = []
        for i in image_list:

            try:
                image_objs.append(Image.open(str(i)).convert('RGB'))
            except:
                pass


        