# address2img
A python module to convert addresses to map images using open source map data sources and mapnik.
## Installation
address2img works on any system with mapnik 2.x or newer.

Mapnik must be installed before proceeding with install.
To test for mapnik, run
```bash
mapnik-config -v # Should return a version 2.x or newer
```

Use pip to install address2img
```bash
sudo python -m pip install address2img
```

## Basic Usage
To use address2img, the configuration file and mapnik xml file must be configured.
The configuration file is (config.ini)[config.ini] by default. To configure the mapnik xml file, see (here)[https://github.com/mapnik/mapnik/wiki/XMLConfigReference].

After the config and xml files are configured, usage is as simple as importing the module and calling the function.
```python
# importing map_maker file from address2img
from address2img import map_maker

# defining addresses for which render maps, must be a list
addresses = [
    'Piazza del Duomo, 56126 Pisa PI, Italy',
    '1600 Pennsylvania Ave NW, Washington, DC 20500',
    ]
    
# instantiating Map_Maker class with addresses
worker = map_maker.Map_Maker(addresses)

# calling make_map method of the Map_Maker instance
worker.make_map()

```