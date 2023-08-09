import numpy as np
from PIL import Image
import colorsys
import io
from math import sqrt, atan2, pi

'''
We will be generating 300x300 PNG images in RGB.
'''
HEIGHT = 300
WIDTH = 300
RGB_VAL = 3

def __init__():
    return

# ============
#   INTERNAL
# ============

def attr_to_gen_input(tempo, valence, energy, acousticness) -> tuple[list[float], int]:
    '''
    Turn Spotify song attributes into HSV values.

    tempo: determines range of hues in gradient
    valence: determines starting hue, value
    energy: determines saturation (additive)
    acousticness: determines saturation (subtractive)

    Returns a tuple containing:
        - list of HSV values between 0.0 and 1.0
        - range between 1-?
    '''

    # starts at blue (low valence), wraps around the color spectrum
    hue = (.5 + valence)
    if hue > 1:
        hue -= 1
    
    # 35% to 100%
    saturation = .35 + (energy * .65) - (acousticness * .35)

    # 50% to 100%
    value = .6 + (valence * .4)

    # how many increments of 35 over 90 bpm
    range = ((tempo - 90) // 20)
    if range < 1:
        range = 1

    return ([hue, saturation, value], range)

# ====================
#   RGB Interpolation
# ====================

def gen_linear_horiz_grad_rgb_interp(c1, c2) -> io.BytesIO():
    '''
    Generate an image with a two-color linear horizontal gradient using HSV values.

    Returns PNG data in BytesIO object.
    '''
    
    # convert hsv floats to rgb ints
    c1 = list(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(c1[0], c1[1], c1[2]))))
    c2 = list(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(c2[0], c2[1], c2[2]))))

    # generate starting array
    a = np.zeros((HEIGHT, WIDTH, RGB_VAL), dtype='uint8')

    # interpolate between the two colors
    for i in range(WIDTH):
        for j in range(HEIGHT):
            a[i][j][0] = int((c2[0] - c1[0]) * (j / HEIGHT) + c1[0])
            a[i][j][1] = int((c2[1] - c1[1]) * (j / HEIGHT) + c1[1])
            a[i][j][2] = int((c2[2] - c1[2]) * (j / HEIGHT) + c1[2])
    
    # make an image from the array and save it as a PNG
    img = Image.fromarray(a)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes

def gen_linear_vert_grad_rgb_interp(c1, c2) -> io.BytesIO():
    '''
    Generate an image with a two-color linear vertical gradient using HSV values.

    Returns PNG data in BytesIO object.
    '''

    # convert hsv floats to rgb ints
    c1 = list(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(c1[0], c1[1], c1[2]))))
    c2 = list(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(c2[0], c2[1], c2[2]))))

    # generate starting array
    a = np.zeros((HEIGHT, WIDTH, RGB_VAL), dtype='uint8')

    # interpolate between the two colors
    for i in range(WIDTH):
        for j in range(HEIGHT):
            a[i][j][0] = int((c2[0] - c1[0]) * (i / HEIGHT) + c1[0])
            a[i][j][1] = int((c2[1] - c1[1]) * (i / HEIGHT) + c1[1])
            a[i][j][2] = int((c2[2] - c1[2]) * (i / HEIGHT) + c1[2])
    
    # make an image from the array and save it as a PNG
    img = Image.fromarray(a)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes

def distance_toward_center(coord, center):
    if coord > center:
        return center * 2 - coord
    return coord

def gen_linear_diamond_grad_rgb_interp(c1, c2) -> io.BytesIO():
    '''
    Generate an image with a two-color linear diamond-shaped gradient using HSV values.

    Returns PNG data in BytesIO object.
    '''
    
    # convert hsv floats to rgb ints
    c1 = list(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(c1[0], c1[1], c1[2]))))
    c2 = list(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(c2[0], c2[1], c2[2]))))

    # generate starting array
    a = np.zeros((HEIGHT, WIDTH, RGB_VAL), dtype='uint8')
    
    center = HEIGHT / 2

    # interpolate between the two colors
    for i in range(HEIGHT):
        for j in range(WIDTH):
            a[i][j][0] = int((c2[0] - c1[0]) * (((distance_toward_center(i, center) / center) + (distance_toward_center(j, center) / center))/2) + c1[0])
            a[i][j][1] = int((c2[1] - c1[1]) * (((distance_toward_center(i, center) / center) + (distance_toward_center(j, center) / center))/2) + c1[1])
            a[i][j][2] = int((c2[2] - c1[2]) * (((distance_toward_center(i, center) / center) + (distance_toward_center(j, center) / center))/2) + c1[2])
    
    # make an image from the array and save it as a PNG
    img = Image.fromarray(a)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes

