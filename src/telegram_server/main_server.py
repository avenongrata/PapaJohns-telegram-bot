## -*- coding: utf-8 -*-
from socket import *
import threading
import select
import time
import random
import os
from log import log_file

ip_server = ''  # 'localhost'
port_server = 9816
psd_server = 'NaNgrataTG-t'
psd_admin = 'NaNgrataAdminTG-t'
HMFPEX = 5  # hom much free processes exist (default for every server)
servers_info = {}  # structure -> 'ip': [socket, how much processes, True/False (auth), [{city: count}, ... ]]
servers_admin = []
readsocks = []
lock = None  # ?


DEBUG = 1
if DEBUG:
    def print_fun(*string):
        for x in string:
            print(x, end=' ')
        print()
else:
    def print_fun(*string):
        pass


def check_th(count=1):
    if count == 1:
        print_fun("Locked >>>>", threading.get_ident())
    else:
        print_fun("Unlocked >>>>", threading.get_ident())


RET_VALUES = {
    'NOCODE': "There is no code now",
    'CNTOPNFILE': "Can't open file",
    'UNEXERROR': 'Unexpected error',
    'FILTNIS': "File is less, then numbers in structure",
    'NTATTF': "Nothing to add to the file",
}

HANDLE = {
    'FUSZ': 'There is no work for crafting code',  # need 1 code & 5 codes at once
    'FUSOF': 'There is one process for crafting, but less than 5 codes',  # need 5 codes
    'FUSOE': 'There is one & more processes for crafting, it craft 5 & more codes',  # don't need codes

    'FUSEPF': 'Enough processes are free',  # can send work
    'FUSNEFP': 'There is not enough processes for work',  # must send only one work (the biggest)
    'FUSNFP': 'There are not free processes for any work',  # can't send any work

    'FHMWCS': 'Can send work on S-server',
    'FHMWCNS': "Can't send work on S-server",
}

cities = {
    '1': ['Москва и мос. область', 'https://www.papajohns.ru/30off', 'city1.txt', 1, 0, 0, 20, False, 'city1_add.txt'],
    #'2': ['Ангарск', 'https://www.papajohns.ru/promo/angarsk/30/', 'city2.txt', 1, 0, 0, 5, False, 'city2_add.txt'],
    '2': ['Екатеринбург', 'https://www.papajohns.ru/promo/ekb/30/', 'city3.txt', 1, 0, 0, 10, False, 'city3_add.txt'],
    # '4': ['Кострома', 'https://kostroma.papajohns.ru/30off', 'city4.txt', 1, 0, 0, 5, False, 'city4_add.txt'],
    # '5': ['Нижневартовск', 'https://nizhnevartovsk.papajohns.ru/30off', 'city5.txt', 1, 0, 0, 5, False, 'city5_add.txt'],
    # '6': ['Новокузнецк', 'https://nvkz.papajohns.ru/30off', 'city6.txt', 1, 0, 0, 10, False, 'city6_add.txt'],
    '3': ['Нижний Новгород', 'https://nn.papajohns.ru/30off', 'city7.txt', 1, 0, 0, 10, False, 'city7_add.txt'],
    # '8': ['Обнинск', 'https://obninsk.papajohns.ru/30off', 'city8.txt', 1, 0, 0, 10, False, 'city8_add.txt'],
    # '9': ['Псков', 'https://pskov.papajohns.ru/30off', 'city9.txt', 1, 0, 0, 10, False, 'city9_add.txt'],
    # '10': ['Рязань', 'https://ryazan.papajohns.ru/30off', 'city10.txt', 1, 0, 0, 10, False, 'city10_add.txt'],
    # '11': ['Сургут', 'https://surgut.papajohns.ru/promo30', 'city11.txt', 1, 0, 0, 10, False, 'city11_add.txt'],
    '4': ['Санкт-Петербург', 'https://spb.papajohns.ru/30off', 'city12.txt', 1, 0, 0, 10, False, 'city12_add.txt'],
    # '13': ['Сочи', 'https://www.papajohns.ru/30off', 'city13.txt', 1, 0, 0, 10, False, 'city13_add.txt'],
    #'6': ['Томск', 'https://www.papajohns.ru/promo/tomsk/30/', 'city14.txt', 1, 0, 0, 5, False, 'city14_add.txt'],
    '5': ['Тверь', 'https://tver.papajohns.ru/30off', 'city15.txt', 1, 0, 0, 5, False, 'city15_add.txt'],
    #'8': ['Тюмень', 'https://tyumen.papajohns.ru/promo/tyumen/30OFF/', 'city16.txt', 1, 0, 0, 5, False,
          #'city16_add.txt'],
    # '17': ['Тамбов', 'https://tambov.papajohns.ru/30off', 'city17.txt', 1, 0, 0, 5, False, 'city17_add.txt'],
}


