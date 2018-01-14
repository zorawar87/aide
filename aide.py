#!/usr/bin/python3

"""
this module attempts to scrape and extract user data
from MyTrinNet's data.
@see https://github.com/zorawar87/aide
@see https://medium.com/@zorawar87/scraping-trincolls-alumni-database-c671c8aa09b8
"""

import argparse
import sys
import time
import json
import logging
from splinter import Browser
from bs4 import BeautifulSoup as bs
import coloredlogs as cl

logging.basicConfig(level=logging.INFO)
cl.install()

totalis = []
exceptions = []


def get_args():
    """
    returns command line args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help="your mytrinnet username")
    parser.add_argument('password', help="your mytrinnet password")
    parser.add_argument('ll', type=int, help="lower limit of the iterations")
    parser.add_argument('ul', type=int, help="upper limit of the iterations")
    parser.add_argument(
        '-d',
        '--debug',
        dest='headless',
        action='store_false',
        help="starts in debugging mode (chrome starts in GUI mode)")
    parser.set_defaults(headless=True)
    namespace = parser.parse_args(sys.argv[1:])
    return namespace.username, namespace.password, namespace.ll, namespace.ul, namespace.headless


def aide(uname, pword, lower_lim, upper_lim, hless):
    """
    completes one cycle of aide
    """
    with Browser('chrome', headless=hless) as browser:
        start = time.time()
        logging.info("starting with %s %s %d", uname, pword, lower_lim)
        if not login(browser, uname, pword):
            logging.critical("authentication failed... quitting.")
            return -1

        logging.info("authentication successful!")
        upper_lim = iterate_profiles(browser, lower_lim, upper_lim)
        end = time.time()
        logging.info(
            "Iterating over [%d, %d) took: %f seconds",
            lower_lim, upper_lim, end - start)
        return upper_lim


def login(browser, uname, pword):
    """
    logs a user in
    TODO: account for auth errors
    TODO: use cookies instead?
    """
    logging.info("attempting log in...")
    # i=0
    #url = "https://mytrinnet.trincoll.edu/s/1490/index-3Col.aspx? "\
    #"sid=1490&gid=1&pgid=275&cid=735&mid="+ str(i) +"#/PersonalProfile"
    # browser.visit(url)
    # auth = { "__cfduid":"d5fc047fe12a2b7d8896933f47194ea121515860850",
    #"ENCOMPASSSESSIONID_1490":"2012410b-54e0-4bb1-89aa-f58bb2b5882f",
    #"EncompassAuth":"cwDX50uKtXWslGK_zzphCQ0sy7mrx5fpXL6DNrWOx1lBiFFLj3663qTDM79g" }
    # browser.cookies.add(auth)
    # browser.visit(url)
    scheme = "https:"
    domain = "securelb.imodules.com"
    path = "//" + domain + "/s/1490/index-3Col.aspx"
    query = "?sid=1490&gid=1&pgid=3&cid=40"
    url = scheme + path + query
    browser.visit(url)
    browser.fill('cid_40$txtUsername', uname)
    browser.fill('cid_40$txtPassword', pword)
    browser.find_by_name('cid_40$btnLogin').click()
    time.sleep(2)
    if browser.url.split("//")[1].split("/")[0] == domain:
        return False
    return True


def iterate_profiles(browser, low, high):
    """
    iterates over a range of profiles
    """
    logging.info("iterating profiles from %d to %d...", low, high)
    for i in range(low, high):
        #widgets = [progressbar.Percentage(), progressbar.Bar()]
        #bar = progressbar.ProgressBar(widgets=widgets, min_value=low, max_value=high).start()
        scheme = "https:"
        path = "//mytrinnet.trincoll.edu/s/1490/index-3Col.aspx"
        query = "?sid=1490&gid=1&pgid=275&cid=735&mid=" + str(i)
        fragment = "#/PersonalProfile"
        url = scheme + path + query + fragment
        browser.visit(url)
        time.sleep(0.8)
        if not is_valid_person(high - low, parse_HTML_to_person(i,
                                                                browser.html)):
            logging.critical("breaking at %d", i)
            return i + 1
    log_data()
    return high


def parse_HTML_to_person(mid, html):
    """
    forms a person out of given html
    """
    page = bs(html, 'html.parser')
    person = {}
    person.update({"mid": mid})
    label = ""
    data = ""
    divs = page.find_all("div")
    for div in divs:
        class_attr = div.get('class')
        if class_attr is not None:
            if class_attr[0] == "imod-profile-field-label":
                label = div.string
            elif class_attr[0] == "imod-profile-field-data":
                data = div.string
                person.update({label: data})
                label = ""
                data = ""
    return person


def is_valid_person(iteration_width, person):
    """
    checks if the person is valid
    """
    global totalis
    mid = person["mid"]
    if len(person) == 1:
        logging.error("%d is not a valid person :(", mid)
        exceptions.append(mid)
    else:
        totalis.append(person)
    if len(exceptions) > 0.65 * (iteration_width):
        log_data()
        return False
    return True


def log_data():
    """
    write data and exceptions to file
    """
    logging.info("logging data")
    write_JSON()
    write_exceptions()


def write_JSON():
    """
    write extracted data as JSON to file
    """
    global totalis
    if len(totalis) == 0:
        return
    with open("out.json", "a") as file:
        json.dump(totalis, file)
        file.write("\n")
    totalis = []


def write_exceptions():
    """
    write exceptions to file
    """
    with open("exceptions.csv", "a") as file:
        for index in exceptions:
            file.write("%d, " % index)
        file.write("\n")


def main():
    """
    groundwork to extract data
    """
    uname, pword, lower_lim, upper_lim, hless = get_args()
    if not hless:
        logging.info("Starting in Debugging mode")
    aide(uname, pword, lower_lim, upper_lim, hless)


if __name__ == "__main__":
    main()
