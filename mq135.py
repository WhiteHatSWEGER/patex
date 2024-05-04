import time
import math
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import ADS1115

class MQ135():
    RL_VALUE = 10  # Load resistance in kilo ohms
    RO_CLEAN_AIR_FACTOR = 3.6  # Sensor resistance in clean air divided by RO

    # Calibration and read sample settings
    CALIBRATION_SAMPLE_TIMES = 50
    CALIBRATION_SAMPLE_INTERVAL = 50
    READ_SAMPLE_INTERVAL = 50
    READ_SAMPLE_TIMES = 5

    # Gas types
    GAS_ACETON = 0
    GAS_TOLUENO = 1
    GAS_ALCOHOL = 2
    GAS_CO2 = 3
    GAS_NH4 = 4
    GAS_CO = 5

    def __init__(self, Ro=10, channel=0):
        self.Ro = Ro
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS1115(self.i2c)
        self.channel = AnalogIn(self.ads, channel)
        self.ads.gain = 1

        # Gas calibration curves
        self.ACETONCurve = [1.0, 0.18, -0.32]
        self.TOLUENOCurve = [1.0, 0.2, -0.30]
        self.AlcoholCurve = [1.0, 0.28, -0.32]
        self.CO2Curve = [1.0, 0.38, -0.37]
        self.NH4Curve = [1.0, 0.42, -0.42]
        self.COCurve = [1.0, 0.45, -0.26]

        print("Calibrating MQ-135...")
        self.Ro = self.MQ135_Calibration()
        print(f"Calibration of MQ-135 is done. Ro={self.Ro:.2f} kohm\n")

    def MQ135_Calibration(self):
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
            "ACETON": self.MQGetGasPercentage(read / self.Ro, self.GAS_ACETON),
            "TOLUENO": self.MQGetGasPercentage(read / self.Ro, self.GAS_TOLUENO),
            "ALCOHOL": self.MQGetGasPercentage(read / self.Ro, self.GAS_ALCOHOL),
            "CO2": self.MQGetGasPercentage(read / self.Ro, self.GAS_CO2),
            "NH4": self.MQGetGasPercentage(read / self.Ro, self.GAS_NH4),
            "CO": self.MQGetGasPercentage(read / self.Ro, self.GAS_CO),
        }

    def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
        curve = {
            self.GAS_ACETON: self.ACETONCurve,
            self.GAS_TOLUENO: self.TOLUENOCurve,
            self.GAS_ALCOHOL: self.AlcoholCurve,
            self.GAS_CO2: self.CO2Curve,
            self.GAS_NH4: self.NH4Curve,
            self.GAS_CO: self.COCurve
        }.get(gas_id, [1.0, 0.0, 0.0])
        return math.pow(10, ((math.log(rs_ro_ratio) - curve[1]) / curve[2]) + curve[0])

if __name__ == '__main__':
    mq135_sensor = MQ135()
    print(mq135_sensor.MQPercentage())
