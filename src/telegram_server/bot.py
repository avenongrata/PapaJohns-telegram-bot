## -*- coding: utf-8 -*-

print('Telegrambot v. 1.2 Wed Jan 8,10:48')

from datetime import datetime
from datetime import timedelta
from log import log_file, code_stat
from log import ERRORS_TG
from log import STATE_TG
from log import save_data
from log import restore_data
import telebot
import sys
import threading
import main_server


TOKEN = ""
bot = telebot.TeleBot(TOKEN)
user_class_dict = {}
account_file = 'account.txt'

RESTORE = 1  # is used to restore data from file
             # data will restore to user_class_dict

DEBUG = 1
if DEBUG:
    def print_fun(*string):
        for x in string:
            print(x, end=' ')
        print()
else:
    def print_fun(*string):
        pass


# we need to start server in thread, so:
def server_starting():
    message = 'Call %s' % server_starting.__qualname__
    print_fun(message)
    log_file(message)
    main_server.server_make_work()


thread = threading.Thread(target=server_starting, args=())
thread.start()


def new_user(user_id, user_dict):  # user_id has type 'str' here
    try:
        with open(account_file, 'r+') as file:
            for _ in file:  # go to the end of file
                pass
            file.write(user_id + '\n')
            user_dict[user_id] = User(user_id)
            message = "Added new user to file %s" % account_file
            print_fun(message, user_id)
            log_file(message, user_id)
    except:
        message = "File doesn't exist. Create new file: %s" % account_file
        print_fun(message)
        log_file(message)
        with open(account_file, 'w') as file:
            file.write(user_id + '\n')
            user_dict[user_id] = User(user_id)
            message = "Added new user to file %s" % account_file
            print_fun(message, user_id)
            log_file(message, user_id)


class User:

    def __init__(self, id, order_count=0, next_time_order=0, city=False, restore=0):
        self.id = id
        self.order_count = order_count
        self.next_time_order = next_time_order
        self.last_time_order = 0
        self.rest_time = False
        self.city = city
        self.lock = threading.RLock()

        if restore:
            # restore flag is used to restore data from file data.txt
            return
        message = 'Call %s' % save_data.__qualname__
        print_fun(message)
        log_file(message)
        ret = save_data(self)
        message = 'Returned from %s: ret = %s' % (save_data.__qualname__, ret)
        print_fun(message, self.id)
        log_file(message, self.id)
        if ret == 'DATA_CHANGED' or ret == 'DATA_ADDED':
            message = "%s: %s" % (STATE_TG[ret], 'data.txt')
        else:
            message = "%s: %s" % (STATE_TG[ret], "user_class_dict")
        print_fun(message)
        log_file(message, id=self.id)

    def order(self):
        self.lock.acquire()
        message = "From %s" % User.order.__qualname__
        print_fun(message, self.id)
        log_file(message, self.id)
        current_time = datetime.now()

        if self.order_count == 0:  # first order
            ret_server = main_server.get_code_file(self.city)
            if ret_server in main_server.RET_VALUES:
                self.lock.release()
                return ret_server
            self.last_time_order = current_time
            self.next_time_order = self.set_next_time_order()
            self.order_count += 1  # for statistics
            message = "Returned true from %s" % User.order.__qualname__
            print_fun(message, self.id)
            log_file(message, self.id)
            message = 'Call %s' % save_data.__qualname__
            print_fun(message)
            log_file(message)
            ret = save_data(self)
            message = 'Returned from %s: ret = %s' % (save_data.__qualname__, ret)
            print_fun(message, self.id)
            log_file(message, self.id)
            if ret == 'DATA_CHANGED' or ret == 'DATA_ADDED':
                message = "%s: %s" % (STATE_TG[ret], 'data.txt')
            else:
                message = "%s: %s" % (STATE_TG[ret], "user_class_dict")
            print_fun(message)
            log_file(message, id=self.id)
            self.lock.release()
            return ret_server  # True -> user can get code
        else:  # user has already ordered
            self.rest_time = self.compare_time(current_time)
            if not self.rest_time:  # user can get code
                ret_server = main_server.get_code_file(self.city)
                if ret_server in main_server.RET_VALUES:
                    self.lock.release()
                    return ret_server
                self.last_time_order = current_time
                self.next_time_order = self.set_next_time_order()
                self.order_count += 1  # for statistics
                message = "Returned true from %s" % User.order.__qualname__
                print_fun(message, self.id)
                log_file(message, self.id)
                message = 'Call %s' % save_data.__qualname__
                print_fun(message)
                log_file(message)
                ret = save_data(self)
                message = 'Returned from %s: ret = %s' % (save_data.__qualname__, ret)
                print_fun(message, self.id)
                log_file(message, self.id)
                if ret == 'DATA_CHANGED' or ret == 'DATA_ADDED':
                    message = "%s: %s" % (STATE_TG[ret], 'data.txt')
                else:
                    message = "%s: %s" % (STATE_TG[ret], "user_class_dict")
                print_fun(message)
                log_file(message, id=self.id)
                self.lock.release()
                return ret_server  # True
            else:
                message = "Returned false from %s" % User.order.__qualname__
                print_fun(message, self.id)
                log_file(message, self.id)
                self.lock.release()
                return False  # user can't get code

    def compare_time(self, current_time):
        message = "From %s" % User.compare_time.__qualname__
        print_fun(message, self.id)
        log_file(message, self.id)
        ret = str(self.next_time_order - current_time)
        if ret[0] == '-' or ret == "0:00:00":
            message = "Returned false from %s" % User.compare_time.__qualname__
            print_fun(message, self.id)
            log_file(message, self.id)
            return False
        else:
            message = "Returned rest time from %s" % User.compare_time.__qualname__
            print_fun(message, self.id)
            log_file(message, self.id)
            ret = ret.split('.')
            return ret[0]

    def set_next_time_order(self, period=1):  # 1 day
        message = "From %s" % User.set_next_time_order.__qualname__
        print_fun(message, self.id)
        log_file(message, self.id)
        ret = self.last_time_order + timedelta(days=0)  # change later =period
        message = "Returned next order %s from %s" % (
            str(ret), User.set_next_time_order.__qualname__)
        print_fun(message, self.id)
        log_file(message, self.id)
        return ret

    def change_city(self, city):
        self.lock.acquire()
        message = "From %s" % User.change_city.__qualname__
        print_fun(message, self.id)
        log_file(message, self.id)
        self.city = city
        message = 'City changed'
        print_fun(message, self.id)
        log_file(message, self.id)

        message = 'Call %s' % save_data.__qualname__
        print_fun(message)
        log_file(message)
        ret = save_data(self)
        message = 'Returned from %s: ret = %s' % (save_data.__qualname__, ret)
        print_fun(message, self.id)
        log_file(message, self.id)
        if ret == 'DATA_CHANGED' or ret == 'DATA_ADDED':
            message = "%s: %s" % (STATE_TG[ret], 'data.txt')
        else:
            message = "%s: %s" % (STATE_TG[ret], "user_class_dict")
        print_fun(message)
        log_file(message, id=self.id)
        self.lock.release()

    def check_city(self):
        print("CUR CITY IS: ", self.city)

    def show_info(self):  # never called this method but someone may be needs it
        print("Account name: %s" % self.id)
        print("Order count: %s" % self.order_count)
        print("Last time order: ", self.last_time_order)
        print("Last time order: ", self.next_time_order)
        print('\n')


