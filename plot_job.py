import cv2
import numpy as np


class PlotJob:

    def __init__(self, plot_width, plot_height, shades, filename):
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.shades = shades
        self.lines = []

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
            image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        n = self.shades    # Number of levels of quantization
        indices = np.arange(0, 256)   # List of all colors
        divider = np.linspace(0, 255, n + 1)[1]  # we get a divider
        quantiz = np.int0(np.linspace(0, 255, n))  # we get quantization colors
        color_levels = np.clip(np.int0(indices / divider), 0, n - 1)  # color levels 0,1,2..
        palette = quantiz[color_levels]  # Creating the palette
        im2 = palette[image]   # Applying palette on image
        im2 = cv2.convertScaleAbs(im2)  # Converting image back to uint8

        cv2.imshow("im", im2)
        cv2.waitKey(0)

        shade_values = np.unique(im2)  # get sorted shade values
        # print shade_values
        # replace the shade vlaues with the shade index
        for i in range(self.shades):
            im2[im2 == shade_values[i]] = self.shades - (i + 1)

        # print im2
        # im2.fill(255)
        return im2
        # cv2.imshow('im2', im2)
        # cv2.imwrite("img/resized" + filename, im2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def __get_sequences(self, val, arr):
        sequences = []
        start = count = 0
        for i in range(len(arr)):
            if arr[i] >= val:
                if count == 0:
                    start = i
                count += 1
            else:
                if count != 0:
                    sequences.append((start, count))
                count = 0

        if arr[-1] >= val:
            sequences.append((start, count))

        return sequences

    def __generate_lines(self, img):
        width = img.shape[1]
        height = img.shape[0]

        # horizontal lines (shade 1)
        h_lines = []
        for row in range(height):
            seq = self.__get_sequences(1, img[row])

            if row % 2 == 0:
                row_lines = [(i[0], row, i[0] + i[1], row) for i in seq]
            else:
                row_lines = [(i[0] + i[1], row, i[0], row) for i in seq[::-1]]

            h_lines.extend(row_lines)
        self.lines.extend(h_lines)

        # vertical lines (shade 2)
        v_lines = []
        for col in range(width):
            seq = self.__get_sequences(2, img[:, col])

            if col % 2 == 0:
                col_lines = [(col, i[0], col, i[0] + i[1]) for i in seq]
            else:
                col_lines = [(col, i[0] + i[1], col, i[0]) for i in seq[::-1]]

            v_lines.extend(col_lines)
        self.lines.extend(v_lines)