def msg_admin(data):
    message = "From {0}: data = {1}".format(msg_admin.__qualname__, data)
    print_fun(message)
    log_file(message, server=1)

    data = data.split(',')
    if len(data) != 3:
        message = "From {0}: In message values are less then 3".format(msg_admin.__qualname__)
        print_fun(message)
        log_file(message, server=1)
        return -1

    ip = data[0].lstrip('\n ').rstrip('\n ')
    city = data[1].lstrip('\n ').rstrip('\n ')
    count = data[2].lstrip('\n ').rstrip('\n ')
    msg = city + ',' + count

    message = "From {0}: ip = {1}; msg = {2}".format(msg_admin.__qualname__, ip, msg)
    print_fun(message)
    log_file(message, server=1)

    return ip, msg


def delete_value(l, val):
    message = "From {0}: list = {1}, val = {2}".format(delete_value.__qualname__, l, val)
    print_fun(message)
    log_file(message, server=1)

    message = "Call %s" % transform_value.__qualname__
    print_fun(message)
    log_file(message, server=1)
    val = transform_value(val)

    message = 'Returned from {0}: ret = {1}'.format(transform_value.__qualname__, val)
    print_fun(message)
    log_file(message, server=1)

    for x in l:
        if x == val:
            l.remove(x)
            break

    message = "From {0}: new list = {1}".format(delete_value.__qualname__, l)
    print_fun(message)
    log_file(message, server=1)


def delete_all_us(l, city):
    # This function will delete from list all values equals this city.
    # Need to call it before sending urgent stop to S-server
    message = "From {0}: list = {1}, city = {2}".format(delete_all_us.__qualname__, l, city)
    print_fun(message)
    log_file(message, server=1)

    count = 0
    for x in l:
        if city in x.keys():
            count += 1

    message = "From {0}: count = {1}".format(delete_all_us.__qualname__, count)
    print_fun(message)
    log_file(message, server=1)

    i = 0
    while count > 0:
        if i >= 10:  # need it to avoid looped cycle
            break

        for x in l:
            if city in x.keys():
                l.remove(x)
                count -= 1
                break
        i += 1

    message = "From {0}: i = {1}; new count = {2}; new list = {3}".format(delete_all_us.__qualname__, i, count, l)
    print_fun(message)
    log_file(message, server=1)


def add_value(l, val):
    message = "From {0}: list = {1}, val = {2}".format(add_value.__qualname__, l, val)
    print_fun(message)
    log_file(message, server=1)

    message = "Call %s" % transform_value.__qualname__
    print_fun(message)
    log_file(message, server=1)
    val = transform_value(val)

    message = 'Returned from {0}: ret = {1}'.format(transform_value.__qualname__, val)
    print_fun(message)
    log_file(message, server=1)

    l.append(val)

    message = "From {0}: new list = {1}".format(add_value.__qualname__, l)
    print_fun(message)
    log_file(message, server=1)


def transform_value(val):
    message = "From {0}: val = {1}".format(transform_value.__qualname__, val)
    print_fun(message)
    log_file(message, server=1)

    l = val.split(',')
    d = {l[0]: l[1]}
    return d


def check_work(l, city):
    message = "From {0}: list = {1}, city = {2}".format(check_work.__qualname__, l, city)
    print_fun(message)
    log_file(message, server=1)

    count = 0
    hmw = 0  # how much work
    for x in l:
        if city not in x.keys():
            continue

        hmw += 1  # how much work
        count += int(x[city])  # how much codes for crafting

    message = "From {0}: hmw = {1}; count = {2}".format(check_work.__qualname__, hmw, count)
    print_fun(message)
    log_file(message, server=1)

    # start analyzing
    if hmw == 0:  # there is no work for this city on M-server
        message = "From {0}: {1}".format(check_work.__qualname__, HANDLE['FUSZ'])
        print_fun(message)
        log_file(message, server=1)

        return 'FUSZ'

    if hmw == 1:  # there is one process for crafting
        if count < 5:  # process is crafting less then 5 codes -> it is too few
            message = "From {0}: {1}".format(check_work.__qualname__, HANDLE['FUSOF'])
            print_fun(message)
            log_file(message, server=1)

            return 'FUSOF'
        else:  # process is crafting 5 and more codes -> it is okay. Don't send work
            message = "From {0}: {1}".format(check_work.__qualname__, HANDLE['FUSOE'])
            print_fun(message)
            log_file(message, server=1)

            return 'FUSOE'

    if hmw > 1:  # 2 & more processes craft codes -> don't need send work
        message = "From {0}: {1}".format(check_work.__qualname__, HANDLE['FUSOE'])
        print_fun(message)
        log_file(message, server=1)

        return 'FUSOE'


def analyze_server(hmp):
    # hmp max value equal 5 -> need to change function if this constant will changed
    message = "From {0}: hmp = {1}".format(analyze_server.__qualname__, hmp)
    print_fun(message)
    log_file(message, server=1)

    if hmp >= 3:
        message = "From {0}: {1}".format(analyze_server.__qualname__, HANDLE['FUSEPF'])
        print_fun(message)
        log_file(message, server=1)

        return 'FUSEPF'  # send both work (1 & 5 4.e.)

    if hmp >= 1:
        message = "From {0}: {1}".format(analyze_server.__qualname__, HANDLE['FUSNEFP'])
        print_fun(message)
        log_file(message, server=1)

        return 'FUSNEFP'  # send only biggest work (5 4.e.)

    message = "From {0}: {1}".format(analyze_server.__qualname__, HANDLE['FUSNFP'])
    print_fun(message)
    log_file(message, server=1)

    return 'FUSNFP'  # can't send something


