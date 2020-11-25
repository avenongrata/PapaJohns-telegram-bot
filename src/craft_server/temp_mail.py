import requests
import json
from log import log_file


DEBUG = 1
if DEBUG:
    def print_fun(*string):
        print(str(pid) + ' > ', end='')
        for x in string:
            print(x, end=' ')
        print()
else:
    def print_fun(*string):
        pass

pid = 'ND'

RET_VALUES = {
    'UNEXERROR': 'Unexpected error',
    'TMERROR': 'Error returned from site',
    'MISERROR': 'There is no such value in dictionary',
    'LTN': 'Values are less than necessary',
    'WRONGTEMPLATE': "Can't find code in html-text"
}


def create_email(name, pid_f):
    message = "From {0}: name = {1}, pid_f = {2}".format(create_email.__qualname__,
                                                         name, pid_f)
    print_fun(message)
    log_file(message)

    global pid
    pid = pid_f

    url = 'https://post-shift.ru/api.php?action=new&name=' + name + '&type=json'
    response = requests.get(url)  # in version 2 must be alone ???
    data = response.text
    d_resp = json.loads(data)

    if 'error' in d_resp:  # there was a error on site
        message = "From {0}: {1}".format(create_email.__qualname__, RET_VALUES['TMERROR'])
        print_fun(message)
        log_file(message)

        return 'TMERROR'

    try:
        email = d_resp['email']
        key = d_resp['key']
    except:
        message = "From {0}: {1}".format(create_email.__qualname__, RET_VALUES['MISERROR'])
        print_fun(message)
        log_file(message)
        return 'MISERROR'

    message = "From {0}: Email created".format(create_email.__qualname__)
    print_fun(message)
    log_file(message)

    return email, key


def get_message_id(key):  # may rewrite in 2 messages
    message = "From {0}: key = {1}".format(get_message_id.__qualname__, key)
    print_fun(message)
    log_file(message)

    url = 'https://post-shift.ru/api.php?action=getlist&key=' + key + '&type=json'
    response = requests.get(url)  # in version 2 must be alone ???
    data = response.text
    d_resp = json.loads(data)

    if 'error' in d_resp:  # work with list or dict ?
        message = "From {0}: {1}".format(get_message_id.__qualname__, RET_VALUES['TMERROR'])
        print_fun(message)
        log_file(message)

        return 'TMERROR'

    if len(d_resp) < 2:
        message = "From {0}: {1}".format(get_message_id.__qualname__, RET_VALUES['LTN'])
        print_fun(message)
        log_file(message)

        return 'LTN'

    msg = '30'
    for d_msg in d_resp:  # get promocode message
        try:
            msg_subj_str = d_msg['subject']
        except:
            message = "From {0}: {1}".format(get_message_id.__qualname__, RET_VALUES['MISERROR'])
            print_fun(message)
            log_file(message)

            return 'MISERROR'

        if msg not in msg_subj_str:
            continue

        # when we found a promocode message
        try:
            id = d_msg['id']
        except:
            message = "From {0}: {1}".format(get_message_id.__qualname__, RET_VALUES['MISERROR'])
            print_fun(message)
            log_file(message)

            return 'MISERROR'

        return id  # will return id of message


def get_promocode(key, id):
    message = "From {0}: key = {1}, id = {2}".format(get_promocode.__qualname__, key, id)
    print_fun(message)
    log_file(message)

    url = 'https://post-shift.ru/api.php?action=getmail&key=' + key + '&id=' + str(id)
    response = requests.get(url)
    text = response.text
    # add error handle if if doesn't exist ?

    index = text.rfind('font-size: 36px')
    if index != -1:
        message = "From {0}: With space".format(get_promocode.__qualname__)
        print_fun(message)
        log_file(message)

        codestring = text[index:index+100]

    else:
        index = text.rfind('font-size:36px')
        if index != -1:
            message = "From {0}: Without space".format(get_promocode.__qualname__)
            print_fun(message)
            log_file(message)

            codestring = text[index:index+100]

        else:
            message = "From {0}: No matches".format(get_promocode.__qualname__)
            print_fun(message)
            log_file(message)

            return 'WRONGTEMPLATE'

    code = codestring.split('</')
    index = code[0].rfind('>')
    if index == -1:
        message = "From {0}: {1}".format(get_promocode.__qualname__, RET_VALUES['WRONGTEMPLATE'])
        print_fun(message)
        log_file(message)

        return 'WRONGTEMPLATE'

    code = code[0][index+1:]
    code = code.lstrip().rstrip()

    message = "From {0}: code = {1}".format(get_promocode.__qualname__, code)
    print_fun(message)
    log_file(message)

    return code


def delete_email(key):
    message = "From {0}: key = {1}".format(delete_email.__qualname__, key)
    print_fun(message)
    log_file(message)

    url = 'https://post-shift.ru/api.php?action=delete&key=' + key
    requests.get(url)

    message = "From {0}: Email deleted".format(delete_email.__qualname__)
    print_fun(message)
    log_file(message)


