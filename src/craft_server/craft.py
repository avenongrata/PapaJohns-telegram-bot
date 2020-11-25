from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import sys
import data_generator
import temp_mail
import time
import signal
import random
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

# change it later
profile_path = r""
wait_sec = [1, 2, 3]
stop_cycle = 0
craft_error = 0
generated_codes = []
pid = 'ND'

city = False
count_codes = False
file_name = False


def signal_handler(signum, frame):
    # print_fun("From signal handler, signum = ", signum)  # it is unsafe
    if signum == signal.SIGUSR2:
        global stop_cycle
        stop_cycle = 1


signal.signal(signal.SIGUSR2, signal_handler)

cities = {
    '1': 'https://www.papajohns.ru/30off',
    '2': 'https://www.papajohns.ru/promo/angarsk/30/',
    '3': 'https://www.papajohns.ru/promo/ekb/30/',
    #'4': 'https://kostroma.papajohns.ru/30off',
    #'5': 'https://nizhnevartovsk.papajohns.ru/30off',
    #'6': 'https://nvkz.papajohns.ru/30off',
    '4': 'https://nn.papajohns.ru/30off',
    #'8': 'https://obninsk.papajohns.ru/30off',
    #'9': 'https://pskov.papajohns.ru/30off',
    #'10': 'https://ryazan.papajohns.ru/30off',
    #'11': 'https://surgut.papajohns.ru/promo30',
    '5': 'https://spb.papajohns.ru/30off',
    #'13': 'https://www.papajohns.ru/30off',
    '6': 'https://www.papajohns.ru/promo/tomsk/30/',
    '7': 'https://tver.papajohns.ru/30off',
    '8': 'https://tyumen.papajohns.ru/promo/tyumen/30OFF/',
    #'17': 'https://tambov.papajohns.ru/30off'
}


def add_to_file(file_name, code):
    message = "From {0}: file name = {1}, code = {2}".format(add_to_file.__qualname__,
                                                             file_name, code)
    print_fun(message)
    log_file(message)

    try:
        with open(file_name, 'r+') as file:
            for _ in file:  # need to add to the end of file
                pass
            dump_msg = code + '\n'
            file.write(dump_msg)
        message = "From {0}: Dumped code ({1}) to file ({2})".format(add_to_file.__qualname__,
                                                                     code, file_name)
        print_fun(message)
        log_file(message)
    except:
        message = "From {0}: File {1} doesn't exist -> create new file {2}".format(
            add_to_file.__qualname__, file_name, file_name)
        print_fun(message)
        log_file(message)

        with open(file_name, 'w') as file:
            dump_msg = str(city) + '\n' + str(code) + '\n'
            file.write(dump_msg)

        message = "From {0}: Dumped code ({1})".format(add_to_file.__qualname__, code)
        print_fun(message)
        log_file(message)


def set_profile_path(new_path):
    message = "From {0}: new path = {1}".format(set_profile_path.__qualname__, new_path)
    print_fun(message)
    log_file(message)

    global profile_path
    profile_path = new_path


def craft_code(name, email, phone, url):  # change to
    message = "From {0}: name = {1}, email = {2}, phone = {3}, url = {4}".format(
        craft_code.__qualname__, name, email, phone, url)
    print_fun(message)
    log_file(message)

    # Also may be add delay before call driver.get() ???

    delay_list = [3, 4, 5]
    time.sleep(random.choice(delay_list))

    stop_error = 0
    global craft_error

    try:
        while True:
            if stop_error > 1:  # only 2 chances
                try:
                    driver.quit()
                except:
                    message = "From {0}: Can't quit from driver".format(craft_code.__qualname__)
                    print_fun(message)
                    log_file(message)

                # global craft_error
                craft_error += 1
                return 1

            try:
                options = Options()
                options.headless = True
                # profile = webdriver.FirefoxProfile(profile_path)
                driver = webdriver.Firefox(options=options)  # f_p = prof
                driver.set_page_load_timeout(15)  # may be 10 ??
            except:
                message = "From {0}: There is some errors in Selenium".format(craft_code.__qualname__)
                print_fun(message)
                log_file(message)

                # global craft_error
                stop_error += 1
                continue

            try:
                driver.get(url)
                break  # break after function call was successful
            except:  # TimeoutException:
                message = "From {0}: Can't get page via Selenium".format(craft_code.__qualname__)
                print_fun(message)
                log_file(message)

                stop_error += 1
                time.sleep(random.choice(delay_list))

        time.sleep(random.choice(wait_sec))

        elem = driver.find_elements_by_css_selector("a.button.next")
        elem[0].click()
        time.sleep(random.choice(wait_sec))

        elem = driver.find_element_by_id('name')
        elem.send_keys(name)
        time.sleep(random.choice(wait_sec))

        elem = driver.find_element_by_id('email')
        elem.send_keys(email)
        time.sleep(random.choice(wait_sec))

        elem = driver.find_element_by_id('phone')
        elem.send_keys(phone)
        time.sleep(random.choice(wait_sec))

        elem = driver.find_elements_by_class_name('custom-checkbox')
        elem[1].click()
        time.sleep(random.choice(wait_sec))

        elem = driver.find_element_by_id('btn-submit')
        elem.click()
        time.sleep(random.choice(wait_sec))

        # check for errors
        try:
            driver.find_element_by_class_name("form-error-msg.is-visible")
            message = "From {0}: Found errors by crafting".format(craft_code.__qualname__)
            print_fun(message)
            log_file(message)
            ret = 1
        except:
            message = "From {0}: Didn't found errors by crafting".format(craft_code.__qualname__)
            print_fun(message)
            log_file(message)
            ret = 0

        driver.quit()

    except:
        message = "From {0}: There is some errors in Selenium".format(craft_code.__qualname__)
        print_fun(message)
        log_file(message)

        # global craft_error
        craft_error += 1
        return 1

    return ret