def set_path_cities(cities):
    message = "From {0}".format(set_path_cities.__qualname__)
    print_fun(message)
    log_file(message, server=1)

    pwd = os.getcwd()
    for x in cities.keys():
        path = pwd + '/codes/' + cities[x][2]
        cities[x][2] = path

        path = pwd + '/codes/' + cities[x][8]
        cities[x][8] = path


set_path_cities(cities)  # call it here


def get_code_file(key):
    message = "From {0}: key = {1}".format(get_code_file.__qualname__, key)
    print_fun(message)
    log_file(message, server=1)

    lock.acquire()  # lock our data structure
    check_th()
    hme = cities[key][4]
    message = "From {0}: hme = {1}".format(get_code_file.__qualname__, hme)
    print_fun(message)
    log_file(message, server=1)

    if hme == 0:  # there is no code now
        add_c = cities[key][5]
        message = "From {0}: add count = {1}".format(get_code_file.__qualname__, add_c)
        print_fun(message)
        log_file(message, server=1)

        if add_c == 0:  # no codes for adding
            check_th(2)
            lock.release()
            message = "From {0}: {1}".format(get_code_file.__qualname__, RET_VALUES['NOCODE'])
            print_fun(message)
            log_file(message, server=1)

            return 'NOCODE'
        else:
            message = "Call %s" % file_code_update.__qualname__
            print_fun(message)
            log_file(message, server=1)
            ret = file_code_update(key)

            message = "Returned from {0}: ret = {1}".format(file_code_update.__qualname__, ret)
            print_fun(message)
            log_file(message, server=1)

            if ret in RET_VALUES:
                check_th(2)
                lock.release()
                message = "From {0}: {1}".format(get_code_file.__qualname__, RET_VALUES[ret])
                print_fun(message)
                log_file(message, server=1)

                return ret

    file_name = cities[key][2]
    message = "From {0}: file name = {1}".format(get_code_file.__qualname__, file_name)
    print_fun(message)
    log_file(message, server=1)

    try:
        file = open(file_name, 'r')
    except:
        check_th(2)
        lock.release()
        message = "From {0}: {1}".format(get_code_file.__qualname__, RET_VALUES['CNTOPNFILE'])
        print_fun(message)
        log_file(message, server=1)

        return 'CNTOPNFILE'

    # start redeem code
    line_count = 1
    cur_p = cities[key][3]
    message = "Start redeem code: cur pos = {0}".format(cur_p)
    print_fun(message)
    log_file(message, server=1)

    for line in file:
        if line_count == cur_p:
            code = line
            break
        line_count += 1
    else:
        file.close()
        check_th(2)
        lock.release()  # unlock our data structure
        message = "From {0}: {1}".format(get_code_file.__qualname__, RET_VALUES['FILTNIS'])
        print_fun(message)
        log_file(message, server=1)

        return 'FILTNIS'

    cities[key][3] += 1  # increase cur position in file
    cities[key][4] -= 1  # codes decreased by one
    file.close()
    check_th(2)
    lock.release()

    message = "From {0}: new cur pos = {1}; new hme = {2}".format(get_code_file.__qualname__,
                                                                  cities[key][3], cities[key][4])
    print_fun(message)
    log_file(message, server=1)

    code = code.split('|')
    code = code[0]
    return code


def file_code_update(key):
    message = "From {0}: key = {1}".format(file_code_update.__qualname__, key)
    print_fun(message)
    log_file(message, server=1)

    lock.acquire()  # if call from current thread -> will not lock
    check_th(1)
    file_name = cities[key][2]
    message = "From {0}: file name = {1}".format(file_code_update.__qualname__, file_name)
    print_fun(message)
    log_file(message, server=1)

    try:
        file = open(file_name, 'w')
    except:
        check_th(2)
        lock.release()
        message = "From {0}: {1}".format(file_code_update.__qualname__, RET_VALUES['CNTOPNFILE'])
        print_fun(message)
        log_file(message, server=1)

        return 'CNTOPNFILE'

    afile = cities[key][8]
    message = "From {0}: add file = {1}".format(file_code_update.__qualname__, afile)
    print_fun(message)
    log_file(message, server=1)

    try:
        ffile = open(afile, 'r')
    except:
        check_th(2)
        lock.release()
        message = "From {0}: Can't open {1}".format(file_code_update.__qualname__, afile)
        print_fun(message)
        log_file(message, server=1)

        return

    codes = []
    for line in ffile:
        codes.append(line.rstrip('\n '))
    ffile.close()

    message = "From {0}: new codes are -> {1}".format(file_code_update.__qualname__, codes)
    print_fun(message)
    log_file(message, server=1)

    # code_list = cities[key][7]
    for code in codes:
        code = code + '|' + '\x00' * 5 + '\n'
        file.write(code)
    file.close()

    cities[key][4] = cities[key][5]  # how much exist
    cities[key][3] = 1  # current position nullify
    cities[key][5] = 0  # add count nullify
    # cities[key][7] = []  # create new code list
    message = "From {0}: new hme = {1}; new cur pos = {2}; new add count = {3}".format(
        file_code_update.__qualname__, cities[key][4], cities[key][3], cities[key][5])
    print_fun(message)
    log_file(message, server=1)

    # delete add_file with codes
    try:
        os.remove(afile)
    except:
        message = "Some errors occurred during deleting the file(%s)" % afile
        print_fun(message)
        log_file(message, server=1)
    check_th(2)
    lock.release()


