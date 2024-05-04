import time
import math
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import ADS1115

class MQ2():

    RL_VALUE = 10  # Load resistance in kilo ohms
    RO_CLEAN_AIR_FACTOR = 9.83  # Sensor resistance in clean air divided by RO

    # Calibration and read sample settings
    CALIBRATION_SAMPLE_TIMES = 50
    CALIBRATION_SAMPLE_INTERVAL = 50
    READ_SAMPLE_INTERVAL = 50
    READ_SAMPLE_TIMES = 5

    # Gas types
    GAS_LPG = 0
    GAS_CO = 1
    GAS_SMOKE = 2
    GAS_PROPANE = 3
    GAS_H2 = 4
    GAS_ALCOHOL = 5
    GAS_CH4 = 6

    def __init__(self, Ro=10, channel=0):
        self.Ro = Ro
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS1115(self.i2c)
        self.channel = AnalogIn(self.ads, channel)
        self.ads.gain = 1

        # Gas calibration curves
        self.LPGCurve = [2.3, 0.21, -0.47]
        self.COCurve = [2.3, 0.72, -0.34]
        self.SmokeCurve = [2.3, 0.53, -0.44]
        self.PropaneCurve = [2.3, 0.24, -0.47]
        self.H2Curve = [2.3, 0.33, -0.47]
        self.AlcoholCurve = [2.3, 0.45, -0.37]
        self.CH4Curve = [2.3, 0.49, -0.38]

        print("Calibrating MQ-2...")
        self.Ro = self.MQ2_Calibration()
        print(f"Calibration of MQ-2 is done. Ro={self.Ro:.2f} kohm\n")

    def MQ2_Calibration(self):
        val = 0.0
        for _ in range(self.CALIBRATION_SAMPLE_TIMES):
            val += self.MQResistanceCalculation(self.channel.value)
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL / 1000.0)
        val /= self.CALIBRATION_SAMPLE_TIMES
        return val / self.RO_CLEAN_AIR_FACTOR

    def MQResistanceCalculation(self, raw_adc):
        if raw_adc == 0:
            raw_adc = 1
        return float(self.RL_VALUE * (self.ads.gain * 65535 - raw_adc) / float(raw_adc))

    def MQRead(self):
        rs = 0.0
        for _ in range(self.READ_SAMPLE_TIMES):
            adc_value = self.channel.value
            rs += self.MQResistanceCalculation(adc_value)
            time.sleep(self.READ_SAMPLE_INTERVAL / 1000.0)
        rs /= self.READ_SAMPLE_TIMES
        return rs

    def MQPercentage(self):
        read = self.MQRead()
        return {
            "GAS_LPG": self.MQGetGasPercentage(read / self.Ro, self.GAS_LPG),
            "CO": self.MQGetGasPercentage(read / self.Ro, self.GAS_CO),
            "SMOKE": self.MQGetGasPercentage(read / self.Ro, self.GAS_SMOKE),
            "PROPANE": self.MQGetGasPercentage(read / self.Ro, self.GAS_PROPANE),
            "H2": self.MQGetGasPercentage(read / self.Ro, self.GAS_H2),
            "ALCOHOL": self.MQGetGasPercentage(read / self.Ro, self.GAS_ALCOHOL),
            "CH4": self.MQGetGasPercentage(read / self.Ro, self.GAS_CH4)
        }

    def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
        curve = {
            self.GAS_LPG: self.LPGCurve,
            self.GAS_CO: self.COCurve,
            self.GAS_SMOKE: self.SmokeCurve,
            self.GAS_PROPANE: self.PropaneCurve,
            self.GAS_H2: self.H2Curve,
            self.GAS_ALCOHOL: self.AlcoholCurve,
            self.GAS_CH4: self.CH4Curve
        }.get(gas_id, [1.0, 0.0, 0.0])
        return math.pow(10, ((math.log(rs_ro_ratio) - curve[1]) / curve[2]) + curve[0])

if __name__ == '__main__':
    mq2_sensor = MQ2()
    print(mq2_sensor.MQPercentage())
