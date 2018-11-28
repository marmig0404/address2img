# importing map_maker file from address2img
from address2img import map_maker

# defining config file
config_file = 'config.ini'

# defining addresses for which render maps, must be a list
addresses = [
    'Piazza del Duomo, 56126 Pisa PI, Italy', # Leaning Tower of Pisa
    '1600 Pennsylvania Ave NW, Washington, DC 20500', # The White House
    'Parque Nacional da Tijuca, Alto da Boa Vista, Rio de Janeiro, Brazil',
]

# instantiating Map_Maker class with addresses and config file
worker = map_maker.Map_Maker(addresses, config_file)

# calling make_map method of the Map_Maker instance
worker.make_map()