import matplotlib.image as img
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def Laplacian(image, laplacian_filter):
    image = np.array(image)
    image_result = np.zeros_like(image)
    for i in range(1, image.shape[0]-1):
        for j in range(1, image.shape[1]-1):
            val = np.sum(laplacian_filter*image[i-1:i+2,j-1:j+2])
            image_result[i,j] = np.clip(val, 0, 255)
    return image_result

def high_boost(image, k=1.0):
    laplacian_filter = np.array([[0, -1, 0], [-1, 4+k, -1], [0, -1, 0]])
    laplacian = Laplacian(image, laplacian_filter)
    sharp = np.clip(image + laplacian, 0, 255).astype(np.uint8)
    return sharp

if __name__ == '__main__':
    fig, axes = plt.subplots (nrows=2,ncols=3)
    
    #read two image file
    blurry_original_img = Image.open('blurry_moon.tif').convert('L')
    skeleton_original_img = Image.open('skeleton_orig.bmp').convert('L')
    #show original image
    axes[0,0].imshow(blurry_original_img,cmap="gray")
    axes[1,0].imshow(skeleton_original_img,cmap="gray")
    axes[0,0].set_title("blurry_original_img")
    axes[1,0].set_title("skeleton_original_img")
    
    #process by Laplacian operator
    
    laplacian_filter = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    blurry_Laplacian_img = Laplacian(blurry_original_img,laplacian_filter)
    skeleton_Laplacian_img = Laplacian(skeleton_original_img,laplacian_filter)
    
    axes[0,1].imshow(blurry_Laplacian_img,cmap="gray")
    axes[1,1].imshow(skeleton_Laplacian_img,cmap="gray")
    axes[0,1].set_title("blurry_Laplacian_img")
    axes[1,1].set_title("skeleton_Laplacian_img")
    
    #process by high-boost filtering
    blurry_high_boost_filtering_img = high_boost(blurry_original_img,2.7)
    skeleton_high_boost_filtering_img = high_boost(skeleton_original_img,2.7)
    
    axes[0,2].imshow(blurry_high_boost_filtering_img,cmap="gray")
    axes[1,2].imshow(skeleton_high_boost_filtering_img,cmap="gray")
    axes[0,2].set_title("blurry_high_boost_filtering_img")
    axes[1,2].set_title("skeleton_high_boost_filtering_img")
    
    fig.tight_layout()
    plt.show()