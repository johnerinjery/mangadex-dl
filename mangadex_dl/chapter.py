from mangadex_dl.helper import name_gen
import time
import requests
from shutil import copyfileobj
import os
import mangadex
from mangadex_dl.organiser import Organiser
api = mangadex.Api()


class MangaChapter(Organiser):

    def __init__(self, ch_url) -> None:
        self.id = ch_url.split('/')[-1]
        self.chapter_number = str(api.get_chapter(self.id).chapter)
        self.chapter_name = api.get_chapter(self.id).title

    def download_chapter(self, data_saver):
        ch_number = str(self.chapter_number)
        print('\ndownloading images for chapter {}..'.format(ch_number))
        os.mkdir(ch_number)
        all_ch_image_path = []
        try:
            r = requests.get(
                url='https://api.mangadex.org/at-home/server/' + self.id)
            data = r.json()
            baseurl = data['baseUrl']
            hash = data['chapter']['hash']
            time.sleep(0.8)
        except:
            time.sleep(6.0)
            try:
                r = requests.get(
                    url='https://api.mangadex.org/at-home/server/' + self.id)
                data = r.json()
                baseurl = data['baseUrl']
                hash = data['chapter']['hash']
            except:
                print(
                    'ERROR: server is too crowded please wait a bit and re-run the program')
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

            all_ch_image_path.append(
                ch_number + '/' + overlay[image_list.index(j)] + '-' + str(image_list.index(j) + 1) + j[-4:])

        if unable_to_download:
            print('unable to download page(s) {}. skipping page(s)..'.format(
                str(unable_to_download)))

        if os.path.exists('all_images_paths.txt'):

            with open('all_images_paths.txt', 'r') as f:
                all_images_paths_list = eval(f.read())
            with open('all_images_paths.txt', 'w') as f:
                all_images_paths_list.extend(all_ch_image_path)
                f.write(str(all_images_paths_list))

        else:

            with open('all_images_paths.txt', 'w') as f:
                f.write(str(all_ch_image_path))

        if os.path.exists('all_images_paths_ch_dict.txt'):
            ch_dict = {ch_number: all_ch_image_path}
            with open('all_images_paths_ch_dict.txt', 'r') as f:
                all_images_paths_ch_dict = eval(f.read())
            with open('all_images_paths_ch_dict.txt', 'w') as f:
                all_images_paths_ch_dict.update(ch_dict)
                f.write(str(all_images_paths_ch_dict))
        else:
            with open('all_images_paths_ch_dict.txt', 'w') as f:
                f.write(str({ch_number: all_ch_image_path}))
        return 1
