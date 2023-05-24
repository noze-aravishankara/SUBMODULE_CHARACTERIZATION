import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_bmp180 import adafruit_bmp180 as bmp
import adafruit_sht31d
from time import sleep

'''
This code is for the submodule characterization system. This will output the data in a format that can easily be copied to csv. Will update later.
'''

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
        self.humidity = adafruit_sht31d.SHT31D(self.i2c0)

        self.ADS = ADS.ADS1115(self.i2c1)
        self.PID = AnalogIn(self.ADS, ADS.P0)
        
        self.counter = 0

    def get_pid_value(self):
        return self.PID.value

    def get_pressure_value(self):
        return self.pressure.pressure
      
    def get_temp_from_pressure(self):
        return self.pressure.temperature
    
    def get_humidity_value(self):
        return self.humidity.relative_humidity
    
    def get_temp_from_humidity(self):
        return self.humidity.temperature
    
    def loop_measurement(self):
        while True:
            print(f'Humidity Sensor - Humidity: {self.get_humidity_value()}% \t Temperature: {self.get_temp_from_humidity()} C\n Pressure Sensor - Pressure: {self.get_pressure_value()}hPa \t Temperature: {self.get_temp_from_pressure()} C \n VOC: {self.get_pid_value()} voltage')
            sleep(1)

    def loop_array(self):
        print('Counter,Humidity,Temperature_H,Pressure,Temperature_P,VOC')
        while True:
            print(f'{self.counter}{self.get_humidity_value()},{self.get_temp_from_humidity()},{self.get_pressure_value()},{self.get_temp_from_pressure()},{self.get_pid_value()}')
            self.counter = self.counter + 1
            sleep(1)


if __name__ == "__main__":
    A = READER()
    A.loop_array()
