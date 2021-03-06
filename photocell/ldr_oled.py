''' LDR photocell sensor on OLED display
    2017-0805 PePo initial version
#'''
import machine, time
import ssd1306

import machine, time

_ADC_PIN = const(0)
_WARNING_LED_PIN = const(14)

# create ADC-object
adc = machine.ADC(_ADC_PIN)
#TEST: print('ADC reading:', adc.read())
led = machine.Pin(_WARNING_LED_PIN, machine.Pin.OUT)

# create i2c for display
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=100000)
print('i2c.scan: ', i2c.scan())   #[60]
# OLED screen dimensions
__WIDTH = const(128)
__HEIGHT = const(32)
oled = ssd1306.SSD1306_I2C(__WIDTH, __HEIGHT, i2c)

# alert ON and OFF
def alertOn():
    led.on()

def alertOff():
    led.off()

# Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - Uref):
_UREF = 1.6 # Ucc=1.6 volt in circuit
def adc2voltage(value):
    return value * (_UREF / 1023.0)

# Convert the analog reading (which goes from 0 - 1023) to a resistor value for the sensor
# ref. 10K
__MAX_VALUE = const(1023)
def Rsensor(value):
    return max( (__MAX_VALUE - value)*10/value, 0)

# run reading sensor, Ctrl-C to abort
#WERKT NIET: _TRESHOLD = const(500) # sensorvalue
_TRESHOLD = 1.0 #0.7 # voltage
def run(dt=2.0):
    print('LDR demo on OLED')
    try:
        while True:
            oled.fill(0)  # clear screen
            reading = adc.read()
            voltage = adc2voltage(reading)
            rsensor = Rsensor(reading)
            print('Photocell reading {0}\tvoltage {1:0.2f}\trsensor {2:0.2f}'.format(reading, voltage, rsensor))
            oled.text('Sensor: {0} '.format(reading),0,0)
            oled.text('Voltage: {0:0.2f}'.format(voltage),0,10)
            oled.text('Rsensor: {0:0.1f}'.format(rsensor),0,20)
            if voltage > _TRESHOLD:
                alertOn()
            else:
                alertOff()
            oled.show()
            time.sleep(dt) #wait > s, see datasheet
    except:
        print('Exception! Done')
run(1.0)
#run(5.0)
