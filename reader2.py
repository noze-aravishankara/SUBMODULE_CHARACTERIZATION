import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_bmp.BMP180 as BMP180

class READER:
    def __init__(self):
        self.i2c0 = busio.I2C(board.SCL, board.SDA)
        self.i2c1 = busio.I2C(board.SCL1, board.SDA1)
        self.i2c2 = busio.I2C(board.SCL2, board.SDA2)

        # pressure_address = 0x44
        # self.pressure = I2CDevice(self.i2c0, pressure_address)
        bmp180 = BMP180.BMP180(self.I2C)
        bmp180.oversample_sett = 2 



        humidity_address = 0x77
        self.humidity = I2CDevice(self.i2c2, humidity_address)

        self.ADS = ADS.ADS1115(self.i2c1)
        self.PID = AnalogIn(self.ADS, ADS.P0)

    def get_pid_value(self):
        return self.PID.value

    def get_pressure_value(self):
        while True:
            # Read temperature in degrees Celsius
            temperature = bmp180.temperature

            # Read pressure in Pascals
            pressure = bmp180.pressure

            # Print the values
            print("Temperature: {:.2f} °C".format(temperature))
            print("Pressure: {:.2f} Pa".format(pressure))

            # Wait for a second before reading again
            time.sleep(1.0)
        # while not self.i2c0.try_lock():
        #     pass

        # try:
        #     data_size = 4
        #     buffer = bytearray(data_size)
        #     self.pressure.readinto(buffer)
    
        # finally:
        #     self.i2c0.unlock()

        return self.convert_to_int(buffer)

    def convert_to_int(self, data):
        return int.from_bytes(data, 'big')
    
    def get_humidity_value(self):
        while not self.i2c2.try_lock():
            pass
        try:
            data_size = 4
            buffer = bytearray(data_size)
            self.humidity.readinto(buffer)

            
        finally:
            self.i2c2.unlock()

        return self.convert_to_int(buffer)


if __name__ == "__main__":
    A = READER()

    print(f'VOC: {A.get_pid_value()}')
    print(f'Pressure: {A.get_pressure_value()}')
    print(f'Humidity: {A.get_humidity_value()}')