def work_test(sock):  # don't want to delete, cuz may be will need it later
    print_fun("From testing function. Sleep 5 sec")
    ip = str(sock.getpeername()[0])
    time.sleep(5)
    if servers_info[ip][2]:
        print_fun("This server was authorized")
    else:
        print_fun("Not authorized")
        return

    while True:
        string = input("Input work for server: ")
        string = string.split(',')
        if string[0] == 'stop':
            break
        if string[0] == 'us':
            urgent_stop(string[1])
        else:
            send_work(sock, string[0], string[1])


def choice_server():
    message = "From {0}".format(choice_server.__qualname__)
    print_fun(message)
    log_file(message, server=1)

    max_f_p = -1
    server_k = 0
    # get server with max free processes
    for elem in servers_info.keys():
        if not servers_info[elem][2]:
            continue  # not authorized

        if servers_info[elem][1] > max_f_p:
            max_f_p = servers_info[elem][1]
            server_k = elem

    message = "From {0}: max_f_p = {1}; server_k = {2}".format(choice_server.__qualname__, max_f_p, server_k)
    print_fun(message)
    log_file(message, server=1)

    if max_f_p == -1:
        return -1  # there is not connected servers
    elif max_f_p <= 0:
        return -2  # there is not free processes
    else:
        return server_k


def hm_work(l, city):
    message = "From {0}: list = {1}, city = {2}".format(hm_work.__qualname__, l, city)
    print_fun(message)
    log_file(message, server=1)

    count = 0
    hmw = 0  # how much work
    for x in l:
        if city not in x.keys():
            continue

        hmw += 1  # how much work
        count += int(x[city])  # how much codes for crafting

    message = "From {0}: hmw = {1}; count = {2}".format(hm_work.__qualname__, hmw, count)
    print_fun(message)
    log_file(message, server=1)

    # start analyzing
    if hmw <= 1:  # there is one/no work for this city on S-server
        message = "From {0}: {1}".format(hm_work.__qualname__, HANDLE['FHMWCS'])
        print_fun(message)
        log_file(message, server=1)

        return 'FHMWCS'

    else:  # 2 & more processes craft codes -> don't need send work
        message = "From {0}: {1}".format(hm_work.__qualname__, HANDLE['FHMWCNS'])
        print_fun(message)
        log_file(message, server=1)

        return 'FHMWCNS'


def urgent_stop(city):  # bot calls this function after client trying to get code but there is no codes for adding
    message = "From {0}: city = {1}".format(urgent_stop.__qualname__, city)
    print_fun(message)
    log_file(message, server=1)

    for server in servers_info.keys():
        if not servers_info[server][2]:
            continue  # not authorized

        message = "Call %s" % check_work.__qualname__
        print_fun(message)
        log_file(message, server=1)
        ret_w = check_work(servers_info[server][3], city)

        message = "Returned from {0}: ret = {1}".format(check_work.__qualname__, ret_w)
        print_fun(message)
        log_file(message, server=1)

        message = "Call %s" % analyze_server.__qualname__
        print_fun(message)
        log_file(message, server=1)
        ret_s = analyze_server(servers_info[server][1])

        message = "Returned from {0}: ret = {1}".format(analyze_server.__qualname__, ret_s)
        print_fun(message)
        log_file(message, server=1)

        if ret_s == 'FUSNFP':  # no free processes
            message = "From {0}: {1}".format(urgent_stop.__qualname__, HANDLE['FUSNFP'])
            print_fun(message)
            log_file(message, server=1)

            if ret_w != 'FUSZ':  # there is some work on S-server -> need stop it
                message = "From {0}: {1}".format(urgent_stop.__qualname__, HANDLE[ret_w])
                print_fun(message)
                log_file(message, server=1)

                message = "Call %s" % delete_all_us.__qualname__
                print_fun(message)
                log_file(message, server=1)
                delete_all_us(servers_info[server][3], city)  # new test it !!!

                message = "Call %s" % send_us.__qualname__
                print_fun(message)
                log_file(message, server=1)
                send_us(city, server)
                continue

            else:
                message = "From {0}: {1}".format(urgent_stop.__qualname__, HANDLE[ret_w])
                print_fun(message)
                log_file(message, server=1)
                continue

        sock = servers_info[server][0]  # get sock for sending work

        if ret_s == 'FUSNEFP' or ret_s == 'FUSEPF':  # not enough or enough processes
            message = "From {0}: {1}".format(urgent_stop.__qualname__, HANDLE[ret_s])
            print_fun(message)
            log_file(message, server=1)

            if ret_w == 'FUSZ':  # there is no work on S-server
                message = "From {0}: {1}".format(urgent_stop.__qualname__, HANDLE[ret_w])
                print_fun(message)
                log_file(message, server=1)

                if ret_s == 'FUSNEFP':
                    message = "Call %s" % send_work.__qualname__
                    print_fun(message)
                    log_file(message, server=1)
                    send_work(sock, city, 5)
                else:
                    message = "Call %s" % send_work.__qualname__
                    print_fun(message)
                    log_file(message, server=1)
                    send_work(sock, city, 1)

                    message = "Call %s" % send_work.__qualname__
                    print_fun(message)
                    log_file(message, server=1)
                    send_work(sock, city, 5)
            else:
                message = "Call %s" % delete_all_us.__qualname__
                print_fun(message)
                log_file(message, server=1)
                delete_all_us(servers_info[server][3], city)  # new test it !!!

                message = "Call %s" % send_us.__qualname__
                print_fun(message)
                log_file(message, server=1)
                send_us(city, server)  # S-server has some work -> stop it


