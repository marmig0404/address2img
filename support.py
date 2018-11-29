import datetime
import os
import time

from backports import configparser

start_time = time.time()


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
        try:
            data_to_write = data_to_write.encode('utf8')
        except UnicodeDecodeError:
            data_to_write = data_to_write.decode('utf-8').encode('ascii', 'replace')
        naming_scheme = self.get_config("Log Config", "Log Naming Scheme")
        log_time = datetime.datetime.now().strftime(naming_scheme)
        print(data_to_write)
        log_dir = self.get_config("Log Config", 'Log File Location')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_location = os.path.join(log_dir, "log-" + log_time + ".txt")
        log_file = open(log_file_location, "a+")
        log_file.write("(" + log_time + "/" + repr(round(start_time, 0)) + ") " + str(data_to_write) + "\n")
        log_file.close()


