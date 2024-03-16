from machine import ADC, Pin
import utime

class MQ2GasSensor:
    RO_CLEAN_AIR_FACTOR = 9.83  # Ro value in clean air
    MQ_SAMPLE_TIMES = 5         # Number of samples to take
    MQ_SAMPLE_INTERVAL = 5000   # Interval between samples in milliseconds

    def __init__(self, pin):
        self.pin = ADC(pin)
        self.pin.atten(ADC.ATTN_11DB)  # Set 11dB attenuation for full range
        self.Ro = self.calibrate()

    def calibrate(self):
        val = 0
        for _ in range(self.MQ_SAMPLE_TIMES):
            val += self.pin.read()
            utime.sleep_ms(self.MQ_SAMPLE_INTERVAL)
        val = val / self.MQ_SAMPLE_TIMES
        Rs_Ro = val / self.RO_CLEAN_AIR_FACTOR
        return Rs_Ro

    def get_gas_concentration(self):
        val = 0
        for _ in range(self.MQ_SAMPLE_TIMES):
            val += self.pin.read()
            utime.sleep_ms(self.MQ_SAMPLE_INTERVAL)
        val = val / self.MQ_SAMPLE_TIMES
        Rs_Ro = val / self.Ro
        return self.get_ppm(Rs_Ro)

    def get_ppm(self, ratio):
        if 0.05 <= ratio <= 0.6:
            return 0.87 * ratio ** -1.07  # Formula for LPG, propane, methane
        elif 0.6 < ratio <= 1.6:
            return 0.22 * ratio ** 2.17    # Formula for alcohol
        elif 1.6 < ratio <= 3.0:
            return 1.25 * ratio ** 1.21    # Formula for hydrogen
        elif 3.0 < ratio <= 5.0:
            return 2.3 * ratio ** 0.68     # Formula for smoke
        else:
            return 0

# Define pin numbers according to your connections
DATA_PIN = 0  # Example pin number, change it as needed

mq2 = MQ2GasSensor(DATA_PIN)

while True:
    ppm = mq2.get_gas_concentration()
    print("Gas concentration (ppm):", ppm)
    utime.sleep(5)  # Adjust the interval as needed