def send_us(city, server):
    message = "From {0}: city = {1}, server = {2}".format(send_us.__qualname__,
                                                          city, server)
    print_fun(message)
    log_file(message, server=1)

    sock = servers_info[server][0]
    city = str(city)
    flag = 'STOP'
    msg = (city + ',' + flag).encode('utf-8')

    try:
        sock.send(msg)
    except:
        message = "From {0}: Can't send US for S-server".format(send_us.__qualname__)
        print_fun(message)
        log_file(message, server=1)
        try:
            message = "From {0}: Remove from dict {1}".format(send_us.__qualname__, server)
            print_fun(message)
            log_file(message, server=1)
            del servers_info[server]
        except:
            message = "From {0}: Can't delete server from dict".format(send_us.__qualname__)
            print_fun(message)
            log_file(message, server=1)

        sock.close()
        readsocks.remove(sock)
        return

    message = "From {0}: Sent US({1}) for server {2}".format(
        send_us.__qualname__, msg.decode('utf-8'), server)
    print_fun(message)
    log_file(message, server=1)


def show_structure(cities):
    for k in cities.keys():
        print_fun(k, ":", cities[k])
    print_fun()


def thread_connection(sock, data):
    message = "From {0}".format(thread_connection.__qualname__)
    print_fun(message)
    log_file(message, server=1)

    data = data.decode('utf-8')
    ip = str(sock.getpeername()[0])

    message = "From {0}: data = {1}; ip = {2}".format(thread_connection.__qualname__,
                                                      data, ip)
    print_fun(message)
    log_file(message, server=1)

    if ip in servers_admin:
        message = "Call %s" % msg_admin.__qualname__
        print_fun(message)
        log_file(message, server=1)
        ret = msg_admin(data)

        message = "Returned from {0}: ret = {1}".format(msg_admin.__qualname__, ret)
        print_fun(message)
        log_file(message, server=1)

        if ret == -1:
            message = "From {0}: Incorrect message from admin-server".format(thread_connection.__qualname__)
            print_fun(message)
            log_file(message, server=1)
            return
        else:
            ip = ret[0]
            data = ret[1]

            if ip in servers_info:
                message = "Call %s" % delete_value.__qualname__
                print_fun(message)
                log_file(message, server=1)
                delete_value(servers_info[ip][3], data)

                servers_info[ip][1] += 1

                if servers_info[ip][1] > HMFPEX:
                    message = "From {0}: Processes are more than {1} for ip {2}".format(
                        thread_connection.__qualname__, HMFPEX, ip)
                    print_fun(message)
                    log_file(message, server=1)
                    servers_info[ip][1] = HMFPEX

                message = "From {0}: new hmp = {1}".format(thread_connection.__qualname__,
                                                           servers_info[ip][1])
                print_fun(message)
                log_file(message, server=1)

            else:
                message = "From {0}: Incorrect IP from admin-server".format(thread_connection.__qualname__)
                print_fun(message)
                log_file(message, server=1)

        return

    if not servers_info[ip][2]:  # not authorized
        if data == psd_server:  # password for authorization
            servers_info[ip][2] = True
            message = "From {0}: Server ({1}) successfully logged in".format(
                thread_connection.__qualname__, ip)
            print_fun(message)
            log_file(message, server=1)

        elif data == psd_admin:  # password for admin server
            message = "From {0}: Server ({1}) logged in as admin".format(
                thread_connection.__qualname__, ip)
            print_fun(message)
            log_file(message, server=1)

            # add to admin dict
            message = "From {0}: Add ({1}) to admin dict".format(
                thread_connection.__qualname__, ip)
            print_fun(message)
            log_file(message, server=1)
            servers_admin.append(ip)

            # delete from user dict
            try:
                message = "From {0}: Remove ({1}) from user dict".format(
                    thread_connection.__qualname__, ip)
                print_fun(message)
                log_file(message, server=1)
                del servers_info[ip]

            except:
                message = "From {0}: Can't delete ({1}) from user dict".format(
                    thread_connection.__qualname__, ip)
                print_fun(message)
                log_file(message, server=1)

        else:  # delete socket from dict, close socket and delete from awaiting list
            message = "From {0}: Server ({1}) sent incorrect password".format(
                thread_connection.__qualname__, ip)
            print_fun(message)
            log_file(message, server=1)

            try:
                message = "From {0}: Remove ({1}) from dict".format(
                    thread_connection.__qualname__, ip)
                print_fun(message)
                log_file(message, server=1)
                del servers_info[ip]

            except:
                message = "From {0}: Can't delete ({1}) from dict".format(
                    thread_connection.__qualname__, ip)
                print_fun(message)
                log_file(message, server=1)

            sock.close()
            readsocks.remove(sock)
            show_structure(servers_info)  # delete

        return

    # when there were no codes
    message = "Call %s" % get_nocode.__qualname__
    print_fun(message)
    log_file(message, server=1)
    ret = get_nocode(data)

    message = "Returned from {0}: ret = {1}".format(get_nocode.__qualname__, ret)
    print_fun(message)
    log_file(message, server=1)

    if ret:
        message = "From {0}: From ip ({1}) got message without codes".format(
            thread_connection.__qualname__, ip)
        print_fun(message)
        log_file(message, server=1)

        if ret != 'NOCODE':
            message = "Call %s" % delete_value.__qualname__
            print_fun(message)
            log_file(message, server=1)
            delete_value(servers_info[ip][3], ret)

        servers_info[ip][1] += 1

        if servers_info[ip][1] > HMFPEX:
            message = "From {0}: Processes are more than {1} for ip {2}".format(
                thread_connection.__qualname__, HMFPEX, ip)
            print_fun(message)
            log_file(message, server=1)
            servers_info[ip][1] = HMFPEX

        message = "From {0}: new hmp = {1}".format(thread_connection.__qualname__,
                                                   servers_info[ip][1])
        print_fun(message)
        log_file(message, server=1)

        return

    # get codes from message
    message = "Call %s" % get_codes.__qualname__
    print_fun(message)
    log_file(message, server=1)
    ret = get_codes(data)

    message = "Returned from {0}: ret = {1}".format(get_codes.__qualname__, ret)
    print_fun(message)
    log_file(message, server=1)

    if len(ret) != 2:
        message = "From {0}: Incorrect len of ret".format(get_codes.__qualname__)
        print_fun(message)
        log_file(message, server=1)
        return
    else:
        city, codes = ret

    code_count = len(codes)
    ip = str(sock.getpeername()[0])

    message = "From {0}: city = {1}; ip = {2}; code count = {3}; codes = {4}".format(
        get_codes.__qualname__, city, ip, code_count, codes)
    print_fun(message)
    log_file(message, server=1)

    # need to delete work from queue
    delete_from_list = str(city) + ',' + str(code_count)
    message = "Call %s" % delete_value.__qualname__
    print_fun(message)
    log_file(message, server=1)
    delete_value(servers_info[ip][3], delete_from_list)

    # need to increase f_processes on S-server
    servers_info[ip][1] += 1
    if servers_info[ip][1] > HMFPEX:
        message = "From {0}: Processes are more than {1} for ip {2}".format(
            thread_connection.__qualname__, HMFPEX, ip)
        print_fun(message)
        log_file(message, server=1)
        servers_info[ip][1] = HMFPEX

    message = "From {0}: new hmp = {1}".format(thread_connection.__qualname__,
                                               servers_info[ip][1])
    print_fun(message)
    log_file(message, server=1)

    # need to add codes to cityN_add.txt
    message = "Call %s" % add_to_afile.__qualname__
    print_fun(message)
    log_file(message, server=1)
    add_to_afile(city, code_count, codes)

    # need to add codes to the structure ???
    # add_to_structure(city, code_count, codes)

    # just for testing
    show_structure(servers_info)
    show_structure(cities)  # latin-1 error ???


