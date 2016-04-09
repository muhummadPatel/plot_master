import numpy as np
import cv2

class PlotJob:

    def __init__(self, plot_width, plot_height, shades, filename):
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.shades = shades

        original_img = self.__load_image(filename)
        prepared_img = self.__prepare_image(original_img)
        self.__lines = self.__generate_lines(prepared_img)

    def __load_image(self, filename):
        return cv2.imread(filename)

    def __prepare_image(self, img):
        # convert to grayscale
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # resize to fit plottable area
        image_width = image.shape[1]
        image_height = image.shape[0]
        width_scale = float(self.plot_width) / image_width
        height_scale = float(self.plot_height) / image_height
        if image_width > self.plot_width:
            r = min(width_scale, height_scale)
            dim = (int(image_width * r), int(image_height * r))
            # perform the actual resizing of the image and show it
            image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        n = self.shades    # Number of levels of quantization
        indices = np.arange(0, 256)   # List of all colors
        divider = np.linspace(0, 255, n + 1)[1] # we get a divider
        quantiz = np.int0(np.linspace(0, 255, n)) # we get quantization colors
        color_levels = np.clip(np.int0(indices / divider), 0, n - 1) # color levels 0,1,2..
        palette = quantiz[color_levels] # Creating the palette
        im2 = palette[image]  # Applying palette on image
        im2 = cv2.convertScaleAbs(im2) # Converting image back to uint8

        shade_values = np.unique(im2) # get sorted shade values
        # print shade_values
        # replace the shade vlaues with the shade index
        for i in range(self.shades):
            im2[im2==shade_values[i]] = i

        # im2.fill(255)
        return im2
        # cv2.imshow('im2', im2)
        # cv2.imwrite("img/resized" + filename, im2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def __get_sequences(self, val, arr):
    	lines = []
    	count = 0
    	start = 0
    	for i in range(len(arr)):
    		if arr[i] >= val:
    			if count == 0:
    				start = i
    			count += 1
    		else:
    			if count != 0:
    				lines.append((start, count))
    			count = 0

        if arr[-1] >= val:
        	lines.append((start, count))

    	return lines

    def __generate_lines(self, img):
        print img[0]

        width = img.shape[1]
        height = img.shape[0]

        # horizontal lines (shade 1)
        h_lines = []
        for row in range(height):
            seq = self.__get_sequences(1, img[row]) # TODO: change 2 to 1
            h_lines.extend( [(row, i[0], row, i[0] + i[1]) for i in seq] )

        print seq
        print h_lines



pj = PlotJob(52, 52, 5, "img/lenna.png")