def gen_linear_radial_grad_rgb_interp(c1, c2) -> io.BytesIO():
    '''
    Generate an image with a two-color linear radial gradient using HSV values.

    Returns PNG data in BytesIO object.
    '''
    
    # convert hsv floats to rgb ints
    c1 = list(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(c1[0], c1[1], c1[2]))))
    c2 = list(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(c2[0], c2[1], c2[2]))))

    # generate starting array
    a = np.zeros((HEIGHT, WIDTH, RGB_VAL), dtype='uint8')
    
    center = HEIGHT / 2
    radius = HEIGHT / 2

    # interpolate between the two colors
    for y in range(HEIGHT):
        for x in range(WIDTH):
            a[y][x][0], a[y][x][1], a[y][x][2] = radial_alg_rgb(c1, c2, radius, center, y, x)
    
    # make an image from the array and save it as a PNG
    img = Image.fromarray(a)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes

def radial_alg_rgb(c1, c2, radius, center, x, y):
    dist_from_center = (sqrt((x - center) ** 2 + (y - center) ** 2))
    if(dist_from_center > radius):
        return (c1[0], c1[1], c1[2])
    else:
        r = int((c2[0] - c1[0]) * ((radius - dist_from_center) / radius) + c1[0])
        g = int((c2[1] - c1[1]) * ((radius - dist_from_center) / radius) + c1[1])
        b = int((c2[2] - c1[2]) * ((radius - dist_from_center) / radius) + c1[2])
        return (r, g, b)

# ====================
#   HSV INTERPOLATION
# ====================

def gen_linear_horiz_grad_hsv_interp(c1, c2) -> io.BytesIO():
    '''
    Generate an image with a two-color linear horizontal gradient using HSV values.
    Interpolation over the HSV colorspace.

    Returns PNG data in BytesIO object.
    '''

    # generate starting array
    a = np.zeros((HEIGHT, WIDTH, RGB_VAL), dtype='uint8')

    # interpolate between the two colors
    for i in range(WIDTH):
        for j in range(HEIGHT):
            h = ((c2[0] - c1[0]) * (j / HEIGHT) + c1[0])
            s = ((c2[1] - c1[1]) * (j / HEIGHT) + c1[1])
            v = ((c2[2] - c1[2]) * (j / HEIGHT) + c1[2])

            a[i][j][0], a[i][j][1], a[i][j][2] = tuple(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(h, s, v))))
    
    # make an image from the array and save it as a PNG
    img = Image.fromarray(a)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes

def gen_linear_vert_grad_hsv_interp(c1, c2) -> io.BytesIO():
    '''
    Generate an image with a two-color linear vertical gradient using HSV values.

    Returns PNG data in BytesIO object.
    '''

    # generate starting array
    a = np.zeros((HEIGHT, WIDTH, RGB_VAL), dtype='uint8')

    # interpolate between the two colors
    for i in range(WIDTH):
        for j in range(HEIGHT):
            h = ((c2[0] - c1[0]) * (i / HEIGHT) + c1[0])
            s = ((c2[1] - c1[1]) * (i / HEIGHT) + c1[1])
            v = ((c2[2] - c1[2]) * (i / HEIGHT) + c1[2])

            a[i][j][0], a[i][j][1], a[i][j][2] = tuple(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(h, s, v))))
    
    # make an image from the array and save it as a PNG
    img = Image.fromarray(a)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes

def gen_linear_diamond_grad_hsv_interp(c1, c2) -> io.BytesIO():
    '''
    Generate an image with a two-color linear diamond-shaped gradient using HSV values.

    Returns PNG data in BytesIO object.
    '''

    # generate starting array
    a = np.zeros((HEIGHT, WIDTH, RGB_VAL), dtype='uint8')
    
    center = HEIGHT / 2

    # interpolate between the two colors
    for i in range(HEIGHT):
        for j in range(WIDTH):
            h = ((c2[0] - c1[0]) * (((distance_toward_center(i, center) / center) + (distance_toward_center(j, center) / center))/2) + c1[0])
            s = ((c2[1] - c1[1]) * (((distance_toward_center(i, center) / center) + (distance_toward_center(j, center) / center))/2) + c1[1])
            v = ((c2[2] - c1[2]) * (((distance_toward_center(i, center) / center) + (distance_toward_center(j, center) / center))/2) + c1[2])

            a[i][j][0], a[i][j][1], a[i][j][2] = tuple(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(h, s, v))))
    
    # make an image from the array and save it as a PNG
    img = Image.fromarray(a)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes

