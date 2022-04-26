# Exercise nine

## CUDA
### Description 
Think of a problem that will run on CUDA and this will be needed to run it faster.
### Solution
#### Describe 
I wrote a program that converts an image into a black and white image.
#### Code
In first image is open
```python
 # load image and convert to grayscale
    img = Image.open("img.jpg").convert('L')
    # read data from image to array
```
Then data are store in array
```python
data = numpy.array(img.getdata(), dtype=numpy.uint8)
    data = numpy.resize(data, (img.size[1], img.size[0]))
    # show image for check
```
Next I initialize and calculate all needed params for CUDA thread grid system
```python
tb = (16, 16)
    # calculate block grid size
    bgx = math.ceil(data.shape[0] / tb[0])
    bgy = math.ceil(data.shape[1] / tb[1])
    bg = (bgx, bgy)
```
In last step I calculate new image pixels value
```python
# run conversion
    convert_image[bg, tb](data)
```
CUDA function
```python
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
```