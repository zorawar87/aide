#!/usr/bin/python3

from splinter import Browser
import argparse
import sys
from bs4 import BeautifulSoup as bs
import time
import json

parser = argparse.ArgumentParser()
parser.add_argument('username', help="your mytrinnet username")
parser.add_argument('password', help="your mytrinnet password")
parser.add_argument('ll', type=int, help="lower limit of the iterations")
parser.add_argument('ul', type=int, help="upper limit of the iterations")

totalis = []

def main(ns):
    #with Browser('chrome', headless=True) as browser:
    with Browser('chrome') as browser:
        print("successful authentication! iterating profiles...")
        login(browser)
        time.sleep(2)
        iterateProfiles(browser, ns.ll, ns.ul)

def login(browser):
    print("starting...")
    url = "https://securelb.imodules.com/s/1490/index-3Col.aspx?sid=1490&gid=1&pgid=3&cid=40"
    browser.visit(url)
    browser.fill('cid_40$txtUsername', ns.username)
    browser.fill('cid_40$txtPassword', ns.password)
    browser.find_by_name('cid_40$btnLogin').click()

def iterateProfiles(browser, low, high):
    global totalis
    for i in range(low, high):
        url = "https://mytrinnet.trincoll.edu/s/1490/index-3Col.aspx?sid=1490&gid=1&pgid=275&cid=735&mid="+ str(i) +"#/PersonalProfile"
        browser.visit(url)
        time.sleep(0.5)
        if parseHTML(i,browser.html) == False:
            appendJSON()
            totalis =[]
            print("emptied array")
            print(totalis)
    
def parseHTML(mid, html):
    global totalis
    page = bs(html, 'html.parser')
    person = {}
    person.update({"mid":mid})
    label =""
    data =""
    for div in page.find_all("div"):
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
    totalis.append(person)
    print("%d person has %d keys." % (mid, len(person)) )
    if len(person) == 1:
        appendJSON()

def appendJSON():
    with open("out.json","a") as f:
        json.dump(totalis, f)
        f.write("\n")

if __name__ == "__main__":
    start = time.time()
    ns = parser.parse_args(sys.argv[1:])
    main(ns)
    end = time.time()
    print("Iterating over [%d, %d) took: %f seconds" %(ns.ll, ns.ul, end-start))


