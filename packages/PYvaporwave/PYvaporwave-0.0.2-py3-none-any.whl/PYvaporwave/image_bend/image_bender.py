class ImageBend:

    _image = None

    def __init__(self, image):
        self._image = image

    def bend_image(self):
        print(self._image)