def craft_f(city_f, count_f, file_name_f, pid_f):
    message = "From {0}: city_f = {1}, count_f = {2}, file_name_f = {3}, pid_f = {4}".format(
        craft_f.__qualname__, city_f, count_f, file_name_f, pid_f)
    print_fun(message)
    log_file(message)

    global city
    global count_codes
    global file_name
    global pid

    pid = pid_f
    city = str(city_f)
    count_codes = int(count_f)
    file_name = str(file_name_f)

    critical_errors = 0
    all_errors = 0
    cycle_iteration = 0
    id = 100  # to avoid error

    if city not in cities:
        message = "From {0}: Incorrect city ({1})".format(craft_f.__qualname__, city)
        print_fun(message)
        log_file(message)
        sys.exit(1)  # terminate with error

    if count_codes // 5 == 0:
        min_cycle_iteration = count_codes + 1
    else:
        min_cycle_iteration = count_codes + count_codes // 5

    while True:
        if stop_cycle == 1:
            message = "From {0}: Stopped cycle due to signal".format(craft_f.__qualname__)
            print_fun(message)
            log_file(message)
            break

        if craft_error > 1:
            message = "From {0}: Found more craft_error than expected".format(craft_f.__qualname__)
            print_fun(message)
            log_file(message)
            break

        if count_codes <= 0:  # we have done work
            break

        if critical_errors > 1:
            if generated_codes:
                message = "From {0}: There were critical errors, but crafted codes also were".format(
                    craft_f.__qualname__)
                print_fun(message)
                log_file(message)
                break

            else:
                message = "From {0}: There were critical errors without crafted codes".format(
                    craft_f.__qualname__)
                print_fun(message)
                log_file(message)
                break

        # count all_errors / cycle_iteration
        if cycle_iteration >= min_cycle_iteration:  # when we did already min iterations
            percent = all_errors / cycle_iteration
            if percent >= 0.6:
                message = "From {0}: Percent of errors is more then 60% and equals {1}%".format(
                    craft_f.__qualname__, int(percent * 100))
                print_fun(message)
                log_file(message)
                break

        cycle_iteration += 1

        message = "Call %s" % data_generator.email_gen.__qualname__
        print_fun(message)
        log_file(message)
        email_name = data_generator.email_gen()

        message = "Returned from {0}: ret = {1}".format(data_generator.email_gen.__qualname__,
                                                        email_name)
        print_fun(message)
        log_file(message)

        # try to create email
        message = "Call %s" % temp_mail.create_email.__qualname__
        print_fun(message)
        log_file(message)
        ret = temp_mail.create_email(email_name, pid)

        message = "Returned from {0}: ret = {1}".format(temp_mail.create_email.__qualname__,
                                                        ret)
        print_fun(message)
        log_file(message)

        if len(ret) != 2:  # error returned
            if ret in temp_mail.RET_VALUES:
                message = "From {0}: {1}".format(craft_f.__qualname__, temp_mail.RET_VALUES[ret])
                print_fun(message)
                log_file(message)

                critical_errors += 1
                all_errors += 1
                continue

        # get email name and key
        email, key = ret

        # get values for craft function
        url = cities[city]

        message = "Call %s" % data_generator.name_gen.__qualname__
        print_fun(message)
        log_file(message)
        name = data_generator.name_gen()

        message = "Returned from {0}: ret = {1}".format(data_generator.name_gen.__qualname__,
                                                        name)
        print_fun(message)
        log_file(message)

        message = "Call %s" % data_generator.phone_gen.__qualname__
        print_fun(message)
        log_file(message)
        phone = data_generator.phone_gen()

        message = "Returned from {0}: ret = {1}".format(data_generator.phone_gen.__qualname__,
                                                        phone)
        print_fun(message)
        log_file(message)

        message = "Call %s" % craft_code.__qualname__
        print_fun(message)
        log_file(message)
        ret = craft_code(name, email, phone, url)

        message = "Returned from {0}: ret = {1}".format(craft_code.__qualname__, ret)
        print_fun(message)
        log_file(message)

        if ret:  # there was an error
            message = "Call %s" % temp_mail.delete_email.__qualname__
            print_fun(message)
            log_file(message)
            temp_mail.delete_email(key)

            all_errors += 1
            continue  # delete email and start from beginning

        flag_repeat = 0
        flag_ltn = 0
        ttw = 10  # this time we will wait
        wait_time = 0
        time.sleep(ttw * 2)  # wait a lot of time until get message id
        while True:
            if wait_time >= 60:  # a lot time of waiting
                #flag_repeat = 1
                flag_ltn = 1  # we can wait a lot of time -> don't need it -> stop crafting
                break

            message = "Call %s" % temp_mail.get_message_id.__qualname__
            print_fun(message)
            log_file(message)
            ret = temp_mail.get_message_id(key)

            message = "Returned from {0}: ret = {1}".format(
                temp_mail.get_message_id.__qualname__, ret)
            print_fun(message)
            log_file(message)

            if ret in temp_mail.RET_VALUES:
                if ret == 'MISERROR':  # need go to the beginning
                    message = "From {0}: {1}".format(craft_f.__qualname__,
                                                     temp_mail.RET_VALUES[ret])
                    print_fun(message)
                    log_file(message)

                    flag_repeat = 1
                    critical_errors += 1
                    break

                if ret == 'LTN' or ret == 'TMERROR':
                    message = "From {0}: {1}".format(craft_f.__qualname__,
                                                     temp_mail.RET_VALUES[ret])
                    print_fun(message)
                    log_file(message)

                    time.sleep(ttw)
                    wait_time += ttw
                    continue

            else:
                id = ret  # when it is not an error
                break

        if flag_ltn:
            message = "Call %s" % temp_mail.delete_email.__qualname__
            print_fun(message)
            log_file(message)
            temp_mail.delete_email(key)

            break  # stop carfting cuz can wait 5 minutes 4.e.
            # NEED ALSO SAY TO ADMIN THAT PJ HAS DELAY ON PROMOCODES !!!! v.2

        if flag_repeat:  # was critical error, need go to the beginning
            message = "Call %s" % temp_mail.delete_email.__qualname__
            print_fun(message)
            log_file(message)
            temp_mail.delete_email(key)

            all_errors += 1
            continue

        message = "Call %s" % temp_mail.get_promocode.__qualname__
        print_fun(message)
        log_file(message)
        ret = temp_mail.get_promocode(key, id)

        message = "Returned from {0}: ret = {1}".format(
            temp_mail.get_promocode.__qualname__, ret)
        print_fun(message)
        log_file(message)

        if ret in temp_mail.RET_VALUES:
            if ret == 'WRONGTEMPLATE':
                # it is very bad situation
                message = "From {0}: {1}".format(craft_f.__qualname__,
                                                 temp_mail.RET_VALUES[ret])
                print_fun(message)
                log_file(message)

                message = "Call %s" % temp_mail.delete_email.__qualname__
                print_fun(message)
                log_file(message)
                temp_mail.delete_email(key)

                critical_errors += 1
                all_errors += 1
                continue

        else:  # it is a promocode
            code = str(ret)
            message = "From {0}: code = {1}".format(craft_f.__qualname__, code)
            print_fun(message)
            log_file(message)
            generated_codes.append(code)

            message = "Call %s" % add_to_file.__qualname__
            print_fun(message)
            log_file(message)
            add_to_file(file_name, code)

        # all is fine
        message = "Call %s" % temp_mail.delete_email.__qualname__
        print_fun(message)
        log_file(message)
        temp_mail.delete_email(key)

        count_codes -= 1

    if not generated_codes:
        message = "From {0}: Something went wrong, no one code was crafted".format(
            craft_f.__qualname__)
        print_fun(message)
        log_file(message)
        sys.exit(1)

    # dumped all crafted code
    if count_codes <= 0:
        message = "From {0}: Hole work has been done".format(craft_f.__qualname__)
        print_fun(message)
        log_file(message)
    else:
        message = "From {0}: Not hole work has been done".format(craft_f.__qualname__)
        print_fun(message)
        log_file(message)

    # just terminate with exit(0), parent process will see it and handle
    sys.exit(0)