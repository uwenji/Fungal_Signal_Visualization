import time

from datalog.adc.adc import Adc
from datalog.adc.config import AdcConfig
from datalog.data import DataStore

# load ADC with default config
adc = Adc.load_from_config(AdcConfig())
if adc.is_open:
    adc.open()
adc._get_hrdl_lib()
# datastore holding last 1000 readings
datastore = DataStore(1000)
adc.configure()
print(adc.get_full_unit_info())
print(adc.get_last_error_message())
# open ADC
with adc.get_retriever(datastore) as retriever:
    # default last reading time
    last_reading = 0
    
    while(True):
        # look for new readings
        new_readings = datastore.get_readings(pivot_time=last_reading)

        if len(new_readings):
            # display readings
            for reading in new_readings:
                print(reading)

            # get the last fetched reading's time
            last_reading = new_readings[-1].reading_time

        # sleep for 1 second
        time.sleep(1)