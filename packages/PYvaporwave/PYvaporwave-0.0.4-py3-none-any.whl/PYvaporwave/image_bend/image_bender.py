from PIL import Image, ImageFile

import io

class ImageBend:

    _image = None
    _title = None
    _btArray = None

    def __init__(self, image, title):
        self._image = image
        self._title = title
        self._btArray = None
        self._image_to_bytearray()


    def _image_to_bytearray(self):
        with open(self._image.path, "rb") as image:
            f = image.read()
            btarray = bytearray(f)
            self._btArray = btarray


    def get_bytearray(self):
        return self._btArray


    def bend_image(self):
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        new_btArray = [b for b in self._btArray[0:100]]
        new_btArray += ([b for b in self._btArray[100:]])
       
       
        bendtImage = Image.open(io.BytesIO(bytearray(new_btArray)))
        bendtImage.show()
        print(bytearray(new_btArray))
        return (new_btArray)

        