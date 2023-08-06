from PIL import Image
import numpy as np

class ImageBend:

    _image = None
    _title = None

    def __init__(self, image, title):
        self._image = image
        self._title = title

    def bend_image(self):
        myimage = Image.open(self._image.path) #Load image to Pillow module for image processing
        iar = np.asarray(myimage) #Convert image to an array of Pixels
        
        my_pixel_list = [] #My own pixel list on which I might apply whatever process I wish
        for row, pixels in enumerate(iar): #each iterration goes through a different row of pixels
            my_pixel_list.append([])
            for pxl in pixels: #each iterration goes through a single pixel of the current row
                r, g, b, a = self._unpack_pixel(*pxl) 
                my_pixel_list[row].append([r, g, b, a])
        
        my_pixel_list = np.asarray(my_pixel_list) #convert MY list to Array
        bent_image = Image.fromarray((my_pixel_list).astype(np.uint8)) #some unknown magic that somehow works (has to do with how PIL library reads images)
        
        return bent_image
    
    def scramble(self, pixel_array):
        #implement magic here
        pass

    def _unpack_pixel(self, r, g, b, alpha = 255):
        return r, g, b, alpha
        