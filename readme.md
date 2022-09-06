# Fungal Signal Visualization

this project link the piclog signal to art-net led device.

## Picolog
- the library from datalog in python, and it need to modifty the lib swift to Picolog24 and Picolog24Sim
    - datalog.adc.adc.py -- load_from_config():
        change the picologsim.
- the data python dylib in mac:
    - datalog.adc.config.py -- adcConfig. self["picolog"] = 'lib_path_adc24': '/Applications/PicoLog.app/Contents/Resources/libpicohrdl.dylib' 
- the modify add.conf.dist at /datalog/adc/adc.conf.dist 
  - [device]
    sample_time = 3000
    conversion_time = 4

  - [adc]
    type = PicoLog24

  - [picolog]
    channel config
    channel_0 = true
    channel_0_range = 0
    channel_0_type = 1
    channel_1 = true
    channel_1_range = 0
    channel_1_type = 1


this project is developed under eu horizon 2020 project the fungal architectures at CITA in Copenhagen.