import mangadex
api = mangadex.Api()


class Manga:
    def __init__(self, _url, translation) -> None:
        self.url = _url
        self.tl = translation
        self.id = self.url.split('/')[-2]
        self.title = self.name_of_manga()

    def name_of_manga(self):
        try:
            return api.view_manga_by_id(manga_id=self.id).title[self.tl]
        except:
            return ''

    def get_chapter_dict(self, range_) -> dict:
        manga_dict = api.get_manga_volumes_and_chapters(
            manga_id=self.id, translatedLanguage=[self.tl])
        chapters_dict_ = {}
        for i in manga_dict.keys():
            chaps = manga_dict[i]['chapters']
            for j in chaps:
                floated_j = float(j)
                if (range_[0] <= floated_j < range_[1]):
                    chapters_dict_.update(
                        {floated_j: chaps[j]['id']})
        chapters_dict_ = dict(sorted(chapters_dict_.items()))
        return chapters_dict_
