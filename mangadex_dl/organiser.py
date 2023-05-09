from PyPDF2 import PdfMerger, PdfReader
import os
from PIL import Image, UnidentifiedImageError
from mangadex_dl.helper import name_gen
from mangadex_dl.constants import LANGUAGE_CODES as lang_c
from mangadex import Api
api = Api()


class Organiser:

    def __init__(self, args_dict) -> None:
        self.manga_url = args_dict['manga_url']
        self.chapter_url = args_dict['chapter_url']
        self.range_ = args_dict['range']
        self.pdf = args_dict['pdf']
        self.img = args_dict['img']
        self.merge = args_dict['merge']
        self.single_folder = args_dict['single_folder']
        self.data_saver = args_dict['data_saver']
        self.tl = args_dict['tl']

    def args_evaluvator(self):

        if self.manga_url == self.chapter_url == None:
            print('ERROR: manga or chapter url must be provided')
            return False
        elif self.manga_url != None and self.chapter_url != None:
            print('ERROR: both manga and chapter urls should not be provided')
            return False
        elif self.manga_url != None and self.range_ == None:
            print('ERROR: Range must be provided for manga urls')
            return False
        elif self.chapter_url != None and self.range_ != None:
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
            if self.tl not in list(lang_c.keys()):
                print('ERROR: Invalid language code. Availiable language codes here : https://github.com/john-erinjery/mangadex-dl#codes')
                return False
            else:
                if self.manga_url != None:
                    if not api.get_manga_volumes_and_chapters(manga_id=self.manga_url.split('/')[-2], translatedLanguage=[self.tl]):
                        print(
                            'managdex does not have any availiable translations of this manga in', lang_c[self.tl])
                        return False
                    else:
                        return True
                else:
                    return True

    def convert_chapter_images_to_pdf(self, ch_image_path_: dict):
        '''
        Converts the given images into pdfs and saves it in a folder 'pdf'

        - the argument is a single element dictionary whose key is the chapter number and value is a list contaning
          paths to the chapter images
        '''
        print('converting chapter to PDF..\n')
        if not os.path.exists('pdf'):
            os.mkdir('pdf')
        image_list = list(ch_image_path_.values())[0]
        image_objs = []
        for i in image_list:
            try:
                image_objs.append(Image.open(str(i)).convert('RGB'))
            except:
                print('truncination error in image {}. skipping page..'.format(
                    image_list.index(i)))
                continue
        try:
            image_objs[0].save('pdf/' + str(list(ch_image_path_.keys())[0]) +
                               '.pdf', save_all=True, append_images=image_objs[1:])
        except UnidentifiedImageError:
            print('unidentified image detected, skipping..')

    def pdf_merger(self):
        '''
        Mergers all PDFs in the folder 'pdf'

        Error if 'pdf' does not exist.

        '''
        pdf_dir = [float(i[:-4]) for i in os.listdir('pdf')]
        pdf_dir.sort()
        merger = PdfMerger()
        print('merging chapters {} to {}..'.format(pdf_dir[0], pdf_dir[-1]))
        for i in pdf_dir:
            merger.append(PdfReader('pdf/{}.pdf'.format(i)))
        merger.write(f'../chapter {pdf_dir[0]}-{pdf_dir[-1]}.pdf')
        print('merge complete')

    def single_folder_images(self):
        '''
        Takes all images from chapterwise folders into a single folder 'imgs'
        '''
        os.mkdir('imgs')
        with open('all_images_paths_ch_dict.txt') as f:
            all_ch_dict = eval(f.read())
        overlay = name_gen(len(eval(open('all_images_paths.txt').read())))
        n = 0
        for i in all_ch_dict:
            for j in all_ch_dict[i]:
                os.rename(src=j, dst=f'imgs/{overlay[n]}-{n + 1}{j[-4:]}')
                n += 1
