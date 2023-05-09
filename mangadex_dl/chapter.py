from mangadex_dl.helper import name_gen, update_file
import time
import requests
from shutil import copyfileobj
import os
import mangadex
import sys
api = mangadex.Api()


class MangaChapter:

    def __init__(self, ch_url) -> None:
        self.id = ch_url.split(
            '/')[-1] if ch_url[-1] != '/' else ch_url.split('/')[-2]
        self.__get_ch = api.get_chapter(self.id)
        self.chapter_number = str(self.__get_ch.chapter)
        self.chapter_name = self.__get_ch.title

    def __connect_to_server(self, _id: str):
        r = requests.get(
            url='https://api.mangadex.org/at-home/server/' + _id, timeout=10)
        data = r.json()

        baseurl = data['baseUrl']
        _hash = data['chapter']['hash']
        return data, baseurl, _hash

    def download_chapter(self, data_saver):
        ch_number = float(self.chapter_number)
        print('\ndownloading images for chapter {}..'.format(ch_number))
        os.mkdir(str(ch_number))
        all_ch_image_path = []
        try:
            data, baseurl, _hash = self.__connect_to_server(self.id)
            time.sleep(0.75)
        except:
            time.sleep(6.0)
            try:
                data, baseurl, _hash = self.__connect_to_server(self.id)
            except:
                print(
                    'ERROR: server is too crowded please wait a bit and re-run the program')
                sys.exit()

        image_url_list = []

        url = baseurl + '/data/' + _hash + \
            '/' if data_saver else '/data-saver/' + _hash + '/'
        for i in data['chapter']['data' if data_saver else 'dataSaver']:
            image_url_list.append(url + i)

        overlay = name_gen(len(image_url_list))
        unable_to_download = []

        for j in image_url_list:
            image_index = image_url_list.index(j)
            try:
                r = requests.get(j, stream=True)
            except:
                for i in range(6):
                    try:
                        r = requests.get(j, stream=True)
                        break
                    except:
                        time.sleep(5)
                        continue
                else:
                    unable_to_download.append(image_index + 1)
                    continue

            image_file_path = str(ch_number) + '/' + \
                overlay[image_index] + '-' + str(image_index + 1) + j[-4:]
            with open(image_file_path, 'wb') as f:
                r.raw.decode_content = True
                copyfileobj(r.raw, f)

            all_ch_image_path.append(
                image_file_path)

        if unable_to_download:
            print('unable to download page(s) {}. skipping page(s)..'.format(
                str(unable_to_download)))

        update_file('all_images_paths.txt', all_ch_image_path, 'list')
        update_file('all_images_paths_ch_dict.txt', {
                    ch_number: all_ch_image_path}, 'dict')
        return {ch_number: all_ch_image_path}