def get_nocode(msg):
    message = "From {0}: msg = {1}".format(get_nocode.__qualname__, msg)
    print_fun(message)
    log_file(message, server=1)

    if msg == "NOCODE":
        return 'NOCODE'

    try:
        msg = msg.split(',')
        if len(msg) != 3:
            return 0

        nc, city, count = msg

        if nc != 'NOCODE':
            return 0
        else:
            city = city.lstrip('\n ').rstrip('\n ')
            count = count.lstrip('\n ').rstrip('\n ')

            value = city + ',' + count
            return value
    except:
        return 0


def get_codes(data):
    message = "From {0}: data = {1}".format(get_codes.__qualname__, data)
    print_fun(message)
    log_file(message, server=1)

    codes = []
    try:
        data = data.split('|')
        for code in data:
            if code == '':
                break
            else:
                codes.append(code)

        city = codes[0]
        codes.remove(codes[0])
    except:
        message = "From {0}: Error occurred while trying to get codes".format(get_codes.__qualname__)
        print_fun(message)
        log_file(message, server=1)
        return 0,  # it is error

    return city, codes


def add_to_afile(city, count, codes):
    message = "From {0}: city = {1}, count = {2}, codes = {3}".format(
        add_to_afile.__qualname__, city, count, codes)
    print_fun(message)
    log_file(message, server=1)

    lock.acquire()
    check_th()

    afile = cities[city][8]
    message = "From {0}: add file = {1}".format(add_to_afile.__qualname__, afile)
    print_fun(message)
    log_file(message, server=1)

    file = open(afile, 'a')
    for code in codes:
        msg = code + '\n'
        file.write(msg)
    file.close()

    cities[city][5] += count
    message = "From {0}: new add count = {1}".format(add_to_afile.__qualname__,
                                                     cities[city][5])
    print_fun(message)
    log_file(message, server=1)

    check_th(2)
    lock.release()

    message = "From {0}: To the file {1} were written {2} code(s)".format(
        add_to_afile.__qualname__, afile, count)
    print_fun(message)
    log_file(message, server=1)


