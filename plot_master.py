import serial
import time
import sys

ser = serial.Serial()
try:
    ser.port = "/dev/tty.usbmodem1451"
    ser.baudrate = 9600
    ser.parity = serial.PARITY_NONE
    ser.bytesize = serial.EIGHTBITS
    ser.open()
    if not ser.is_open:
        sys.exit("Could not open serial connection")


    print "waiting for device to initialise..."
    time.sleep(5)

    ser.write("help\n")
    print "listening... "
    while True:
        ser.write("line 0 0 10 10\n")
        time.sleep(5);
        ser.write("line 10 10 0 0\n")
        time.sleep(5)

        # line = ser.readline()
        # while line != "":
        #     print line,
        #     line = ser.readline()
except KeyboardInterrupt:
    print "Error: KeyboardInterrupt"
except serial.SerialException:
    print "Error: SerialException"
finally:
    if ser.is_open:
        ser.close()
        print "connection closed"
