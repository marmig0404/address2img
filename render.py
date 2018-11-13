import sys, os

from address2img import address_converter
import support
import mapnik




class Renderer:


    @staticmethod
    def parse_map_database(map_database):
        # converts postgresql database to postgis datasource for mapnik
        host = map_database.host
        port = map_database.port
        dbname = map_database.dbname
        username = map_database.username
        password = map_database.password
        table_names = map_database.table_names
        geometry_columns = map_database.geometry_colums
        postgis_data_sources = list()
        index = 0
        for table in table_names:
            geometry_column = geometry_columns[index]
            params = dict()
            params['host'] = host
            params['port'] = port
            params['user'] = username
            params['password'] = password
            params['dbname'] = dbname
            params['table'] = table
            params['geometry_field'] = geometry_column
            params['estimate_extent'] = False
            params['extent'] = 'x1,y1,x2,y2'  # Define how to create extents based off mile values
            postgis_data_sources.extend(mapnik.PostGIS(**params))
            index = index + 1
        return postgis_data_sources

    def __init__(self, map_database, address_database, output_location):
        # defining universal settings for all map images
        self.settings = {
            'px_width': support.get_config("Map Image Config", "Width In px"),
            'px_height': support.get_config("Map Image Config", "Height In px"),
            'mile_width': support.get_config("Map Image Config", "Width In Miles"),
            'mile_height': support.get_config("Map Image Config", "Height In Miles"),
            'output_location': support.get_config("General Config", "Output Location"),
            'naming_scheme': support.get_config("General Config", "Output Naming Scheme"),
            'output_type': support.get_config("General Config", "Output File Type"),
            'run_mode': support.get_config("General Config", "Operation Mode"),
            'temp_folder': os.path.join(os.path.realpath(__file__), 'temp')
        }
        self.map_database = map_database
        self.address_database = address_database
        self.output_location = output_location
        self.data_sources = Renderer.parse_map_database(map_database)
        support.write_to_log("New Renderer Initialized")



    def write_map_location(self, map_image):
        # final step in rendering process, writes the final location and updates last modified time in database
        address_database = self.address_database
        address = map_image[0]
        image_location = map_image[1]
        command = "UPDATE " + address_database.table + " SET " + address_database.map_image_column + " = '" \
                  + image_location + "', " + address_database.last_modified_column + " = '" + support.start_time \
                  + " WHERE " + address_database.address_column + " = '" + address + "'"
        address_database.execute_command(command)
        support.write_to_log("Updated address database with map location and modification time.")
        support.write_to_log("Map Location: " + image_location + " Modification time: " + support.start_time + ".")

    @staticmethod
    def get_map_name(image):
        # generates a name for the image based on file type, naming scheme, and a hash of the image
        # hash image, take first 8 digits
        # use Renderer.naming_scheme to create name
        return map_name

    def make_layers(self):
        sources = self.data_sources
        layers = list()
        index = 0
        for source in sources:  # makes a layer for each data source specified in config.ini
            layers[index] = mapnik.Layer("layer" + str(index))
            layers[index].datasource = source
            layers[index].styles.append('Style')
        return layers

    def make_image(self, address):
        # renders image from database around address specified using settings from config.ini

        support.write_to_log("Attempting to make map for " + address + ".")
        coordinate = address_converter.convert_address(address)

        layers = self.make_layers()
        image = mapnik.Map(self.settings['px_width'], self.settings['px_height'])
        for layer in layers:
            image.layers.append(layer)
        image.zoom() #check on this function here, this is where the implementation of the mile size comes in
        image_name = Renderer.get_map_name(image)
        image_template = mapnik.Image(image.width, image.height)
        mapnik.render(image, image_template)
        # Renderer.temp_folder, Renderer.output_type
        image_location = self.output_location + image_name
        support.write_to_log("Created map successfully.")
        support.write_to_log("Path to map: " + image_location)
        return [address, image_location]

    def make_images(self):
        # iterative make_image function
        maps = list()
        addresses = self.get_addresses()
        for address in addresses:
            maps.append(self.make_image(address))
        return maps

    def render(self):
        # main method of class, calls other methods in order
        maps = self.make_images()
        for map in maps:
