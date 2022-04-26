"""
Copyright 2022 Michal Rendek
Licenced to MIT https://spdx.ogr/licenses/MIT.html

This module implements the solution for generators and scheduler
"""
import math
import numpy
from numba import cuda
from PIL import Image


@cuda.jit
def convert_image(img_data):
    """
    Cuda function for change image from grayscale to white black image
    :param img_data: data about image grayscale pixel color
    """
    x, y = cuda.grid(2)
    # if pixel color is less then 127 set pixel to black else to white
    if img_data[x][y] < 127:
        img_data[x][y] = 0
    else:
        img_data[x][y] = 255


if __name__ == "__main__":
    # load image and convert to grayscale
    img = Image.open("img.jpg").convert('L')
    # read data from image to array
    data = numpy.array(img.getdata(), dtype=numpy.uint8)
    data = numpy.resize(data, (img.size[1], img.size[0]))
    # show image for check
    img = Image.fromarray(data)
    img.show()
    # creat threads block 16 x 16
    tb = (16, 16)
    # calculate block grid size
    bgx = math.ceil(data.shape[0] / tb[0])
    bgy = math.ceil(data.shape[1] / tb[1])
    bg = (bgx, bgy)
    # run conversion
    convert_image[bg, tb](data)
    # show final image
    img = Image.fromarray(data)
    img.show()
