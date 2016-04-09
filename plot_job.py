import numpy as np
import cv2

filename = "img/lenna.png"
initial = cv2.imread(filename)
image = cv2.cvtColor(initial, cv2.COLOR_BGR2GRAY)
# cv2.imshow('color_image', image)
# cv2.imshow('gray_image', im)

image_width = image.shape[1]
image_height = image.shape[0]

# TODO: Get these values from the plotter
plot_width = 26
plot_height = 26
width_scale = float(plot_width) / image_width
height_scale = float(plot_height) / image_height
if image_width > plot_width:
    r = min(width_scale, height_scale)
    dim = (int(image_width * r), int(image_height * r))
    # perform the actual resizing of the image and show it
    im = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

# cv2.imshow("resized", resized)
# cv2.waitKey(0)

n = 5    # Number of levels of quantization
indices = np.arange(0,256)   # List of all colors
divider = np.linspace(0,255,n+1)[1] # we get a divider
quantiz = np.int0(np.linspace(0,255,n)) # we get quantization colors
color_levels = np.clip(np.int0(indices/divider),0,n-1) # color levels 0,1,2..
palette = quantiz[color_levels] # Creating the palette
im2 = palette[im]  # Applying palette on image
im2 = cv2.convertScaleAbs(im2) # Converting image back to uint8
cv2.imshow('im2', im2)
cv2.imwrite("img/resized" + filename, im2)

cv2.waitKey(0)
cv2.destroyAllWindows()
