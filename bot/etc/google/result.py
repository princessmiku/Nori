

class Result:

    def __init__(self, title: str, description: str, url: str, image: str = None):
        self.title = title
        self.description = description[:1500] + "..."
        self.url = url
        self.image = image
