import time
import math
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class MQ4():
    RL_VALUE = 20  # load resistance in kilo ohms (adjust based on your configuration)
    RO_CLEAN_AIR_FACTOR = 4.4  # Sensor resistance in clean air divided by RO
    CALIBRATION_SAMPLE_TIMES = 50
    CALIBRATION_SAMPLE_INTERVAL = 50  # in milliseconds
    READ_SAMPLE_INTERVAL = 50  # in milliseconds
    READ_SAMPLE_TIMES = 5
    METHANE_CURVE = [2.3, 0.29, -0.47]  # Example curve, adjust based on actual data

    def __init__(self, Ro=20, channel=ADS.P1):
        self.Ro = Ro
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c, address=0x49)
        self.chan = AnalogIn(ads, channel)

        print("Calibrating MQ-4 on ADS1115 at address 0x49...")
        self.Ro = self.MQ_Calibration()
        print("Calibration of MQ-4 is done...")
        print("MQ-4 Ro=%f kohm" % self.Ro)
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
        val["METHANE"] = self.MQ_GetGasPercentage(read / self.Ro, self.METHANE_CURVE)
        val["RAW_VALUE"] = raw_value
        return val

    def MQ_GetGasPercentage(self, rs_ro_ratio, pcurve):
        return math.pow(10, (((math.log(rs_ro_ratio) - pcurve[1]) / pcurve[2]) + pcurve[0]))

# Example of using the MQ4 class
sensor = MQ4()
print(sensor.MQ_Percentage())
