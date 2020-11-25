## -*- coding: utf-8 -*-
from datetime import datetime

log_file_name = "log_M.txt"
data_file_name = "data.txt"
log_msf_name = "log_ms.txt"


ACTION_TG = {
    1: "received message",
    2: "sent message"
}

ERRORS_TG = {
    'FILE_DOESNT_EXIST': "File doesn't exist",
    'INSTANCE_ALREADY_EXIST': "Cat't create class instance. It exist already"
}

STATE_TG = {
    'INSTANCES_ADDED': "Instances added to dict",
    'DATA_CHANGED': "File entry has been changed",
    'DATA_ADDED': "Data has been added to file"
}


SEP_SYM = '|'


def log_file(string, id='', act='', server=0):
    with open(log_file_name, "a") as file:
        current_time = str(datetime.now())
        string += '\n'
        if id or act:
            extra = '{Telegram'
            if id:
                extra = extra + ':id=' + str(id)
            if act in ACTION_TG:
                extra = extra + ':' + ACTION_TG[act]
        else:
            if server:
                extra = '{Server'
            else:
                extra = '{Debug'
        extra += '} '
        time = '[' + current_time + '] '
        file.write(time)
        file.write(extra)
        file.write(string)


def save_data(instance):
    try:
        file = open(data_file_name, 'r+')
    except:
        file = open(data_file_name, 'a')  # when file exist, but there is an error
    len_f = 0                              # it will be save call 'a+' instead 'w+'
    ret = 'DATA_ADDED'

    for line in file:
        if str(instance.id) in line:
            file.seek(len_f, 0)
            file.write(str(instance.id))
            file.write(SEP_SYM)
            file.write(str(instance.order_count))
            file.write(SEP_SYM)
            file.write(str(instance.next_time_order))
            file.write(SEP_SYM)
            file.write(str(instance.city))
            file.write(SEP_SYM)
            ret = 'DATA_CHANGED'
            break
        len_l = len(line)  #+ 1  # use only for Windows
        len_f += len_l
    else:
        file.write(str(instance.id))
        file.write(SEP_SYM)
        file.write(str(instance.order_count))
        file.write(SEP_SYM)
        file.write(str(instance.next_time_order))
        file.write(SEP_SYM)
        file.write(str(instance.city))
        file.write(SEP_SYM)
        line = '\x00' * 40 + '\n'
        file.write(line)

    file.close()
    return ret


def restore_data(cur_dict, Cur_class, restore=1):
    """
    You must call this function only when ur server crashed.
    This function returns class instances with previous
    value of variables
    """
    count = 0  # how many instances have been added

    try:
        file = open(data_file_name, 'r')
    except:
        return 'FILE_DOESNT_EXIST', count

    for line in file:
        line = line.split(SEP_SYM)
        id = line[0]
        order_count = int(line[1])
        try:
            next_time_order = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S.%f')
        except:  # when it has 0
            next_time_order = line[2]

        city = line[3]
        if city == 'False':
            city = bool(0)

        if id in cur_dict:
            return 'INSTANCE_ALREADY_EXIST', count  # change it later ???

        cur_dict[id] = Cur_class(id, order_count=order_count,
                                 next_time_order=next_time_order, city=city,
                                 restore=restore)
        count += 1

    return 'INSTANCES_ADDED', count


def code_stat(city, id, code):
    file_name = 'code_statistics.txt'
    file = open(file_name, 'a+')
    msg = str(city) + '| ' + str(id) + ' | ' + str(code) + '\n'
    file.write(msg)
    file.close()


def log_msf(string):
    with open(log_msf_name, "a") as file:
        current_time = str(datetime.now())
        string += '\n'
        time = '[' + current_time + '] '
        file.write(time)
        file.write(string)