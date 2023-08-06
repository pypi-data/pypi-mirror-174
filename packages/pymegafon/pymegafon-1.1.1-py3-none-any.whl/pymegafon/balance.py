#!/usr/bin/env python3
"""
    Signs in, retrieves balance information, returns a json structure.
"""

import http.cookiejar
import json
import urllib
import time
import re
import os
import logging
from pprint import pprint

from . import common

class APIConnection():

    def __init__(self, login, password):
        self.login = login
        self.password = password
        
        self.cookiejar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
        self.csrf = None
        self.balance = None
        self.internet_remainings = None
        self.options = None

        self.lk_start_url = common.LK_START_URL
        self.lk_login_url = common.LK_LOGIN_URL
        self.get_balance_url = common.API_GET_BALANCE_URL
        self.get_internet_reiminigs_url = common.API_GET_INTERNET_REMININGS_URL

    def get_cookie(self, requested_cookie_name):
        logging.debug("Looking for a cookie named '%s'" % requested_cookie_name) 
        
        for cookie in self.cookiejar:
            if cookie.name == requested_cookie_name:
                logging.debug("Found cookie '%s': %s" % (requested_cookie_name, cookie))
                return cookie

    def start(self):
        logging.debug("Enter URL: '%s'" % (self.lk_start_url))
        response = self.opener.open(self.lk_start_url)
        self.csrf = self.get_cookie("CSRF-TOKEN")

        if not self.csrf:
            raise Exception("Couldn't get initial CSRF token.")

    def do_login(self):
        params = {
            "CSRF": self.csrf,
            "j_username": self.login,
            "j_password": self.password,
        }

        data = urllib.parse.urlencode(params).encode('utf-8')
        response = self.opener.open(self.lk_login_url, data=data)

    def sign_in(self):
        logging.info("Signing in...")

        self.start()
        self.do_login()

    def get_balance(self):
        if not self.csrf:
            raise Exception("Not signed in!")

        params = {
            "CSRF": self.csrf
        }

        response = self.opener.open("%s?%s" % (self.get_balance_url, urllib.parse.urlencode(params)))
        balance = json.loads(response.read())

        self.balance = balance['balance']
        logging.info("Balance: %s" % self.balance)
        
        return self.balance

    def list_options(self):
        if not self.csrf:
            raise Exception("Not signed in!")

        params = {
            "CSRF": self.csrf
        }

        response = self.opener.open("%s?%s" % (self.get_internet_reiminigs_url, urllib.parse.urlencode(params)))
        self.options = json.loads(response.read())
        logging.info("Internet: %s" % self.options)
        pprint(self.options)
        print(response.read())


    def get_all_remainings(self):
        if not self.csrf:
            raise Exception("Not signed in!")

        params = {
            "CSRF": self.csrf
        }

        logging.info("Requesting remainings from API...")

        response = self.opener.open("%s?%s" % (self.get_internet_reiminigs_url, urllib.parse.urlencode(params)))
        self.internet_remainings = json.loads(response.read())
        logging.debug("Remainings: %s" % self.internet_remainings)
        
        return json.dumps(self._process_remainings(), ensure_ascii=False).encode('utf8')

    def _process_remainings(self):
        remainings_dict = {}
        option_fields = [
            "name",
            "totalValue",
            "totalValueUnit",
            "availableValue",
            "availableValueUnit",
            "optionId",
            "monthly",
            "groupId",
            "validUntilDate",
        ]

        logging.debug("Remaining keys: %s" % (self.internet_remainings.keys()))
        for remainder_item in self.internet_remainings['remainders']:
            for remainder_item_service in remainder_item['remainders']:
                option_renew_date = remainder_item_service['dateTo'].split(" ")[0]
                logging.info("Option: '%s' (Total: %s %s, Available: %s %s) Until: %s" % (remainder_item_service['name'], remainder_item_service['totalValue']['value'], remainder_item_service['totalValue']['unit'], remainder_item_service['availableValue']['value'], remainder_item_service['availableValue']['unit'], option_renew_date))

                remainings_dict[remainder_item_service['name']] = {}
                for field in option_fields:
                    if field in remainder_item_service:
                        remainings_dict[remainder_item_service['name']][field] = remainder_item_service[field]
                    else:
                        remainings_dict[remainder_item_service['name']][field] = None
    
        return remainings_dict
    

    def _get_internet_remainder(self):
        for item in self.internet_remainings['remainders']:
            if item["name"] == "Интернет по России":
                return item['remainders']

    def _get_internet_stat(self):
        for item in self._get_internet_remainder():
            if item["name"] == "Интернет":
                result = {
                    "total": item['totalValue']['value'], 
                    "available": item['availableValue']['value']
                }

                return result

