import glob
from skimage.io import imread, imsave, imshow, show
from skimage.metrics import mean_squared_error
import numpy as np

# files variables containing lists of pictures
dirlist = glob.glob("mnist-subset/*")
testlist = glob.glob("test_images/*")
fliplist = glob.glob('images_flip/*')


# flips an image of each type and displays
def images_flip():
    for folder in fliplist:  # loops for each folder
        index = 0
        file = glob.glob(f'{folder}/*.png')  # Loading the files
        for fname in file:    # loops for each file in folder
            index = index + 1
            im = imread(fname)  # Reading the file
            im_flipped = np.flip(im)  # Flipping the image
            imshow(im_flipped)
            show()  # Displaying the file
            imsave(f'{folder}flip.png', im_flipped)  # save the file to specified folder


# making the composite images for base case, then moved to base_images folder
def composite_image():
    n = 0
    print("Starting...")
    for dir in dirlist:  # loops for each folder
        f1 = glob.glob(f'{dir}/*.png')  # loading the files
        print("Dir, Nfiles: ", dir, len(f1))
        im = np.zeros((28, 28), dtype=np.float64)  # creating an array of zeros
        for fname in f1:  # looping for each file in dir
            im = im + imread(fname)  # reading the file
        # computing the summation of images
        im = im / im.max()
        im = im * 255
        im = im.astype(np.uint8)
        imsave(f'base_images/{n}.png', im)  # Saving the image into base-images directory
        n = n + 1  # Incrementing the directory
    print("Finished!")


# This function was used in order to get a general performance of each number in order to establish a threshold
def image_learning(number):
    maximum = 0.0
    sum = 0.0

    base = imread(f'base_images/{number}.png')  # choosing base image to compare against
    # Making base image a binary image
    base[base > 90] = 255
    base[base != 255] = 0
    base[base == 255] = 1

    for folder in dirlist:  # loops for each folder
        index = 0
        file = glob.glob(f'{folder}/*.png')  # loading the file list
        for fname in file:   # loops for each file in the folder
            index = index + 1
            im = imread(fname)  # Reading the file into "im"
            #  Making im a binary image
            im[im > 90] = 255
            im[im != 255] = 0
            im[im == 255] = 1
            image_mse = mean_squared_error(base, im)  # computing the MSE
            sum = sum + image_mse  # Summation of MSE
            # Finding the max
            if maximum < image_mse:
                maximum = image_mse
            # If reached the final index compute the results and reset values
            elif index == 80:
                print('========================================')
                print(f'Base image: {number}.png')
                print(f'Compared to: {folder}')
                print(f'Maximum: {maximum}')
                print(f'Sum: {sum}')
                print(f'Average: {sum / 80}')
                maximum = 0.0
                sum = 0.0


# Test each base image against test images from 0-9 with 20 images for each number. Then prints the pass and fail
# metrics
def image_tester(number):
    passed = 0
    failed = 0

    base = imread(f'base_images/{number}.png')  # choosing base image to compare against
    # Making base image a binary image
    base[base > 90] = 255
    base[base != 255] = 0
    base[base == 255] = 1

    for folder in testlist:  # loops for each folder
        index = 0
        file = glob.glob(f'{folder}/*.png')  # Loading the files
        for fname in file:  # loops for each file in the folder
            index = index + 1
            im = imread(fname)  # Reading each file into im
            # Making im a binary image
            im[im > 90] = 255
            im[im != 255] = 0
            im[im == 255] = 1
            image_mse = mean_squared_error(base, im)  # computing the MSE
            #  if smaller than 0.13 then increment passed
            if image_mse < 0.13:
                passed = passed + 1
            #  if larger than 0.13 then increment failed
            elif image_mse >= 0.13:
                failed = failed + 1
        # Print and reset pass and fail rates
        print('========================================')
        print(f'Base image: {number}.png')
        print(f'Compared to: {folder}')
        print(f'passed: {passed}')
        print(f'failed: {failed}')
        passed = 0
        failed = 0


# Running the functions -------------------------
# images_flip()
# composite_image()
# image_tester(0)