def add_to_structure(city, count, codes):  # don't use now
    lock.acquire()
    check_th()
    if not cities[city][7]:
        cities[city][7] = codes
    else:
        for code in codes:
            cities[city][7].append(code)

    cities[city][5] += count
    check_th(2)
    lock.release()


def send_work(sock, city, count):
    message = "From {0}: city = {1}, count = {2}".format(send_work.__qualname__, city,
                                                         count)
    print_fun(message)
    log_file(message, server=1)

    msg = str(city) + "," + str(count)
    add_to_list = msg
    msg = msg.encode('utf-8')
    ip = str(sock.getpeername()[0])
    try:
        sock.send(msg)
    except:
        message = "From {0}: Can't send work for {1}".format(send_work.__qualname__, ip)
        print_fun(message)
        log_file(message, server=1)

        try:
            message = "From {0}: Remove from dict {1}".format(send_work.__qualname__, ip)
            print_fun(message)
            log_file(message, server=1)
            del servers_info[ip]

        except:
            message = "From {0}: Can't remove {1} from dict".format(send_work.__qualname__, ip)
            print_fun(message)
            log_file(message, server=1)

        sock.close()
        readsocks.remove(sock)

    servers_info[ip][1] -= 1  # reduce count of free processes
    message = "From {0}: new hmp = {1}".format(send_work.__qualname__, servers_info[ip][1])
    print_fun(message)
    log_file(message, server=1)

    message = "Call %s" % add_value.__qualname__
    print_fun(message)
    log_file(message, server=1)
    add_value(servers_info[ip][3], add_to_list)  # add work to queue

    message = "From {0}: Sent work ({1}) for {2}".format(
        send_work.__qualname__, msg.decode('utf-8'), ip)
    print_fun(message)
    log_file(message, server=1)


def work_checker(city):  # bot calls this function after client got code
    message = "From {0}: city = {1}".format(work_checker.__qualname__, city)
    print_fun(message)
    log_file(message, server=1)

    lock.acquire()
    check_th()

    max_ac = cities[city][6]
    add_c = cities[city][5]
    message = "From {0}: max_ac = {1}; add_c = {2}".format(work_checker.__qualname__,
                                                           max_ac, add_c)
    print_fun(message)
    log_file(message, server=1)

    if add_c >= max_ac:
        message = "From {0}: There is enough codes for city {1}".format(
            work_checker.__qualname__, cities[city][0])
        print_fun(message)
        log_file(message, server=1)

        check_th(2)
        lock.release()
        return

    check_th(2)
    lock.release()

    message = "Call %s" % choice_server.__qualname__
    print_fun(message)
    log_file(message, server=1)
    server = choice_server()

    message = "Returned from {0}: ret = {1}".format(choice_server.__qualname__, server)
    print_fun(message)
    log_file(message, server=1)

    if server == -1:
        message = "From {0}: There are not connected servers".format(work_checker.__qualname__)
        print_fun(message)
        log_file(message, server=1)
        return

    if server == -2:
        message = "From {0}: There are not free processes on any S-server".format(work_checker.__qualname__)
        print_fun(message)
        log_file(message, server=1)
        return

    # check if I can send work on S-server or not
    message = "Call %s" % hm_work.__qualname__
    print_fun(message)
    log_file(message, server=1)
    ret = hm_work(servers_info[server][3], city)

    message = "Returned from {0}: ret = {1}".format(hm_work.__qualname__, ret)
    print_fun(message)
    log_file(message, server=1)

    if ret == 'FHMWCNS':
        message = "From {0}: {1}".format(work_checker.__qualname__, HANDLE['FHMWCNS'])
        print_fun(message)
        log_file(message, server=1)
        return
    else:
        message = "From {0}: {1}".format(work_checker.__qualname__, HANDLE['FHMWCS'])
        print_fun(message)
        log_file(message, server=1)

    count = str(random.randint(1, 5))
    sock = servers_info[server][0]

    message = "Call %s" % send_work.__qualname__
    print_fun(message)
    log_file(message, server=1)
    send_work(sock, city, count)

    message = "From {0}: Sent work ({1}, {2}) for {3}".format(
        work_checker.__qualname__, count, cities[city][0], server)
    print_fun(message)
    log_file(message, server=1)


