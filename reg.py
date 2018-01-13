#!/usr/bin/python3                                                                                                                          

from splinter import Browser
import argparse
import sys
from bs4 import BeautifulSoup as bs
import time
import json 
import logging

logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser()
parser.add_argument('password', help="your mytrinnet password")
parser.add_argument('ll', type=int, help="lower limit")
parser.add_argument('ul', type=int, help="upper limit")
parser.add_argument('-d','--debug',dest='headless', action='store_false', help="starts in debugging mode (chrome starts in GUI mode)")
parser.set_defaults(headless=True)

reg_url = "https://securelb.imodules.com/s/1490/index-3Col.aspx?sid=1490&gid=1&pgid=8&cid=46"

def main():
    with Browser('chrome', headless=ns.headless) as browser:
        for cid in range(ns.ll, ns.ul):
            browser.visit(reg_url)
            lookup(browser, cid)
            if select(browser, cid) == False:
                logging.critical(str(cid)+" throws exception".format(cid))
                continue
            verify(browser, cid)
            save(register(browser), cid)
            browser.cookies.delete()


def lookup(browser, cid):
    browser.fill("cid_46$tbLookup", cid)
    radio = browser.find_by_name("cid_46$btnFind").click()
    logging.info("looked-up")

def select(browser, cid):
    try:
        radio = browser.find_by_name("RadioGroup").click()
    except Exception:
        return False
    browser.find_by_name("cid_46$dgResults$ctl03$lnkBtnNext").click()
    logging.info("selected")
    return True

def verify(browser, cid):
    browser.fill("cid_46$tbVerify1", cid)
    browser.find_by_name("cid_46$btnVerify").click()
    logging.info("verified")

def register(browser):
    fname = browser.find_by_name("rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl00$ctl00$tblGrouping_40$ctl00$tr_50$ctl00$ctl01$ctl00$fc_50$TextBox1").value
    lname = browser.find_by_name("rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl00$ctl00$tblGrouping_40$ctl00$tr_61$ctl00$ctl01$ctl00$fc_61$TextBox1").value
    uname = str(fname[0]+lname[:7]).lower()
    browser.fill("rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl02$ctl00$tblGrouping_42$ctl00$tr_182$ctl00$ctl01$ctl00$fc_182$TextBox1", uname)
    browser.fill("rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl02$ctl00$tblGrouping_42$ctl00$tr_45$ctl00$ctl01$ctl00$fc_45$TextBox1", ns.password)
    browser.fill("rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl02$ctl00$tblGrouping_42$ctl00$tr_45$ctl00$ctl01$ctl00$fc_45$TextBox1_Confirm", ns.password)
    browser.select("rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl02$ctl00$tblGrouping_42$ctl00$tr_62$ctl00$ctl01$ctl00$fc_62$DropDown1", "1_676")
    browser.find_by_name("rg$gfid_39$tblOuter$ctl00$ctl00$ctl00$ctl01$ctl00$ctl04$btnNext").click()
    logging.info("registered")
    return uname

def save(uname, cid):
    with open("../user", "a") as f:
        f.write("%s %s\n" % (uname, ns.password))
    logging.info("saved "+str(cid))

if __name__ == "__main__":
    ns = parser.parse_args(sys.argv[1:])
    if ns.headless == False:
        logging.info("Starting in Debugging mode")
    main()

