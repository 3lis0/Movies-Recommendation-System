class PosterSizes:
    def __init__(self):
        self.w92 = 'w92'
        self.w154 = 'w154'
        self.w185 = 'w185'
        self.w342 = 'w342'
        self.w500 = 'w500'
        self.w780 = 'w780'
        self.original = 'original'
        
class BackdropSizes:
    def __init__(self):
        self.w342 = 'w300'
        self.w780 = 'w780'
        self.w780 = 'w1280'
        self.original = 'original'
        
class ImageInfo:
    def __init__(self):
        self.IMAGE_BASE_URL = "https://image.tmdb.org/t/p"
        self.poster_sizes = PosterSizes()
        self.backdrop_sizes = BackdropSizes()
        
    def get_url(self, size: str, path: str) -> str:
        return f"{self.IMAGE_BASE_URL}/{size}{path}"
        
