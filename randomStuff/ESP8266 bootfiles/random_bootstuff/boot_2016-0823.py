# This file is executed on every boot (including wake-boot from deepsleep)
# 2016-0823 PePo disable debug for using ampy (Adafruit)
import esp
esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()
gc.collect()
