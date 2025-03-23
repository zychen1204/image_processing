from PIL import Image
import numpy as np

def sobel(image):
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    height, width = image.shape
    
    new_image = np.zeros((height, width))
    padded_image = np.pad(image, pad_width=1, mode='constant', constant_values=0)
    
    for i in range(height):
        for j in range(width):
            x_start = i
            x_end = i + 3
            y_start = j
            y_end = j + 3
            
            image_block = padded_image[x_start:x_end, y_start:y_end]
            
            gradient_x = np.sum(np.multiply(image_block, sobel_x))
            gradient_y = np.sum(np.multiply(image_block, sobel_y))
            
            gradient = np.sqrt(gradient_x**2 + gradient_y**2)
            
            new_image[i, j] = gradient
    new_image *=255.0/new_image.max()
    
    return new_image

#imput image,convert to gray and convert to array
image1 = Image.open('baboon.png').convert('L')
gray_image1 = np.array(image1)
image2 = Image.open('peppers.png').convert('L')
gray_image2 = np.array(image2)
image3 = Image.open('pool.png').convert('L')
gray_image3 = np.array(image3)

#using sobal operation
sobel_image1 = sobel(gray_image1)
sobel_image2 = sobel(gray_image2)
sobel_image3 = sobel(gray_image3)

#array to image
sobel_image1 = Image.fromarray(sobel_image1)
sobel_image2 = Image.fromarray(sobel_image2)
sobel_image3 = Image.fromarray(sobel_image3)

# Display images
sobel_image1.show()
sobel_image2.show()
sobel_image3.show()