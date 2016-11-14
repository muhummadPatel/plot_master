import cv2
import numpy as np
import serial
import sys
import time

from plot_job import PlotJob

# TODO: show the user the list of available ports (using pyserial) and let them
# choose which to connect to


def plot_preview(lines):
    cell_width = 5
    line_colour = (255, 0, 0)
    line_thickness = 1

    # TODO: Don't hardcode the plot dimensions (130x130).
    img = np.full((130 * cell_width, 130 * cell_width, 3), 255, dtype=np.uint8)

    for line in lines:
        start = (line[0] * cell_width, line[1] * cell_width)
        end = (line[2] * cell_width, line[3] * cell_width)

        cv2.line(img, start, end, line_colour, line_thickness)

    cv2.imshow('Preview', img)


def plot(lines):
    ser = serial.Serial()
    try:
        ser.port = "/dev/tty.usbmodem1451"
        ser.baudrate = 9600
        ser.parity = serial.PARITY_NONE
        ser.bytesize = serial.EIGHTBITS
        ser.timeout = 10
        ser.open()
        if not ser.is_open:
            sys.exit("Could not open serial connection")

        print "waiting for device to initialise..."
        time.sleep(5)

        print "listening... "
        for line in lines:
            code = "line " + " ".join([str(i) for i in line]) + "\n"
            ser.write(code)
            print code,

            response = ser.readline()
            retries = 1
            # print "X> " + response
            while response.find("x") < 0:
                response = ser.readline()
                retries += 1

                if retries > 6:
                    print "no response, assume ok\n",
                    break
                # print "X> " + response
        ser.write("origin\n")
        print "DONE. Finishing up..."
        time.sleep(10)
    except KeyboardInterrupt:
        print "Error: KeyboardInterrupt"
    except serial.SerialException:
        print "Error: SerialException"
    finally:
        if ser.is_open:
            print "closing connection..."
            ser.close()
            print "connection closed"


def main():
    job = PlotJob(130, 130, 5, "img/me.jpg")
    plot_preview(job.lines)
    cv2.waitKey(0)

    plot(job.lines)

if __name__ == '__main__':
    main()
