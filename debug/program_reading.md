Adc.load_from_config()

load_from_config(cls, config):

    logger.info() #print
    from datalog.adc.hrdl.picolog import PicoLogAdc24, PicoLogAdc24Sim, PicoLogAdc20

    if config['adc']['type'] == 'PicoLog24':
            return PicoLogAdc24(config)
    #config: parameter

change the program to picolog24
    datalog.adc.hrdl.constants.Status

1661349685657,-239673.0,-238428.0,-237950.0,-241718.0
1661349688657,-232470.0,-232952.0,-231307.0,-237344.0
1661349691657,-229191.0,-230519.0,-228567.0,-235287.0