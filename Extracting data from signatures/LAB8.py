from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def numberOfTransitions(array):
    n=0
    prev = array[0][0]
    for x in range(array.shape[0]-1):
        for y in range(array.shape[1]-1):
            curr = array[x][y]
            if (curr == 255 ):
                if(prev == 0):
                    n = n + 1            
            prev = curr
    return n

#READING AN IMAGE AND PREPROCESSING

image = cv2.imread("image.jpg")
print("Shape of image read =",image.shape)

greyScaleArray = np.dot(image,[0.07,0.72,0.21])
print("Shape of greyscale image = ",greyScaleArray.shape)

greyScaleArray[greyScaleArray > 127] = 255
greyScaleArray[greyScaleArray <= 127] = 0

image=Image.fromarray(greyScaleArray)
image.show()

cv2.imwrite("PREPROCESSED.jpg",greyScaleArray)

print("Shape of FINAL PREPROCESSED image  =",greyScaleArray.shape)

#MAKING BOUNDING BOX

rows = int(greyScaleArray.shape[0])
columns = int(greyScaleArray.shape[1])


min_row = 1000000000000000;
max_row = 0;
min_column = 100000000000000;
max_column = 0;

for x in range(rows-1):
    for y in range(columns-1):
        
        pixel = greyScaleArray[x][y]

        if(pixel == 0):

            if(x<min_row):
                min_row=x
            if(x>max_row):
                max_row=x;
            if(y<min_column):
                min_column=y
            if(y>max_column):
                max_column=y


#print(min_row,max_row, min_column,max_column)

crop_img = greyScaleArray[min_row:max_row, min_column:max_column]
image=Image.fromarray(crop_img)
image.show()

print("Dimensions of CROPPED IMAGE = ",crop_img.shape)

cv2.imwrite("PREPROCESSED_AND_CROPPED.jpg",crop_img)

#FINDING CENTROID

cx = 0
cy = 0
n = 0

rows = int(crop_img.shape[0])
columns = int(crop_img.shape[1])

print(rows,columns)

for x in range(rows-1):
    for y in range(columns-1):

        pixel = crop_img[x][y]

        if(pixel == 0):
            cx = cx + x
            cy = cy + y
            n = n + 1
	
cx = cx / n
cy = cy / n


cx=int(cx)
cy=int(cy)

print("Centroid = ",cx,cy)

#PLOTTING


part1 = crop_img[0:cx,0:cy]
imagePart1=Image.fromarray(part1)
imagePart1.show()

part2 = crop_img[0:cx,cy:columns-1]
imagePart2=Image.fromarray(part2)
imagePart2.show()

part3 = crop_img[cx:rows-1,0:cy]
imagePart3=Image.fromarray(part3)
imagePart3.show()

part4 = crop_img[cx:rows-1,cy:columns-1]
imagePart4=Image.fromarray(part4)
imagePart4.show()

TL = numberOfTransitions(part1)
TR = numberOfTransitions(part2)
BL = numberOfTransitions(part3)
BR = numberOfTransitions(part4)

print("VALUES OF TL TR BL BR",TL,TR,BL,BR)



'''
# Create figure and axes
fig,ax = plt.subplots(1)
# Display the image
plt.imshow(crop_img, cmap='Greys_r')

# Create a Rectangle patch
rect1 = patches.Rectangle((0,0),cy,cx,linewidth=1,edgecolor='r',facecolor='none')
rect2 = patches.Rectangle((cy,cx),(columns-1-cy),(-cx),linewidth=1,edgecolor='y',facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect1)
ax.add_patch(rect2)
ax.patch.set_facecolor('white')

plt.show()
'''
