import os
import time
import datetime
from backports import configparser

config_file = 'render-config.ini'
start_time = str(round(time.time(), 0))


def get_config(section, key):
    # reads CONFIG_FILE, returns value of specified section and key
    parser = configparser.ConfigParser()
    parser.read(config_file)
    value = parser.get(section, key)
    return value


def write_to_log(data_to_write):
    # writes function input to log file and terminal output
    naming_scheme = get_config("General Config", "Log Naming Scheme")
    log_time = datetime.datetime.now().strftime(naming_scheme)
    print(data_to_write)
    log_file_location = os.path.join("logs", "log-" + log_time + ".txt")
    log_file = open(log_file_location, "a")
    log_file.write("(" + log_time + "/" + start_time + ") " + data_to_write + "\n")
    log_file.close()