if RESTORE:
    message = "Data restore from file data.txt started"
    print_fun(message)
    log_file(message)
    message = 'Call %s' % restore_data.__qualname__
    print_fun(message)
    log_file(message)
    ret, count = restore_data(user_class_dict, User)
    message = 'Returned from %s: ret = %s, count = %d' % (restore_data.__qualname__,
                                                          ret, count)
    print_fun(message)
    log_file(message)
    if ret in ERRORS_TG:
        if ret == 'FILE_DOESNT_EXIST':
            message = "%s: %s" % (ERRORS_TG[ret], 'data.txt')
        else:
            message = ret
        print_fun(message)
        log_file(message)
        message = 'Program terminated with sys.exit(0)'
        print_fun(message)
        log_file(message)
        sys.exit(0)
    elif ret in STATE_TG:
        message = "%s: %s, count = %d" % (STATE_TG[ret], "user_class_dict", count)
        print_fun(message)
        log_file(message)
    else:
        message = "Unknown error: program terminated with sys.exit(1)"
        print_fun(message)
        log_file(message)
        sys.exit(1)

    message = "Data restore from file data.txt ended"
    print_fun(message)
    log_file(message)


@bot.message_handler(commands=['start'])
def start(msg):
    message = "From message_handler(start)"
    print_fun(message, msg.from_user.id)
    log_file(message, msg.from_user.id, 1)
    if msg.chat.type != 'private':
        message = "Chat isn't private"
        print_fun(message, msg.from_user.id)
        log_file(message, msg.from_user.id)
        return

    user_id = msg.from_user.id
    user_id_str = str(user_id)
    if user_id_str in user_class_dict:
        if type(user_class_dict[user_id_str].city) == type(False):
            message = "Call %s" % set_city.__qualname__
            print_fun(message, user_id)
            log_file(message, user_id)
            set_city(msg)
            message = "Returned from %s" % set_city.__qualname__
            print_fun(message, user_id)
            log_file(message, user_id)
            return

        message = "Account already exist"
        print_fun(message, user_id)
        log_file(message, user_id)
        try:
            bot.send_message(user_id, "Бот уже запущен.\nНаберите /code чтобы получить промокод\n"
                                      "Наберите /city чтобы сменить город")
        except:
            message = "User stopped bot"
            print_fun(message, user_id)
            log_file(message, user_id, 2)

        message = 'Sent info text for user after "/start" command'
        print_fun(message, user_id)
        log_file(message, user_id, 2)
        return
    # user isn't in dict, it is new user
    new_user(user_id_str, user_class_dict)
    message = "Call %s" % set_city.__qualname__
    print_fun(message, user_id)
    log_file(message, user_id)
    set_city(msg)
    message = "Returned from %s" % set_city.__qualname__
    print_fun(message, user_id)
    log_file(message, user_id)


