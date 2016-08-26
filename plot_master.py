import serial
import time
import sys
from plot_job import PlotJob

# TODO: show the user the list of available ports (using pyserial) and let them
# choose which to connect to


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
    job = PlotJob(130, 130, 3, "img/me.jpg")
    plot(job.lines)

if __name__ == '__main__':
    main()
