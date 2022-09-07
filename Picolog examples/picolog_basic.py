import time
from datalog.adc.adc import Adc
from datalog.adc.config import AdcConfig
from datalog.data import DataStore
from datalog.data import Reading


#picolog setup
# load ADC with default config
adc24 = AdcConfig()
conf = adc24.get_config_filepath()
adc24.create_user_config_file(conf)

adc = Adc.load_from_config(adc24)
if adc.is_open:
    adc.open()
adc._get_hrdl_lib()
# datastore holding last 1000 readings
datastore = DataStore(1000)
setReading = Reading(10000,[1,2],  [1000,1000])
adc.configure()
print(adc.get_full_unit_info())

# open ADC
with adc.get_retriever(datastore) as retriever:
    # default last reading time
    last_reading = 0
    
    while(True):
        # look for new readings
        new_readings = datastore.get_readings(pivot_time=last_reading)
        if len(new_readings):
            # display readings
            # list = []
            for reading in new_readings:
                print(reading)
            
            # readingData = str(new_readings[-1])
            # firstData = float(readingData.split(',')[0].replace('[',''))
            # print(firstData)
            
            # get the last fetched reading's time
            # last_reading = new_readings[-1].reading_time

        # sleep for 1 second
        time.sleep(1)
        