@bot.message_handler(commands=['code'])
def code_f(msg):
    message = "From message_handler(code)"
    print_fun(message, msg.from_user.id)
    log_file(message, msg.from_user.id, 1)
    if msg.chat.type != 'private':
        message = "Chat isn't private"
        print_fun(message, msg.from_user.id)
        log_file(message, msg.from_user.id)
        return

    user_id = msg.from_user.id
    user_id_str = str(msg.from_user.id)
    if user_id_str not in user_class_dict:
        message = "User doesn't exist in dictionary"
        print_fun(message, user_id)
        log_file(message, user_id)
        message = 'Наберите /start для запуска бота'
        try:
            bot.send_message(user_id, message)
        except:
            message = "User stopped bot"
            print_fun(message, user_id)
            log_file(message, user_id, 2)

        message = 'Sent info text for user after "/code" command'
        print_fun(message, user_id)
        log_file(message, user_id, 2)
        return

    if type(user_class_dict[user_id_str].city) == type(False):
        message = "Call %s" % set_city.__qualname__
        print_fun(message, user_id)
        log_file(message, user_id)
        set_city(msg)
        message = "Returned from %s" % set_city.__qualname__
        print_fun(message, user_id)
        log_file(message, user_id)
        return

    ret_val = user_class_dict[user_id_str].order()
    if ret_val in main_server.RET_VALUES:
        #bot.send_message(user_id, ret_val)  # send message about waiting if specific error
        try:
            bot.send_message(user_id, "В данный момент нет кодов. Попробуйте позже\n")
        except:
            message = "User stopped bot"
            print_fun(message, user_id)
            log_file(message, user_id, 2)

        message = 'Sent message: There is no codes now. Try later'
        print_fun(message, user_id)
        log_file(message, user_id, 2)
        message = "Call %s" % main_server.urgent_stop.__qualname__
        print_fun(message, user_id)
        log_file(message, user_id)
        main_server.urgent_stop(user_class_dict[user_id_str].city)
    elif not ret_val:
        msg_to_user = 'Следующий промокод через: ' + user_class_dict[user_id_str].rest_time
        try:
            bot.send_message(user_id, msg_to_user)
        except:
            message = "User stopped bot"
            print_fun(message, user_id)
            log_file(message, user_id, 2)

        message = "User got rest of time"
        print_fun(message, user_id_str)
        log_file(message, user_id_str, 2)
    else:
        try:
            bot.send_message(user_id, ret_val)
        except:
            message = "User stopped bot"
            print_fun(message, user_id)
            log_file(message, user_id, 2)

        message = "User got code"
        print_fun(message, user_id_str)
        log_file(message, user_id_str, 2)
        # new !!!!!!!!!!!!!!!!!!
        message = "Call %s" % code_stat.__qualname__
        print_fun(message, user_id)
        log_file(message, user_id)
        code_stat(user_class_dict[user_id_str].city, user_id_str, ret_val)
        message = "Call %s" % main_server.work_checker.__qualname__
        print_fun(message, user_id)
        log_file(message, user_id)
        main_server.work_checker(user_class_dict[user_id_str].city)


