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
            ch_dict = self.get_chapter_dict()
            output = []
            for i in ch_dict:
                output.append(i)
            return output
        return chapters, last_volume

    def get_chapter_dict(self):
        manga_dict = api.get_manga_volumes_and_chapters(
            manga_id=self.id, translatedLanguage=['en'])
        chapters_dict_ = {}
        for i in dict(manga_dict).keys():
            chapters_dict_.update(manga_dict[i]['chapters'])
        chapter_dict = {}
        for i in chapters_dict_:
            chapter_dict[i] = chapters_dict_[i]['id']
        return chapter_dict
