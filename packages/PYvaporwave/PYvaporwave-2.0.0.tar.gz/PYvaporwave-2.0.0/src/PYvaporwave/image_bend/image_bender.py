import io
import math
from random import randrange
from PIL import Image, ImageFile
import numpy as np

class ImageBend:

    _image = None
    _title = None
    _pixel_array = None
    _bytemap = None

    def __init__(self, image, title):
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        self._image = image
        self._title = title
        self._pixel_array = np.asarray(Image.open(self._image.path))
        self._bytemap = self._get_image_bytemap()


    def _get_image_bytemap(self):
        _bytemap = None
        with open(self._image.path, 'rb') as img:
            _bytemap = img.read()
            img.close
        return _bytemap


    def _unpack_pixel(self, r, g, b, alpha = 255):
        return 110, g, 110, alpha


    def _pixel_list_to_image(self, _pixel_list):
        _img_array = np.asarray(_pixel_list)
        return Image.fromarray(
                _img_array.astype(np.uint8) #some unknown magic that somehow works (has to do with how PIL library reads images)
            )


    def ultra_bend_image(self):
        bytemap = self._bytemap
        _newBytemap = list(self._bytemap)
        grab_min = int(len(_newBytemap)/2000)
        grab_max = int(len(_newBytemap)/500)

        for i in range (0,10):
            grab_index = randrange(50, len(bytemap) - grab_max)
            grab = randrange(randrange(1, grab_min), randrange(grab_min + 1, grab_max))
            _tmp = []

            for j in range(grab_index, grab_index + grab - 1):
                _tmp.append(bytemap[j])

            while True:
                insert = randrange(50, len(bytemap) - grab_max)
                if insert != grab_index:
                    break

            for k in range(insert, insert + grab - 1):
                _newBytemap[k] = _tmp[0]
                _tmp.pop(0)
        
        return Image.open(io.BytesIO(bytes(_newBytemap)))



    def bend_image(self):
        myimage = Image.open(self._image.path) #Load image to Pillow module for image processing
        iar = np.asarray(myimage) #Convert image to an array of Pixels
        
        my_pixel_list = [] #My own pixel list on which I might apply whatever process I wish
        for row, pixels in enumerate(iar): #each iterration goes through a different row of pixels
            my_pixel_list.append([])
            for pxl in pixels: #each iterration goes through a single pixel of the current row
                r, g, b, a = self._unpack_pixel(*pxl) 
                my_pixel_list[row].append([r, g, b, a])
        
        bent_image = self._pixel_list_to_image(my_pixel_list)
        return bent_image


    def scramble(self, slices = 4):
        y_intervals = []
        for i in range(0, slices):
            range_1 = math.ceil((len(self._pixel_array) / slices)) * i
            if i != 0:
                range_1 += 1
            
            if i != slices - 1:
                range_2 = math.ceil(len(self._pixel_array) / slices) * (i + 1)
            else:
                range_2 = len(self._pixel_array)

            y_intervals.append(
                {
                    "from": range_1,
                    "to" : range_2
                }
            )

        x_intervals = []
        for i in range(0, slices):
            range_1 = math.ceil((len(self._pixel_array[0]) / slices)) * i
            if i != 0:
                range_1 += 1
            
            if i != slices - 1:
                range_2 = math.ceil(len(self._pixel_array[0]) / slices) * (i + 1)
            else:
                range_2 = len(self._pixel_array[0])
            
            x_intervals.append(
                {
                    "from": range_1,
                    "to" : range_2
                }
            )


        return {
            "intervals": {
                "bytes": list(self._bytemap[0:10]),
                "width": x_intervals,
                "height" : y_intervals
            }
        }