@bot.message_handler(commands=['city'])
def set_city(msg):
    message = "From message_handler(set_city)"
    print_fun(message, msg.from_user.id)
    log_file(message, msg.from_user.id, 1)

    if msg.chat.type != 'private':
        message = "Chat isn't private"
        print_fun(message, msg.from_user.id)
        log_file(message, msg.from_user.id)
        return

    user_id = msg.from_user.id
    user_id_str = str(user_id)
    if user_id_str not in user_class_dict:
        message = "User doesn't exist in dictionary"
        print_fun(message, user_id)
        log_file(message, user_id)
        message = 'Наберите /start для запуска бота'
        try:
            bot.send_message(user_id, message)
        except:
            message = "User stopped bot"
            print_fun(message, user_id)
            log_file(message, user_id, 2)

        message = 'Sent info text for user after "/city" command'
        print_fun(message, user_id)
        log_file(message, user_id, 2)
        return

    message = "Выберите ваш город\n" \
              "/1 Москва и мос. область\n" \
              "/2 Екатеринбург\n" \
              "/3 Нижний Новгород\n" \
              "/4 Санкт-Петербург\n" \
              "/5 Тверь\n"
              #"/8 Тюмень\n"
              #"/6 Томск\n" \
              #"/2 Ангарск\n" \
              #"/4 Кострома\n" \
              #"/5 Нижневартовск\n" \
              #"/6 Новокузнецк\n" \
              #"/8 Обнинск\n" \
              #"/9 Псков\n" \
              #"/10 Рязань\n" \
              #"/11 Сургут\n" \
              #"/13 Сочи\n" \
              #"/17 Тамбов\n"

    try:
        bot.send_message(user_id, message)
    except:
        message = "User stopped bot"
        print_fun(message, user_id)
        log_file(message, user_id, 2)

    message = "Sent list of cities for user"
    print_fun(message, user_id)
    log_file(message, user_id, 2)


@bot.message_handler(commands=['1', '2', '3', '4', '5'])
def city(msg):
    if msg.chat.type != 'private':
        message = "Chat isn't private"
        print_fun(message, msg.from_user.id)
        log_file(message, msg.from_user.id)
        return

    user_id = msg.from_user.id
    user_id_str = str(user_id)
    if user_id_str not in user_class_dict:
        message = "User doesn't exist in dictionary"
        print_fun(message, user_id)
        log_file(message, user_id)
        message = 'Наберите /start для запуска бота'
        try:
            bot.send_message(user_id, message)
        except:
            message = "User stopped bot"
            print_fun(message, user_id)
            log_file(message, user_id, 2)

        message = 'Sent info text for user after "/1.../17" commands'
        print_fun(message, user_id)
        log_file(message, user_id, 2)
        return

    city_number = msg.text.split('/')[1]  # get command without '/'
    city = main_server.cities[city_number][0]
    user_class_dict[user_id_str].change_city(city_number)
    message = 'Теперь Ваш город: %s' % city
    try:
        bot.send_message(user_id, message)
    except:
        message = "User stopped bot"
        print_fun(message, user_id)
        log_file(message, user_id, 2)

    message = 'Sent info text about city to user'
    print_fun(message, user_id)
    log_file(message, user_id, 2)

    try:
        bot.send_message(user_id, "Наберите /code чтобы получить промокод\n"
                                  "Наберите /city чтобы сменить город")
    except:
        message = "User stopped bot"
        print_fun(message, user_id)
        log_file(message, user_id, 2)

    message = 'Sent info text for user after "/1.../17" commands'
    print_fun(message, user_id)
    log_file(message, user_id, 2)


@bot.message_handler(content_types=['text', 'document', 'audio'])
def answer_msg(msg):
    message = "From message_handler(answer_msg)"
    print_fun(message, msg.from_user.id)
    log_file(message, msg.from_user.id, 1)

    if msg.chat.type != 'private':
        message = "Chat isn't private"
        print_fun(message, msg.from_user.id)
        log_file(message, msg.from_user.id)
        return

    user_id = msg.from_user.id
    user_id_str = str(user_id)
    if user_id_str not in user_class_dict:
        message = "User doesn't exist in dictionary"
        print_fun(message, user_id)
        log_file(message, user_id)
        message = 'Наберите /start для запуска бота'
        try:
            bot.send_message(user_id, message)
        except:
            message = "User stopped bot"
            print_fun(message, user_id)
            log_file(message, user_id, 2)

        message = 'Sent info text for user after "text, document, audio" content types'
        print_fun(message, user_id)
        log_file(message, user_id, 2)
        return

    if type(user_class_dict[user_id_str].city) == type(False):
        message = "Call %s" % set_city.__qualname__
        print_fun(message, user_id)
        log_file(message, user_id)
        set_city(msg)
        message = "Returned from %s" % set_city.__qualname__
        print_fun(message, user_id)
        log_file(message, user_id)
        return

    message = "Наберите /code чтобы получить промокод\nНаберите /city чтобы сменить город"
    try:
        bot.send_message(user_id, message)
    except:
        message = "User stopped bot"
        print_fun(message, user_id)
        log_file(message, user_id, 2)

    message = "Answered on user message"
    print_fun(message, user_id)
    log_file(message, user_id, 2)


bot.polling()