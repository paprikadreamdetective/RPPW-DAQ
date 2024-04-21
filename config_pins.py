"""
Esta hash table provee el ID de los pines GPIO
de la Raspberry Pi Pico W, ofrece la siguiente
configuracion:
    
    - SPI 
    - PWM 

Modificaciones:
    Antes LEDC_BIT 8 : Despues PWM_BIT_RESOLUTION

    
"""

cfg_pin = {
    'SPI': {
        'SPI_CLK' : 18,
        'SPI_DOUT' : 16,
        'SPI_DIN' : 19,
        'CSn' : 17 
    },
    'PWM': {
        'PWM_BIT_RESOLUTION' : 8,
        'PWM_BASE_FREQUENCY' : 800,
        'PIN_CHANNEL_0' : 0,
        'PIN_CHANNEL_1' : 1,
        'PIN_CHANNEL_2' : 2,
        'PIN_CHANNEL_3' : 3,
        'PIN_CHANNEL_4' : 4,
        'PIN_CHANNEL_5' : 5
    }
}