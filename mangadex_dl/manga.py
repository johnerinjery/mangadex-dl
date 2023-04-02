from mangadex_dl.helper import ret_float_or_int
import mangadex
api = mangadex.Api()


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
        manga_dict = api.get_manga_volumes_and_chapters(
            manga_id=self.id, translatedLanguage=['en'])
        last_volume = list(manga_dict.keys())

        def chapters():
            ch_dict = self.get_chapter_dict([])
            output = []
            for i in ch_dict:
                output.append(i)
            return output
        return chapters, last_volume

    def get_chapter_dict(self, range_=[]):
        manga_dict = api.get_manga_volumes_and_chapters(
            manga_id=self.id, translatedLanguage=['en'])
        chapters_dict_ = {}
        for i in dict(manga_dict).keys():
            chapters_dict_.update(manga_dict[i]['chapters'])
        all_chapter_dict = {}
        for i in chapters_dict_:
            all_chapter_dict[i] = chapters_dict_[i]['id']
        if range_ == []:
            return all_chapter_dict
        all_ch_keys = list(float(x)
                           for x in all_chapter_dict.keys())
        all_ch_keys.sort()
        ch_dict = {}
        for i in all_ch_keys:
            if i >= range_[0] and i < range_[1]:
                ch_dict[str(i)] = all_chapter_dict[str(
                    ret_float_or_int(str(i)))]
        return ch_dict
