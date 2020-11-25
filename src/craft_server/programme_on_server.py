from socket import *
import time
import os
import signal
import threading
import select
import craft
from log import log_file

ip_server = ''  #'localhost'
port_server = 9816
TTW = 5  # time to wait in seconds -> 30 ?
psd_server = 'NaNgrataTG-t'  # this message is like ACK
f_processes = 5
work_dict = {}
readsocks = []


DEBUG = 1
if DEBUG:
    def print_fun(*string):
        for x in string:
            print(x, end=' ')
        print()
else:
    def print_fun(*string):
        pass


def thread_handler(pid, exit_code):
    message = "From {0}: pid = {1}, exit code = {2}".format(thread_handler.__qualname__,
                                                            pid, exit_code)
    print_fun(message)
    log_file(message)

    global sock

    try:
        pid = str(pid)
        exit_code = int(exit_code)
    except:
        message = "From {0}: Can't cast variables".format(thread_handler.__qualname__)
        print_fun(message)
        log_file(message)
        return

    if exit_code > 0:  # process terminated with error
        message = "From {0}: Process terminated with error".format(thread_handler.__qualname__)
        print_fun(message)
        log_file(message)
        ###########################################
        # Send that there was an error and M-server must count errors for every city.
        # If errors were 2 and more -> make this city unsupported in structure cities
        # When user choose unsupported city from cities, than bot must
        # show message that this city isn't supported and suggest to choose new city
        ###########################################
        # Or better count errors on S-server and send info message to admin.
        # If there were a lof of errors -> admin must make this city unsupported.
        # Or S-server must send structured message to M-server like: 1,UNSUPPORTED
        # than M-server must turn off this city
        ###########################################

        #work_dict.pop(pid, None)
        #return

    file_name = pid + '.txt'
    try:
        file = open(file_name, 'r')
    except:
        message = "From {0}: File ({1}) doesn't exist".format(thread_handler.__qualname__,
                                                              file_name)
        print_fun(message)
        log_file(message)

        error = 0  # flag
        value = work_dict.pop(pid, None)
        # say M-server that 1 process is free
        if value == None:
            message = "There is no such value in dict. Sent to server just NOCODE"
            print_fun(message)
            log_file(message)
            error = 1
        else:
            try:
                city, work = value
                value = str(city) + "," + str(work)
            except:
                message = "Can't cast value from dict"
                print_fun(message)
                log_file(message)
                error = 1

        if error == 0:
            msg = 'NOCODE' + "," + str(value)
        else:
            msg = 'NOCODE'

        msg = msg.encode('utf-8')
        try:
            sock.send(msg)
        except:
            message = "From {0}: Can't send message to M-server".format(thread_handler.__qualname__)
            print_fun(message)
            log_file(message)

        return

    msg = ''
    for code in file:
        code = code.rstrip('\n')
        msg = msg + code + '|'
    file.close()

    msg = msg.encode('utf-8')
    try:
        sock.send(msg)
    except:
        message = "From {0}: Can't send message to M-server".format(thread_handler.__qualname__)
        print_fun(message)
        log_file(message)
        # need to say M-server that process is free. HOW ?

        work_dict.pop(pid, None)
        return

    # delete file and pop value from dict
    try:
        os.remove(file_name)
    except:
        message = "From {0}: Some errors occurred during deleting the file {1}".format(
            thread_handler.__qualname__, file_name)
        print_fun(message)
        log_file(message)

    work_dict.pop(pid, None)

    # just for testing
    message = "From {0}: Now work-dict looks like -> {1}".format(thread_handler.__qualname__,
                                                               work_dict)
    print_fun(message)
    log_file(message)


def signal_handler(signum, frame):
    global f_processes

    try:  # this is unexpected error that I can't fix now, but code is working
        ret = os.waitpid(-1, os.WNOHANG)
    except:
        return
    #print_fun("Process(%s) terminated with EXIT-code: %s" % (ret[0], ret[1]))  # unsafe

    if str(ret[0]) not in work_dict:  # not craft.py
        #print_fun("Process(%s) wasn't craft.py" % str(ret[0]))  # unsafe
        return

    # create new thread to handle file with codes
    thread = threading.Thread(target=thread_handler, args=(ret[0], ret[1]))
    thread.start()

    f_processes += 1  # process ended


def thread_connection(data):
    message = "From {0}".format(thread_connection.__qualname__)
    print_fun(message)
    log_file(message)

    global f_processes

    if f_processes <= 0:  # there aren't now free processes
        message = "From {0}: There aren't free processes".format(thread_connection.__qualname__)
        print_fun(message)
        log_file(message)

        return  # in theory it can't be happen

    message = "Call %s" % check_msg.__qualname__
    print_fun(message)
    log_file(message)
    ret = check_msg(data)

    message = "Returned from {0}: ret = {1}".format(check_msg.__qualname__, ret)
    print_fun(message)
    log_file(message)

    if len(ret) != 2:
        return
    else:
        city, count = ret

    if count == 'STOP':
        message = "From {0}: Received STOP message ({1}, {2})".format(thread_connection.__qualname__,
                                                                      city, count)
        print_fun(message)
        log_file(message)

        message = "Call %s" % urgent_stop.__qualname__
        print_fun(message)
        log_file(message)
        urgent_stop(city)

        return

    message = "From {0}: Work from M-server ({1}, {2})".format(
        thread_connection.__qualname__, city, count)
    print_fun(message)
    log_file(message)

    pid = os.fork()  # now create a new process
    if pid == 0:  # child process
        pid = os.getpid()
        file_name = str(pid) + '.txt'
        message = "From {0}: Child process = {1}".format(thread_connection.__qualname__,
                                                         pid)
        print_fun(message)
        log_file(message)

        message = "Call %s" % craft.craft_f.__qualname__
        print_fun(message)
        log_file(message)
        #print_fun('Parameters: ', city, count, file_name, pid)
        craft.craft_f(city, str(count), file_name, pid)

    work_dict[str(pid)] = city, count  # append to dict for future work
    message = "From {0}: Work dict updated --> {1}".format(
        thread_connection.__qualname__, work_dict)
    print_fun(message)
    log_file(message)

    # parent process
    f_processes -= 1
    message = "From {0}: Free processes now - {1}".format(thread_connection.__qualname__, f_processes)
    print_fun(message)
    log_file(message)


