from datetime import datetime
import os

log_file_name = "log_S.txt"


def log_file(string):
    pid = os.getpid()
    with open(log_file_name, "a") as file:
        current_time = str(datetime.now())
        string += '\n'
        time = '[' + current_time + '] '
        file.write(time)
        pid = '{' + str(pid) + '} '
        file.write(pid)
        file.write(string)