def server_make_work():
    global lock
    lock = threading.RLock()

    m_thread = "[main cycle]"

    message = "From {0}: Starting server".format(m_thread)
    print_fun(message)
    log_file(message, server=1)

    sock = socket(AF_INET, SOCK_STREAM)
    message = "From {0}: Socket created".format(m_thread)
    print_fun(message)
    log_file(message, server=1)

    sock.setsockopt(SOCK_STREAM, SO_REUSEADDR, 1)
    sock.bind((ip_server, port_server))
    message = "From {0}: Socket bound on ip {1}, port {2}".format(m_thread, ip_server, port_server)
    print_fun(message)
    log_file(message, server=1)

    sock.listen(5)
    message = "From {0}: Socket is listening...".format(m_thread)
    print_fun(message)
    log_file(message, server=1)

    readsocks.append(sock)
    while True:
        readables, writeables, exceptions = select.select(readsocks, [], [])
        print_fun("READSOCKS:", readsocks)  # delete ?
        for s_sock in readables:
            if s_sock == sock:  # new connection
                newsock, addr = s_sock.accept()
                message = "From {0}: New connection {1}".format(m_thread, addr)
                print_fun(message)
                log_file(message, server=1)

                readsocks.append(newsock)
                servers_info[str(addr[0])] = [newsock, HMFPEX, False, []]  # addr[0] == ip
                print_fun("Servers_info now looks like:")  # delete later ?
                show_structure(servers_info)  # just for testing

            else:  # get data from S-server
                try:  
                    data = s_sock.recv(2048)
                except:
                    message = "From {0}: HARD ERROR -> Connection closed by client".format(m_thread)
                    print_fun(message)
                    log_file(message, server=1)

                    ip = str(s_sock.getpeername()[0])
                    if ip in servers_admin:
                        servers_admin.remove(ip)
                        message = "From {0}: Deleted IP ({1}) from admin-dict".format(m_thread, ip)
                        print_fun(message)
                        log_file(message, server=1)

                        try:
                            s_sock.close()
                            readsocks.remove(s_sock)
                        except:
                            message = "From {0}: Can't delete from list(normal situation)".format(m_thread)
                            print_fun(message)
                            log_file(message, server=1)

                        continue

                    try:
                        message = "From {0}: Remove from dict {1}".format(m_thread, s_sock.getpeername()[0])
                        print_fun(message)
                        log_file(message, server=1)
                        del servers_info[s_sock.getpeername()[0]]
                    except:
                        message = "From {0}: Can't delete {1} from dict".format(m_thread, s_sock.getpeername()[0])
                        print_fun(message)
                        log_file(message, server=1)

                    try:
                        s_sock.close()
                        readsocks.remove(s_sock)
                    except:
                        message = "From {0}: Can't delete from list(normal situation)".format(m_thread)
                        print_fun(message)
                        log_file(message, server=1)

                    continue

                if not data:
                    message = "From {0}: Connection closed by client".format(m_thread)
                    print_fun(message)
                    log_file(message, server=1)

                    ip = str(s_sock.getpeername()[0])
                    if ip in servers_admin:
                        servers_admin.remove(ip)
                        message = "From {0}: Deleted IP ({1}) from admin-dict".format(m_thread, ip)
                        print_fun(message)
                        log_file(message, server=1)

                        try:
                            s_sock.close()
                            readsocks.remove(s_sock)
                        except:
                            message = "From {0}: Can't delete from list(normal situation)".format(m_thread)
                            print_fun(message)
                            log_file(message, server=1)

                        continue

                    try:
                        message = "From {0}: Remove {1} from dict".format(m_thread, s_sock.getpeername()[0])
                        print_fun(message)
                        log_file(message, server=1)
                        del servers_info[s_sock.getpeername()[0]]

                    except:
                        message = "From {0}: Can't delete {1} from dict".format(
                            m_thread, s_sock.getpeername()[0])  # can write it(s_sock.get....) ?
                        print_fun(message)
                        log_file(message, server=1)

                    s_sock.close()
                    readsocks.remove(s_sock)

                else:
                    # create thread to process data
                    message = "From {0}: Call {1}".format(m_thread, thread_connection.__qualname__)
                    print_fun(message)
                    log_file(message, server=1)
                    thread = threading.Thread(target=thread_connection, args=(s_sock, data))
                    thread.start()

