#!/usr/bin/python3

from splinter import Browser
import argparse
import sys
from bs4 import BeautifulSoup as bs
import time
import json
import logging
import progressbar

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
        #browser.cookies.add(auth)
        login(browser)
        iterateProfiles(browser, ns.ll, ns.ul)

def login(browser):
    logging.info("attempting log in...")
    """
    i=0
    url = "https://mytrinnet.trincoll.edu/s/1490/index-3Col.aspx?sid=1490&gid=1&pgid=275&cid=735&mid="+ str(i) +"#/PersonalProfile"
    browser.visit(url)
    #auth = {"__cfduid":"dbb2a6cd8d80c6780ef70535d80acb3551515856917", "ENCOMPASSCC_1490":"bsc", "ENCOMPASSSESSIONID_1490":"2012410b-54e0-4bb1-89aa-f58bb2b5882f", "EncompassAuth":"7VTRsKDOJKhWOgwBKJ3fEwMXwTylNTOSA1Xsph5Raqe2oP__hziIzE86HDh6Dx1EzCvOcYLZKFPIdteQcaGzE-kb8QsqlCyr7rNswsl-YR-LLSGFQ37qFajMaMFMiPFL72RG3SSj9NUt-ufxinolKUia1Et8sIzOpFn-8pn5b0Nv_ZrlXyyDMbAFzlqOm081oP6y-zE58rXIolkHiMjHzdIRxp4GYIF8T9rG5bn6aZrzXAbOBXXIHTdtRDq1Am1UH1IZDLUn1mHHK64ctJ5qXei3AKA"}
    auth = {"__cfduid":"d5fc047fe12a2b7d8896933f47194ea121515860850", "ENCOMPASSSESSIONID_1490":"2012410b-54e0-4bb1-89aa-f58bb2b5882f", "EncompassAuth":"cwDX50uKtXWslGK_zzphCQ0sy7mrx5fpXL6DNrWOx1lBiFFLj3663qTDM79g"}
    browser.cookies.add(auth)
    browser.visit(url)
    """
    url = "https://securelb.imodules.com/s/1490/index-3Col.aspx?sid=1490&gid=1&pgid=3&cid=40"
    browser.visit(url)
    browser.fill('cid_40$txtUsername', ns.username)
    browser.fill('cid_40$txtPassword', ns.password)
    browser.find_by_name('cid_40$btnLogin').click()
    logging.info("checking credentials...")
    time.sleep(2)
    if browser.url.split("//")[1].split("/")[0] == "securelb.imodules.com":
        sys.exit("authentication failed... quitting.")
    else:
        logging.info("authentcation successful!")


def iterateProfiles(browser, low, high):
    logging.info("iterating profiles from %d to %d..." % (low,high))
    global totalis
    for i in range(low, high):
        #widgets = [progressbar.Percentage(), progressbar.Bar()]
        #bar = progressbar.ProgressBar(widgets=widgets, min_value=low, max_value=high).start()
        url = "https://mytrinnet.trincoll.edu/s/1490/index-3Col.aspx?sid=1490&gid=1&pgid=275&cid=735&mid="+ str(i) +"#/PersonalProfile"
        browser.visit(url)
        time.sleep(0.8)
        if verifyPerson(high-low, parseHTMLToPerson(i,browser.html)) == False:
            logging.critical("breaking at %d" % i)
            ns.ul = i+1
            break
        #bar.update(i + 1)
    logData()
    #bar.finish()
    
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
                person.update({label: data})
                label=""
                data=""
    return person

def verifyPerson(range, person):
    global totalis
    mid = person["mid"]
    if len(person) == 1:
        logging.warning("Error or Blank ID at %d" % mid)
        exceptions.append(mid)
    else:
        totalis.append(person)
    if len(exceptions) > 0.65*(range):
        logData()
        return False
    return True

def logData():
    logging.info("logging data")
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

if __name__ == "__main__":
    start = time.time()
    ns = parser.parse_args(sys.argv[1:])
    if ns.headless == False:
        logging.info("Starting in Debugging mode")
    main()
    end = time.time()
    logging.info("Iterating over [%d, %d) took: %f seconds" %(ns.ll, ns.ul, end-start))