def gen_linear_radial_grad_hsv_interp(c1, c2) -> io.BytesIO():
    '''
    Generate an image with a two-color linear radial gradient using HSV values.

    Returns PNG data in BytesIO object.
    '''

    # generate starting array
    a = np.zeros((HEIGHT, WIDTH, RGB_VAL), dtype='uint8')
    
    center = HEIGHT / 2
    radius = HEIGHT / 2

    # interpolate between the two colors
    for y in range(HEIGHT):
        for x in range(WIDTH):
            h, s, v = radial_alg_hsv(c1, c2, radius, center, y, x)
            a[y][x][0], a[y][x][1], a[y][x][2] = tuple(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(h, s, v))))
    
    # make an image from the array and save it as a PNG
    img = Image.fromarray(a)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes

def radial_alg_hsv(c1, c2, radius, center, x, y):
    dist_from_center = (sqrt((x - center) ** 2 + (y - center) ** 2))
    if(dist_from_center > radius):
        return (c1[0], c1[1], c1[2])
    else:
        h = ((c2[0] - c1[0]) * ((radius - dist_from_center) / radius) + c1[0])
        s = ((c2[1] - c1[1]) * ((radius - dist_from_center) / radius) + c1[1])
        v = ((c2[2] - c1[2]) * ((radius - dist_from_center) / radius) + c1[2])
        return (h, s, v)

def gen_linear_conic_grad_hsv_interp(c1, c2) -> io.BytesIO():
    '''
    Generate an image with a two-color linear conic gradient using HSV values.

    Returns PNG data in BytesIO object.
    '''

    # generate starting array
    a = np.zeros((HEIGHT, WIDTH, RGB_VAL), dtype='uint8')

    # interpolate between the two colors
    for y in range(HEIGHT):
        for x in range(WIDTH):
            h, s, v = conic_alg_hsv(c1, c2, (x - 150), (y - 150))
            a[y][x][0], a[y][x][1], a[y][x][2] = tuple(map(lambda x: int(x * 255), list(colorsys.hsv_to_rgb(h, s, v))))
    
    # make an image from the array and save it as a PNG
    img = Image.fromarray(a)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes

def conic_alg_hsv(c1, c2, x, y):

    degree = atan2(y, x)
    degree += pi

    percentage = degree / (2 * pi)

    h = ((c2[0] - c1[0]) * percentage + c1[0])
    s = ((c2[1] - c1[1]) * percentage + c1[1])
    v = ((c2[2] - c1[2]) * percentage + c1[2])

    return (h, s, v)

# ============
#   EXTERNAL
# ============

def gen_linear_horiz_grad_from_attr(tempo, valence, energy, acousticness) -> io.BytesIO():
    '''
    Generate a linear horizontal gradient image from song attributes.

    tempo: determines range of hues in gradient
    valence: determines starting hue, value
    energy: determines saturation (additive)
    acousticness: determines saturation (subtractive)

    Returns PNG data in BytesIO object.
    '''
    generator_inputs = attr_to_gen_input(tempo, valence, energy, acousticness)
    hsv = generator_inputs[0]
    range = generator_inputs[1]
    
    c1 = hsv
    c2 = [c1[0] + .2 * range, c1[1], c1[2]]
    return gen_linear_horiz_grad_hsv_interp(c1, c2)

def gen_linear_vert_grad_from_attr(tempo, valence, energy, acousticness) -> io.BytesIO():
    '''
    Generate a linear vertical gradient image from song attributes.

    tempo: determines range of hues in gradient
    valence: determines starting hue, value
    energy: determines saturation (additive)
    acousticness: determines saturation (subtractive)

    Returns PNG data in BytesIO object.
    '''
    generator_inputs = attr_to_gen_input(tempo, valence, energy, acousticness)
    hsv = generator_inputs[0]
    range = generator_inputs[1]
    
    c1 = hsv
    c2 = [c1[0] + .2 * range, c1[1], c1[2]]
    return gen_linear_vert_grad_hsv_interp(c1, c2)

