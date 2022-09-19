import time
from datalog.adc.adc import Adc
from datalog.adc.config import AdcConfig
from datalog.data import DataStore
from datalog.data import Reading
import numpy as np
import pandas as pd

#picolog setup
# load ADC with default config
adc24 = AdcConfig()
adc = Adc.load_from_config(adc24)
# datastore holding last 1000 readings
datastore = DataStore(1000)

cols = ['channel1', 'channel2']
arr = np.array(np.mat([0,0]))
df=pd.DataFrame(arr, columns=cols)
df.iloc[0]=0

# open ADC
with adc.get_retriever(datastore) as retriever:
    
    # default last reading time
    last_reading = 0

    while(retriever.retrieving):
        
        # look for new readings
        new_readings = datastore.get_readings(pivot_time=last_reading)
        if len(new_readings):
            readingData = str(new_readings[-1])
            # print(readingData)
            arr2 = np.array(np.mat(readingData.split(','),dtype=float))
            df2 = pd.DataFrame(arr2, columns = cols)
            df = pd.concat([df, df2], ignore_index=True)
            print(df)
            df.to_csv('/Users/jyou/Desktop/Fungal_Signal_Visualization/pico2tsv/example.csv')
            # Define callback to update graph
        # sleep for 1 second
        time.sleep(1)
        
        