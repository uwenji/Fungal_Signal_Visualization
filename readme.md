# Fungal Signal Visualization

this project link the piclog signal to art-net led device.

## Picolog
- the library from datalog in python, and it need to modifty the lib swift to Picolog24 and Picolog24Sim
    - datalog.adc.adc.py -- load_from_config():
        change the picologsim.
- the data python dylib in mac:
    - datalog.adc.config.py -- adcConfig. self["picolog"] = 'lib_path_adc24': '/Applications/PicoLog.app/Contents/Resources/libpicohrdl.dylib' 


this project is developed under eu horizon 2020 project the fungal architectures at CITA in Copenhagen.