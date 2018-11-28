import datetime
import os
import time

from backports import configparser

start_time = str(round(time.time(), 0))


class Support:

    def __init__(self, config_file):
        self.config_file = config_file

    def get_config(self, section, key):
        # reads config_file, returns value of specified section and key
        parser = configparser.ConfigParser()
        parser.read(self.config_file)
        value = parser.get(section, key)
        return value

    def write_to_log(self, data_to_write):
        # writes function input to log file and terminal output
        naming_scheme = self.get_config("Log Config", "Log Naming Scheme")
        log_time = datetime.datetime.now().strftime(naming_scheme)
        print(data_to_write)
        log_file_dir = self.get_config("Log Config", 'Log File Location')
        log_file_location = os.path.join(log_file_dir, "log-" + log_time + ".txt")
        log_file = open(log_file_location, "a+")
        log_file.write("(" + log_time + "/" + start_time + ") " + data_to_write + "\n")
        log_file.close()


