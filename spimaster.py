import RPi.GPIO as GPIO

class SPIMaster(object):
    def __init__(self, chipselect, mosi, miso, clock):
        self.chip_select = chipselect
        self.mosi = mosi
        self.miso = miso
        self.clock = clock
        self.spi_write_operation = 0x00
        self.spi_read_operation = 0x01

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.clock, GPIO.OUT)
        GPIO.setup(self.miso, GPIO.IN)
        GPIO.setup(self.mosi, GPIO.OUT)
        GPIO.setup(self.chip_select, GPIO.OUT)

    def write_to_bus(self, data):
        for i in range(8):
            if (data & 0x80):
                GPIO.output(self.mosi, GPIO.HIGH)
            else:
                GPIO.output(self.mosi, GPIO.LOW)

            GPIO.output(self.clock, GPIO.HIGH)
            GPIO.output(self.clock, GPIO.LOW)
            data <<= 1

    def read_from_bus(self):
        data = 0
        for i in range(8):
            data <<= 1;
            if (GPIO.input(self.miso)):
                data |= 0x01;

            GPIO.output(self.clock, GPIO.HIGH)
            GPIO.output(self.clock, GPIO.LOW)
        return data


