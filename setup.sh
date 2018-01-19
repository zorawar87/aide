#!/bin/bash

pip3 install --user splinter beautifulsoup4 coloredlogs
if [ $? -ne 0 ]; then
  wget https://bootstrap.pypa.io/get-pip.py
  python3 get-pip.py --user
fi
wget https://chromedriver.storage.googleapis.com/2.34/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
unzip chromedriver_linux64.zip && chmod +x chromedriver && mv chromedriver ~/.local/bin && rm -f chromedriver_linux64.zip;

if [ $? -eq 0 ]; then
  clear
  echo "RESULT: SUCCESS"
else
  echo "RESULT: FAILED"
fi