def check_msg(data):
    message = "From {0}".format(check_msg.__qualname__)
    print_fun(message)
    log_file(message)

    data = data.decode('utf-8')
    data = data.split(',')

    try:
        city = data[0]
        flag = data[1].lstrip('\n ').rstrip('\n ')
        if flag == 'STOP':
            message = "From {0}: It's STOP message from M-server -> ({1}, {2})".format(
                check_msg.__qualname__, city, flag)
            print_fun(message)
            log_file(message)

            return city, flag

        else:
            count = int(data[1].lstrip('\n ').rstrip('\n '))
            message = "From {0}: It's WORK message from M-server -> ({1}, {2})".format(
                check_msg.__qualname__, city, count)
            print_fun(message)
            log_file(message)

            return city, count

    except:  # it is just a message from M-server, not a work for S-server
        message = "From {0}: It's just message from M-server --> {1}".format(
            check_msg.__qualname__, data)
        print_fun(message)
        log_file(message)

        return -1


def urgent_stop(city):
    message = "From {0}: city = {1}".format(urgent_stop.__qualname__, city)
    print_fun(message)
    log_file(message)

    city = str(city)
    for k in work_dict.keys():
        if work_dict[k][0] == city:
            pid = int(k)
            try:
                os.kill(pid, 12)  # SIGUSR2
                message = "From {0}: Sent signal ({1}) to pid ({2})".format(urgent_stop.__qualname__,
                                                                            12, pid)
                print_fun(message)
                log_file(message)

            except:
                message = "From {0}: Can't send signal {1} to pid {2}".format(
                    urgent_stop.__qualname__, 12, pid)
                print_fun(message)
                log_file(message)


RET_VALUES = {
    'CNTCONN': "Can't connect to server",
    'CNTSEND': "Can't send message to server",
    'CNTRECV': "Can't receive data from server",
    'DNTADDED': "S-server wasn't added to list on M-server",
    'CONNISST': "Connection is stable",
}


signal.signal(signal.SIGCHLD, signal_handler)


def connect_to_server(ip=ip_server, port=port_server):
    message = "From {0}: ip = {1}, port = {2}".format(
        connect_to_server.__qualname__, ip, port)
    print_fun(message)
    log_file(message)

    while True:
        sock = socket(AF_INET, SOCK_STREAM)  # create TCP
        message = "From {0}: Socket created".format(connect_to_server.__qualname__)
        print_fun(message)
        log_file(message)

        try:
            sock.connect((ip, port))
        except:
            message = "From {0}: Can't connect to server".format(connect_to_server.__qualname__)
            print_fun(message)
            log_file(message)
            sock.close()
            time.sleep(TTW)
            continue

        message = "From {0}: Connected to server".format(connect_to_server.__qualname__)
        print_fun(message)
        log_file(message)

        # send to M-server password
        msg = psd_server.encode('utf-8')
        try:
            sock.send(msg)
        except:
            message = "From {0}: Can't send password to M-server".format(
                connect_to_server.__qualname__)
            print_fun(message)
            log_file(message)
            sock.close()
            time.sleep(TTW)
            continue

        message = "From {0}: Sent password to M-server".format(
            connect_to_server.__qualname__)
        print_fun(message)
        log_file(message)

        readsocks.append(sock)
        return sock  # return socket for future work


sock = connect_to_server()
m_thread = "[main cycle]"

while True:
    readables, writeables, exceptions = select.select(readsocks, [], [])
    # get data from M-server
    for s_sock in readables:
        try:
            data = s_sock.recv(2048)
        except:
            message = "From {0}: Connection with M-server hard refused".format(m_thread)
            print_fun(message)
            log_file(message)

            try:
                s_sock.close()
                readsocks.remove(s_sock)
            except:
                message = "From {0}: Can't remove server from list(it is Ok)".format(m_thread)
                print_fun(message)
                log_file(message)

            message = "Call %s" % connect_to_server.__qualname__
            print_fun(message)
            log_file(message)

            #global sock
            sock = connect_to_server()

            continue

            #try:
                #s_sock.close()
                #readsocks.remove(s_sock)
            #except:
                #print_fun("Can't remove M-server from list(it is Ok)")

            #s_sock = connect_to_server()
            #sock = connect_to_server()
            #continue

        if not data:
            message = "From {0}: Connection closed".format(m_thread)
            print_fun(message)
            log_file(message)

            s_sock.close()  # add try : except ???
            readsocks.remove(s_sock)
            #s_sock = connect_to_server()

            message = "Call %s" % connect_to_server.__qualname__
            print_fun(message)
            log_file(message)

            #global sock
            sock = connect_to_server()

        else:
            # create thread to process data
            message = "Call %s" % thread_connection.__qualname__
            print_fun(message)
            log_file(message)

            thread = threading.Thread(target=thread_connection, args=(data,))
            thread.start()
