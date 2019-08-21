from PIL import Image
from os import makedirs, path

class Map:
    """
    This class is used to store the image in memory. It has the following fields:

    - fileName : Name of the image opened

    - img : The image object (used to output)

    - pixels : The 2D array containing pixel data.

    - sx, sy : The x and y dimensions of the image. The top left pixel (start) 
               is at (0,0). x increases as you go right, and y increases as you go down. The 
               bottom right pixel (target) is located at (sx-1, sy-1)

    - path : Initialized to be an empty array, but you needs to add in the pixels along the 
             fastest path in here to have it output correctly. Each element in this should 
             be a tuple of (x,y) coordinates in order of the path found.

             For example:
             path = [(0,0), (0,1), (1,1), ... , (sx-1, sy-1)]

             Means path found starts at (0,0), then goes to (0,1), then to (1,1), etc.
    """

    def __init__(self, filePath):
        with open(filePath, 'rb') as img_handle:
            self.fileName = path.basename(filePath)
            self.img = Image.open(img_handle)
            (sx, sy) = self.img.size
            self.pixels = self.img.load()
            self.path = []
            self.sx = sx
            self.sy = sy

    def outputPath(self):
        """
        Outputs an image with the name Path-<fileName> (in the 'output' folder) which displays the path 
        stored in self.path. The path is coloured green, with pixels at start being a brighter green 
        and towards the end being a darker green. 
        """
        if self.path == []:
            print('Nothing in path. Skipping output...')
            return

        makedirs('output', exist_ok=True)
        # Scaling factor to gradually change colour
        ptImg = self.img.copy()
        ptPix = ptImg.load()
        l = 120.0 / len(self.path)
        for i, coords in enumerate(self.path):
            ptPix[coords] = (0, 255-int(i*l), 0)
        ptImg.save('output/Path-'+self.fileName)
        ptImg.close()
