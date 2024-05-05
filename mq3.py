import time
import math
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class MQ3():
    RL_VALUE = 10  # load resistance in kilo ohms
    RO_CLEAN_AIR_FACTOR = 60  # Sensor resistance in clean air divided by RO
    CALIBRATION_SAMPLE_TIMES = 50
    CALIBRATION_SAMPLE_INTERVAL = 50  # in milliseconds
    READ_SAMPLE_INTERVAL = 50  # in milliseconds
    READ_SAMPLE_TIMES = 5
    ALCOHOL_CURVE = [0.477, 0.209, -0.680]

    def __init__(self, Ro=10, channel=ADS.P0):
        self.Ro = Ro
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c, address=0x48)
        self.chan = AnalogIn(ads, channel)

        print("Calibrating MQ-3 on ADS1115 at address 0x48...")
        self.Ro = self.MQ_Calibration()
        print("Calibration of MQ-3 is done...")
        print("MQ-3 Ro=%f kohm" % self.Ro)
        print("\n")
    
    def MQ_Calibration(self):
        val = 0.0
        for i in range(self.CALIBRATION_SAMPLE_TIMES):
            val += self.MQ_ResistanceCalculation(self.chan.value)
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL / 1000.0)
        val = val / self.CALIBRATION_SAMPLE_TIMES
        val = val / self.RO_CLEAN_AIR_FACTOR
        return val
    
    def MQ_ResistanceCalculation(self, raw_adc):
        if raw_adc == 0:
            raw_adc = 1
        return float(self.RL_VALUE * (32767.0 - raw_adc) / float(raw_adc))
    
    def MQ_Read(self):
        rs = 0.0
        raw_value = 0.0
        for i in range(self.READ_SAMPLE_TIMES):
            raw_value += self.chan.value
            rs += self.MQ_ResistanceCalculation(self.chan.value)
            time.sleep(self.READ_SAMPLE_INTERVAL / 1000.0)
        rs = rs / self.READ_SAMPLE_TIMES
        raw_value = raw_value / self.READ_SAMPLE_TIMES
        return rs, raw_value

    def MQ_Percentage(self):
        val = {}
        read, raw_value = self.MQ_Read()
        val["ALCOHOL"] = self.MQ_GetGasPercentage(read/self.Ro, self.ALCOHOL_CURVE)
        val["RAW_VALUE"] = raw_value
        return val

    def MQ_GetGasPercentage(self, rs_ro_ratio, pcurve):
        return math.pow(10, (((math.log(rs_ro_ratio) - pcurve[1]) / pcurve[2]) + pcurve[0]))

# Example of using the MQ3 class
sensor = MQ3()
print(sensor.MQ_Percentage())
