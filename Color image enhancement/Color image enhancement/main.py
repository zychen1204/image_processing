from PIL import Image
import math

class RGB:
    def __init__(self, r, g, b):
        self.R = r
        self.G = g
        self.B = b

class HSI:
    def __init__(self, h=None, s=None, i=None):
        self.H = h
        self.S = s
        self.I = i

class LAB:
    def __init__(self, l=None, a=None, b=None):
        self.L = l
        self.A = a
        self.B = b

class XYZ:
    def __init__(self, x=None, y=None, z=None):
        self.X = x
        self.Y = y
        self.Z = z

def RGBtoHSI(rgb):
    r = rgb.R / 255.0
    g = rgb.G / 255.0
    b = rgb.B / 255.0
    denominator = math.sqrt((r - g) * (r - g) + (r - b) * (g - b))
    if denominator == 0:
        
        theta = 0  
    else:
        theta = math.acos(0.5 * ((r - g) + (r - b)) / denominator)
    hsi = HSI()
    hsi.H = theta if b <= g else (2 * math.pi - theta)
    
    denominator = r + g + b
    if denominator == 0:
        hsi.S = 0
    else:
        hsi.S = 1 - 3 * min(min(r, g), b) / denominator
    hsi.I = (r + g + b) / 3
    return hsi

def HSItoRGB(hsi):
    h = hsi.H
    s = hsi.S
    i = hsi.I
    s  +=5

    if 0 <= h < 2 * math.pi / 3:
        b = i * (1 - s)
        r = i * (1 + s * math.cos(h) / math.cos(math.pi / 3 - h))
        g = 3 * i - (r + b)
    elif 2 * math.pi / 3 <= h < 4 * math.pi / 3:
        r = i * (1 - s)
        g = i * (1 + s * math.cos(h - 2 * math.pi / 3) / math.cos(math.pi - h))
        b = 3 * i - (r + g)
    else:
        g = i * (1 - s)
        b = i * (1 + s * math.cos(h - 4 * math.pi / 3) / math.cos(5 * math.pi / 3 - h))
        r = 3 * i - (g + b)
    
    rgb = RGB(r * 255, g * 255, b * 255)
    return rgb
def gamma(x):
    return math.pow((x + 0.055) / 1.055, 2.4) if x > 0.04045 else x / 12.92
def RGBtoXYZ(rgb):
    RR = gamma(rgb.R / 255.0)
    GG = gamma(rgb.G / 255.0)
    BB = gamma(rgb.B / 255.0)
    xyz = XYZ()
    xyz.X = 0.4124564 * RR + 0.3575761 * GG + 0.1804375 * BB
    xyz.Y = 0.2126729 * RR + 0.7151522 * GG + 0.0721750 * BB
    xyz.Z = 0.0193339 * RR + 0.1191920 * GG + 0.9503041 * BB
    return xyz

def XYZtoLAB(xyz):
    x = xyz.X / 95.047
    y = xyz.Y / 100.000
    z = xyz.Z / 108.883

    x = x ** (1 / 3) if x > 0.008856 else (903.3 * x + 16) / 116
    y = y ** (1 / 3) if y > 0.008856 else (903.3 * y + 16) / 116
    z = z ** (1 / 3) if z > 0.008856 else (903.3 * z + 16) / 116

    lab = LAB()
    lab.L = 116 * y - 16
    lab.A = 500 * (x - y)
    lab.B = 200 * (y - z)
    lab.A*=5
    return lab

def LABtoXYZ(lab):
    y = (lab.L + 16) / 116
    x = lab.A / 500 + y
    z = y - lab.B / 200

    x = x ** 3 if x ** 3 > 0.008856 else (x - 16 / 116) / 7.787
    y = y ** 3 if y ** 3 > 0.008856 else (y - 16 / 116) / 7.787
    z = z ** 3 if z ** 3 > 0.008856 else (z - 16 / 116) / 7.787

    xyz = XYZ()
    xyz.X = 95.047 * x
    xyz.Y = 100.000 * y
    xyz.Z = 108.883 * z
    return xyz

def XYZtoRGB(xyz):
    x = xyz.X 
    y = xyz.Y 
    z = xyz.Z 

    r = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z
    g = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z
    b = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z

    r = 1.055 * (r ** (1 / 2.4)) - 0.055 if r > 0.0031308 else 12.92 * r
    g = 1.055 * (g ** (1 / 2.4)) - 0.055 if g > 0.0031308 else 12.92 * g
    b = 1.055 * (b ** (1 / 2.4)) - 0.055 if b > 0.0031308 else 12.92 * b

    rgb = RGB(int(r * 255), int(g * 255), int(b * 255))
    return rgb

def image_process(image):
    # Convert image to RGB mode
    image = image.convert("RGB")

    # Get pixel data
    pixels = image.load()

    
    #Create an empty image for RGB enhance
    rgb_output_image = Image.new("RGB", image.size)
    rgb_output_pixels = rgb_output_image.load()
    
    # Create an empty image for HSI enhance
    hsi_output_image = Image.new("RGB", image.size)
    hsi_output_pixels = hsi_output_image.load()

    # Create an empty image for LAB enhance
    lab_output_image = Image.new("RGB", image.size)
    lab_output_pixels = lab_output_image.load()

    # Iterate over each pixel
    for i in range(image.width):
        for j in range(image.height):
            # Get RGB values of the pixel
            r, g, b = pixels[i, j]
            
            # Create RGB object
            rgb = RGB(r, g, b)
            
            # Convert RGB to HSI
            hsi = RGBtoHSI(rgb)
            
            # Convert HSI to RGB
            new_rgb_hsi = HSItoRGB(hsi)
            
            # Convert RGB to LAB
            xyz = RGBtoXYZ(rgb)
            lab = XYZtoLAB(xyz)
            
            # Convert LAB to RGB
            new_rgb_lab = XYZtoRGB(LABtoXYZ(lab))
            
            # Update pixel with new RGB values in the rgb output image
            
            rgb_output_pixels[i, j] = 2*r,g,b
            
            # Update pixel with new RGB values in the HSI output image
            hsi_output_pixels[i, j] = (int(new_rgb_hsi.R), int(new_rgb_hsi.G), int(new_rgb_hsi.B))
            
            # Update pixel with new RGB values in the LAB output image
            lab_output_pixels[i, j] = (int(new_rgb_lab.R), int(new_rgb_lab.G), int(new_rgb_lab.B))

    # Display the results
    rgb_output_image.show()
    hsi_output_image.show()
    lab_output_image.show()

# Load image
image = Image.open("aloe.jpg")
image_process(image)
image = Image.open("church.jpg")
image_process(image)
image = Image.open("house.jpg")
image_process(image)
image = Image.open("kitchen.jpg")
image_process(image)