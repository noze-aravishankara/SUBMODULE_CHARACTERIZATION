import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_bmp180 import adafruit_bmp180 as bmp
import adafruit_sht31d


class READER:
    def __init__(self):
        '''
        SCL/SDA 0 - HUMIDITY/TEMPERATURE PROBE
        SCL/SDA 1 - PID
        SCL/SDA 2 - PRESSURE SENSOR (BMP180)
        '''
        
        self.i2c0 = busio.I2C(board.SCL, board.SDA)
        self.i2c1 = busio.I2C(board.SCL1, board.SDA1)
        self.i2c2 = busio.I2C(board.SCL2, board.SDA2)

        pressure_address = 0x77
        self.pressure = bmp.Adafruit_BMP180_I2C(self.i2c2)

        humidity_address = 0x44
        #self.humidity = I2CDevice(self.i2c0, humidity_address)

        self.humidity = adafruit_sht31d.SHT31D(self.i2c0)

        self.ADS = ADS.ADS1115(self.i2c1)
        self.PID = AnalogIn(self.ADS, ADS.P0)

    def get_pid_value(self):
        return self.PID.value

    def get_pressure_value(self):
        self.pressure.pressure

    def convert_to_int(self, data):
        return int.from_bytes(data, 'big')
    
    def get_humidity_value(self):
        return self.humidity.relative_humidity


if __name__ == "__main__":
    A = READER()

    print(f'VOC: {A.get_pid_value()}')
    print(f'Pressure: {A.get_pressure_value()}')
    print(f'Humidity: {A.get_humidity_value()}')
