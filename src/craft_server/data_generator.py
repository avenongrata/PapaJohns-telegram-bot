import random
import datetime
from log import log_file
import os

operators = [
    '900', '901', '902', '903', '904', '905', '906', '908', '909',
    '910', '911', '912', '913', '914', '915', '916', '917', '918', '919',
    '920', '921', '922', '923', '924', '925', '926', '927', '928', '929',
    '930', '931', '932', '933', '934', '936', '937', '938', '939',
    '950', '951', '952', '953', '954', '955', '956', '958',
    '960', '961', '962', '963', '964', '965', '966', '967', '968', '969',
    '980', '981', '982', '983', '984', '985', '986', '987', '988', '989',
    '991', '992', '993', '994', '995', '996', '997', '999'
]

names = [
    'Alexander', 'Alexey', 'Anatoly', 'Andrei', 'Anton',
    'Arkady', 'Artyom', 'Borislav', 'Vadim', 'Valentine',
    'Valery', 'Basil', 'Victor', 'Vitaliy', 'Vladimir',
    'Vyacheslav', 'Gennady', 'George', 'Gregory', 'Daniel',
    'Denis', 'Dmitriy', 'Evgeniy', 'Egor', 'Ivan',
    'Igor', 'Ilya', 'Kirill', 'Maksim', 'Michael',
    'Nikita', 'Nikolay', 'Oleg', 'Semen', 'Sergey',
    'Stanislav', 'Stepan', 'Fedor', 'Yuri', 'Alexandra',
    'Alina', 'Alla', 'Anastasia', 'Angela', 'Anna',
    'Antonina', 'Valentine', 'Valeria', 'Veronica', 'Victoria',
    'Galina', 'Daria', 'Eugene', 'Catherine', 'Helena',
    'Elizabeth', 'Karina', 'Kira', 'Claudia', 'Kristina',
    'Ksenia', 'Lydia', 'Lyudmila', 'Margarita', 'Marina',
    'Maria', 'Natalya', 'Nina', 'Oksana', 'Olesya',
    'Olga', 'Pauline', 'Svetlana', 'Taisiya', 'Tamara',
    'Tatyana', 'Evelina', 'Elvira', 'Juliana', 'Yulia',
    'Jana'
]

email_string = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

"""
I added random.seed(...) in every function to avoid
the same values.
"""


DEBUG = 1
if DEBUG:
    def print_fun(*string):
        pid = os.getpid()
        print(str(pid) + ' > ', end='')
        for x in string:
            print(x, end=' ')
        print()
else:
    def print_fun(*string):
        pass


def phone_gen():
    message = "From {0}".format(phone_gen.__qualname__)
    print_fun(message)
    log_file(message)

    random.seed(datetime.datetime.now())  # somewhere needs it, somewhere not
    number = random.choice(operators)
    number += str(random.randint(1000000, 9999999))
    return number


def name_gen():
    message = "From {0}".format(name_gen.__qualname__)
    print_fun(message)
    log_file(message)

    random.seed(datetime.datetime.now())  # somewhere needs it, somewhere not
    name = random.choice(names)
    return name


def email_gen():
    message = "From {0}".format(email_gen.__qualname__)
    print_fun(message)
    log_file(message)

    email = ''
    for x in range(10):
        random.seed(datetime.datetime.now())  # somewhere needs it, somewhere not
        email += random.choice(email_string)

    return email


