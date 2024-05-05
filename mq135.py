import time
import math
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class MQ135():
    RL_VALUE = 10  # load resistance in kilo ohms
    RO_CLEAN_AIR_FACTOR = 3.6  # Sensor resistance in clean air divided by RO
    CALIBRATION_SAMPLE_TIMES = 50
    CALIBRATION_SAMPLE_INTERVAL = 50  # in milliseconds
    READ_SAMPLE_INTERVAL = 50  # in milliseconds
    READ_SAMPLE_TIMES = 5

    def __init__(self, Ro=10, channel=ADS.P0):
        self.Ro = Ro
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c, address=0x49)
        self.chan = AnalogIn(ads, channel)

        print("Calibrating MQ-135 on ADS1115 at address 0x49...")
        self.Ro = self.MQ135_Calibration()
        print("Calibration of MQ-135 is done...")
        print("MQ-135 Ro=%f kohm" % self.Ro)
        print("\n")

    def MQ135_Calibration(self):
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
        # Here you would need to add the logic to calculate percentage based on curves for each gas
        # For example:
        val["ACETON"] = self.MQ_GetGasPercentage(read / self.Ro, 0)
        val["TOLUENO"] = self.MQ_GetGasPercentage(read / self.Ro, 1)
        val["ALCOHOL"] = self.MQ_GetGasPercentage(read / self.Ro, 2)
        val["CO2"] = self.MQ_GetGasPercentage(read / self.Ro, 3)
        val["NH4"] = self.MQ_GetGasPercentage(read / self.Ro, 4)
        val["CO"] = self.MQ_GetGasPercentage(read / self.Ro, 5)
        val["RAW_VALUE"] = raw_value
        return val

    def MQ_GetGasPercentage(self, rs_ro_ratio, gas_id):
        curves = [
            [1.0,0.18,-0.32],  # ACETON
            [1.0,0.2,-0.30],   # TOLUENO
            [1.0,0.28,-0.32],  # ALCOHOL
            [1.0,0.38,-0.37],  # CO2
            [1.0,0.42,-0.42],  # NH4
            [1.0,0.45,-0.26]   # CO
        ]
        pcurve = curves[gas_id]
        return math.pow(10, (((math.log(rs_ro_ratio) - pcurve[1]) / pcurve[2]) + pcurve[0]))

# Example of using the MQ135 class
sensor = MQ135()
print(sensor.MQ_Percentage())
