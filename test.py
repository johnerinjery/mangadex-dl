import mangadex
api = mangadex.Api()
print(api.get_manga_volumes_and_chapters(
    'd0407445-b80d-4854-9f12-c8227f94cba6'))
