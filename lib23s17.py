import RPi.GPIO as GPIO
from threading import Thread, Lock
from time import sleep
from spimaster import SPIMaster

class MCP23S17(SPIMaster):
    def __init__(self, chipselect, mosi, miso, clock, address=0x00):
        super(MCP23S17, self).__init__(chipselect, mosi, miso, clock)
        self.address = 0x40 | address
        self.iodira = 0x00
        self.iodirb = 0x10

        self.IOCONA = 0x0A
        self.IOCONB = 0x0B

        GPIO.output(self.chip_select, GPIO.HIGH)
        GPIO.output(self.clock, GPIO.LOW)

        #Separa o enderecamento dos registradores para cada porta
        self.write_data(0x80, self.IOCONA)
        self.write_data(0x80, self.IOCONB)

    def write_data(self, data, register):
        GPIO.output(self.chip_select, GPIO.LOW)
        #Envia o endereco e a operacao
        super(MCP23S17, self).write_to_bus(self.address | self.spi_write_operation)

        #Envia o registrador a ser escrito
        super(MCP23S17, self).write_to_bus(register)

        #Envia o dado a ser escrito no registrador
        super(MCP23S17, self).write_to_bus(data)
        GPIO.output(self.chip_select, GPIO.HIGH)

    def read_data(self, register):
        GPIO.output(self.chip_select, GPIO.LOW)

        super(MCP23S17, self).write_to_bus(self.address | self.spi_read_operation)

        super(MCP23S17, self).write_to_bus(register)

        data = super(MCP23S17, self).read_from_bus()

        GPIO.output(self.chip_select, GPIO.HIGH)

        return data

    def get_port_a(self):
        return Port(self.iodira, self)

    def get_port_b(self):
        return Port(self.iodirb, self)


class Port():
    def __init__(self, port_address, mcpdrive):
        self.port_address = port_address
        self.drive = mcpdrive

        self.IODIR = port_address
        self.IPOL = port_address + 1
        self.GPINTEN = port_address + 2
        self.DEFVAL = port_address + 3
        self.INTCON = port_address + 4
        self.GPPU = port_address + 6
        self.INTF = port_address + 7
        self.INTCAP = port_address + 8
        self.GPIO = port_address + 9
        self.OLAT = port_address + 10
        self.port_value = 0;

    def set_out(self):
        self.drive.write_data(0, self.IODIR)

    def invert_polarity(self):
        current_polarity = self.drive.read_data(self.IPOL)
        self.drive.write_data(255^current_polarity, self.IPOL)

    def set_int(self, value):
        self.drive.write_data(255, self.GPINTEN)
        self.drive.write_data(value, self.DEFVAL)
        self.drive.write_data(255, self.INTCON)

    def set_input(self, pull_up = True):
        self.drive.write_data(255, self.IODIR)
        if (pull_up):
            self.drive.write_data(255, self.GPPU)
        else:
            self.drive.write_data(0, self.GPPU)

    def read(self):
        return self.drive.read_data(self.GPIO)

    def read_async(self, mutex):
        with mutex:
            self.port_value = self.drive.read_data(self.GPIO)

    def write(self, data):
        self.drive.write_data(data, self.GPIO)

    def write_async(self, data, mutex):
        with mutex:
            self.drive.write_data(data, self.GPIO)
