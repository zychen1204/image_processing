from PIL import Image
import matplotlib.pyplot as plt


def process(image1):
        # show original image
    hist_eq_image1 = image1.histogram()
    cdf = [sum(hist_eq_image1[:i+1]) for i in range(len(hist_eq_image1))]
    fig, axs = plt.subplots(3, 3, figsize=(10, 10))
    axs[0,0].imshow(image1,cmap='gray')
    axs[0,0].set_title('original image')
    axs[1,0].plot(image1.histogram(), color='blue', label='Image1',alpha=0.5)
    axs[1,0].set_title('original image histogram')
    axs[2,0].plot(cdf, color='blue', label='Image1',alpha=0.5)
    axs[2,0].set_title('original image cdf_line')

    # process global histogram 
    cdf = [round((cdf[i] - cdf[0]) * 255 / (cdf[-1] - cdf[0])) for i in range(len(cdf))]
    hist_eq_image1 = image1.point(lambda x: cdf[x])

    #show global image
    axs[1,1].plot(hist_eq_image1.histogram(), color='blue', label='Image1')
    axs[1,1].set_title('global image histogram',alpha=0.5)
    axs[2,1].plot(cdf, color='blue', label='Image1')
    axs[2,1].set_title('global image cdf_line',alpha=0.5)
    axs[0,1].imshow(hist_eq_image1, cmap='gray')
    axs[0,1].set_title('gobal-processed image')

    plt.tight_layout()

    # Perform local histogram equalization on image1
    
    #define block
    block_size = (image1.size[0] // 4, image1.size[1] // 4)
    
    hist_eq_image1 = Image.new("L", image1.size)
    hist_eq_image1_pixels = hist_eq_image1.load()
    for i in range(0, image1.size[0], block_size[0]):
        for j in range(0, image1.size[1], block_size[1]):
            block = image1.crop((i, j, i + block_size[0], j + block_size[1]))
            block_histogram = block.histogram()
            cumulative_histogram = [sum(block_histogram[:k + 1]) for k in range(256)]
            cdf_min = min(cumulative_histogram)  # Find the minimum value in CDF
            cdf_max = max(cumulative_histogram)  # Find the maximum value in CDF
            for x in range(i, i + block_size[0]):
                for y in range(j, j + block_size[1]):
                    pixel = image1.getpixel((x, y))
                    new_pixel = int(((cumulative_histogram[pixel] - cdf_min) * 255) / (cdf_max - cdf_min))
                    hist_eq_image1_pixels[x, y] = new_pixel
                    
            axs[2,2].plot(cumulative_histogram, color='blue', label='Image1',alpha=0.5)
            axs[2,2].set_title('local image cdf_line')
            axs[1,2].plot(block_histogram, color='blue', label='Image1',alpha=0.5)
            axs[1,2].set_title('local image histogram')
    axs[0,2].imshow(hist_eq_image1, cmap='gray')
    axs[0,2].set_title('local-processed image')
    plt.show()

if __name__ == '__main__':

    #process two image and show that
    process(Image.open('Lena.bmp').convert('L'))
    process(Image.open('Peppers.bmp').convert('L'))


            