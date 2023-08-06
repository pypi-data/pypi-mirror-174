#!/usr/bin/env python3
"""
    Interacts with MegaFon
"""

from pprint import pprint
import logging

from . import balance
from . import credentials

def main(login=None, password=None, command=None, debug=False):

    if debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    
    logging.basicConfig(level=loglevel)
    logging.debug("Validating credentials..")

    if not login or not password:
        env_credentials = credentials.get_from_env()
        login = env_credentials['login']
        password = env_credentials['password']

    logging.debug("Uniforming login")
    uniformed_login = credentials.uniform_login(login)
    logging.debug("Login: '%s' -> '%s'" % (login, uniformed_login) )

    connection = balance.APIConnection(login=uniformed_login, password=password)

    if command == 'do_check_balance':
        logging.debug("Check balance command invoked")
        connection.sign_in()
        connection.get_balance()

    elif command == 'do_check_remainings':
        logging.debug("Check option remainings command invoked")
        connection.sign_in()
        result = connection.get_all_remainings()
        print(result.decode())


    elif command == 'do_list_options':
        logging.debug("List options command invoked")
        connection.sign_in()
        connection.list_subscriptions()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.error("Not implemented.")