def gen_linear_radial_grad_from_attr(tempo, valence, energy, acousticness) -> io.BytesIO():
    '''
    Generate a linear radial gradient image from song attributes.

    tempo: determines range of hues in gradient
    valence: determines starting hue, value
    energy: determines saturation (additive)
    acousticness: determines saturation (subtractive)

    Returns PNG data in BytesIO object.
    '''
    generator_inputs = attr_to_gen_input(tempo, valence, energy, acousticness)
    hsv = generator_inputs[0]
    range = generator_inputs[1]
    
    c1 = hsv
    c2 = [c1[0] + .2 * range, c1[1], c1[2]]
    return gen_linear_radial_grad_hsv_interp(c1, c2)

def gen_linear_diamond_grad_from_attr(tempo, valence, energy, acousticness) -> io.BytesIO():
    '''
    Generate a linear diamond-shaped gradient image from song attributes.

    tempo: determines range of hues in gradient
    valence: determines starting hue, value
    energy: determines saturation (additive)
    acousticness: determines saturation (subtractive)

    Returns PNG data in BytesIO object.
    '''
    generator_inputs = attr_to_gen_input(tempo, valence, energy, acousticness)
    hsv = generator_inputs[0]
    range = generator_inputs[1]
    
    c1 = hsv
    c2 = [c1[0] + .2 * range, c1[1], c1[2]]
    return gen_linear_diamond_grad_hsv_interp(c1, c2)

def gen_linear_conic_grad_from_attr(tempo, valence, energy, acousticness) -> io.BytesIO():
    '''
    Generate a linear diamond-shaped gradient image from song attributes.

    tempo: determines range of hues in gradient
    valence: determines starting hue, value
    energy: determines saturation (additive)
    acousticness: determines saturation (subtractive)

    Returns PNG data in BytesIO object.
    '''
    generator_inputs = attr_to_gen_input(tempo, valence, energy, acousticness)
    hsv = generator_inputs[0]
    range = generator_inputs[1]
    
    c1 = hsv
    c2 = [c1[0] + .2 * range, c1[1], c1[2]]
    return gen_linear_conic_grad_hsv_interp(c1, c2)

# ============
#   Testing
# ============

if __name__ == '__main__':

    # These are hardcoded values just used for testing the appearance of gradients.

    # asobi seksu: strawberries
    img_data = gen_linear_conic_grad_from_attr(tempo=130.542, valence=0.350, energy=0.859, acousticness=0.000322)
    img = Image.open(fp=img_data)
    img.save(fp="strawberries.png")


    # caroline polachek: welcome to my island
    img_data = gen_linear_conic_grad_from_attr(tempo=118.000, valence=0.360, energy=0.627, acousticness=0.0836)
    img = Image.open(fp=img_data)
    img.save(fp="welcome.png")

    # tennis: glorietta
    img_data = gen_linear_conic_grad_from_attr(tempo=169.034, valence=0.799, energy=0.839, acousticness=0.0183)
    img = Image.open(fp=img_data)
    img.save(fp="glorietta.png")

    # flying saucer attack: my dreaming hill
    img_data = gen_linear_conic_grad_from_attr(tempo=128.090, valence=0.197, energy=0.696, acousticness=0.233)
    img = Image.open(fp=img_data)
    img.save(fp="dreaming.png")

    # tv priest: bury me in my shoes
    img_data = gen_linear_conic_grad_from_attr(tempo=134.011, valence=0.0712, energy=0.663, acousticness=0.000184)
    img = Image.open(fp=img_data)
    img.save(fp="bury.png")

    # measuring windows playlist
    img_data = gen_linear_conic_grad_from_attr(tempo=115.35723333333331, valence=0.35263999999999995, energy=0.6138333333333332, acousticness=0.32758713)
    img = Image.open(fp=img_data)
    img.save(fp="windows.png")

    # let me play guitar in your math rock band playlist
    img_data = gen_linear_conic_grad_from_attr(tempo=123.25553571428567, valence=0.4888749999999999, energy=0.7668392857142857, acousticness=0.08682526839285713)
    img = Image.open(fp=img_data)
    img.save(fp="math.png")
