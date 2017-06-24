import os


def read_env_file():
    with open('../.env', "r") as fp:
        lines = fp.readlines()
        options = {}
        for line in lines:
            line = line.strip()

            # Ignore comments
            if line.startswith('#'):
                continue
            if line == "":
                continue

            name, value = line.split('=', 1)

            # Boolean type
            if value == 'True' or value == 'False':
                value = (value == 'True')

            options[name] = value
    return options


try:
    env_vars = read_env_file()
    print("Environment variables read from file.")
except FileNotFoundError:  # NOQA
    env_vars = os.environ


class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']
    TEST = os.environ['TESTING']
