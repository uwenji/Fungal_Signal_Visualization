import time

from datalog.adc.adc import Adc

import datalog.adc.config
datalog.adc.config
from datalog.data import DataStore
from datalog.adc.hrdl.picolog import PicoLogAdc24

# load ADC with default config
adc = Adc.load_from_config(PicoLogAdc24.configure)


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
        