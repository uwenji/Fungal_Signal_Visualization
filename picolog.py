import os 

#picolog lib from picolib
src = '/Applications/PicoLog.app/Contents/Resources/libpicohrdl.dylib'

import time

from datalog.adc.adc import Adc
from datalog.adc.config import AdcConfig
from datalog.data import DataStore
from datalog.adc.hrdl.picolog import PicoLogAdc24

# load ADC with default config
config = AdcConfig.get_config_filepath('/Users/jyou/Desktop/Fungal_Signal_Visualization/piclog_data/Aug 19, 2022 2-59-08 PM.picolog')
adc = Adc.load_from_config(config)

# datastore holding last 1000 readings
datastore = DataStore(1000)

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