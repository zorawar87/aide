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
parser.add_argument('username', help="your mytrinnet username")
parser.add_argument('password', help="your mytrinnet password")
parser.add_argument('ll', type=int, help="lower limit of the iterations")
parser.add_argument('ul', type=int, help="upper limit of the iterations")
parser.add_argument('-d','--debug',dest='headless', action='store_false', help="starts in debugging mode (chrome starts in GUI mode)")
parser.set_defaults(headless=True)

totalis = []
exceptions = []

def main():
    with Browser('chrome', headless=ns.headless) as browser:
        login(browser)
        iterateProfiles(browser, ns.ll, ns.ul)

def login(browser):
    logging.info("attempting to log in...")
    url = "https://securelb.imodules.com/s/1490/index-3Col.aspx?sid=1490&gid=1&pgid=3&cid=40"
    browser.visit(url)
    browser.fill('cid_40$txtUsername', ns.username)
    browser.fill('cid_40$txtPassword', ns.password)
    browser.find_by_name('cid_40$btnLogin').click()
    time.sleep(2)
    if browser.url.split("//")[1].split("/")[0] == "securelb.imodules.com":
        sys.exit("authentication failed... quitting.")
    else:
        logging.info("authentcation successful!")


def iterateProfiles(browser, low, high):
    logging.info("iterating profiles...")
    global totalis
    for i in range(low, high):
        url = "https://mytrinnet.trincoll.edu/s/1490/index-3Col.aspx?sid=1490&gid=1&pgid=275&cid=735&mid="+ str(i) +"#/PersonalProfile"
        browser.visit(url)
        time.sleep(0.75)
        verifyPerson(parseHTMLToPerson(i,browser.html))
        if len(exceptions) > 0.4*(high-low):
            logging.critical("breaking at %d" % i)
            break
    
def parseHTMLToPerson(mid, html):
    page = bs(html, 'html.parser')
    person = {}
    person.update({"mid":mid})
    label =""
    data =""
    divs = page.find_all("div")
    for div in divs:
        class_attr = div.get('class')
        if class_attr != None:
            if class_attr[0]=="imod-profile-field-label":
                label = div.string
            elif class_attr[0]=="imod-profile-field-data":
                data = div.string
                kv_pair= {label:data}
                person.update(kv_pair)
                label=""
                data=""
    #if len(person) == 1:
        #with open(str(mid)+".html","w") as f:
        #   f.write(html)
    return person

def verifyPerson(person):
    global totalis
    mid = person["mid"]
    if len(person) == 1:
        logging.warning("Error or Blank ID at %d" % mid)
        exceptions.append(mid)
        logData()
    else:
        totalis.append(person)

def logData():
    appendJSON()
    writeExceptions()

def appendJSON():
    global totalis
    if len(totalis) == 0:
        return
    with open("out.json","a") as f:
        json.dump(totalis, f)
        f.write("\n")
    totalis = []

def writeExceptions():
    global exceptions
    with open("exceptions.csv","a") as f:
        for index in exceptions:
            f.write("%d, " % index)
        f.write("\n")
    exceptions = []

if __name__ == "__main__":
    start = time.time()
    ns = parser.parse_args(sys.argv[1:])
    if ns.headless == False:
        logging.info("Starting in Debugging mode")
    main()
    end = time.time()
    logging.info("Iterating over [%d, %d) took: %f seconds" %(ns.ll, ns.ul, end-start))


