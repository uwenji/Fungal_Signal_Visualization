import time
from datalog.adc.adc import Adc
from datalog.adc.config import AdcConfig
from datalog.data import DataStore
from datalog.data import Reading
import numpy as np

#picolog setup
# load ADC with default config
adc24 = AdcConfig()
print(AdcConfig.get_config_filepath())
adc = Adc.load_from_config(adc24)
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
            readingData = str(new_readings[-1])
            # print(new_readings[-1])
            # print(new_readings)
            arr = np.array(np.mat(readingData.split(','),dtype=float))
            # arr = np.array(np.mat(readingData.split(',')))
            # Define callback to update graph
        # sleep for 1 second
        time.sleep(1)
        