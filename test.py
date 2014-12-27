from spimaster import SPIMaster
from lib23s17 import MCP23S17


mcpdrive = MCP23S17(8, 10, 9, 11)

def configurar():
    mcpdrive.write_data(0x00, mcpdrive.iodira)
    mcpdrive.write_data(0x01, mcpdrive.iodirb)

def escrever(dado):
    mcpdrive.write_data(dado, mcpdrive.gpioa)

def ler():
    return mcpdrive.read_data(mcpdrive.gpiob)

configurar()
escrever(255)

print(ler())

print("fim")
