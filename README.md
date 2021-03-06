# AiDE: Alumni Data Extractor #
Extract, parse and organise alumni information from [MyTrinNet](https://mytrinnet.trincoll.edu).

## Goal ##
Make it easier to find alumni with whom one's interests align. This way, we spend less time finding, and more time writing and contacting potential alumni.

## Setup ##
### Install python dependencies ###
`pip3 install --user splinter beautifulsoup4 coloredlogs`

### Install the chrome web driver ###
#### For Linux: ####
```
wget https://chromedriver.storage.googleapis.com/2.34/chromedriver_linux64.zip
```

then
```bash
unzip chromedriver_linux64.zip && chmod +x chromedriver && mv chromedriver ~/.local/bin && rm -f chromedriver_linux64.zip;
```

If `~/.local/bin` in not in `$PATH`, then execute
```bash
echo "export PATH=\$PATH:~/.local/bin" >> ~/.bashrc && source ~/.bashrc;
```

#### For Mac: ####
```
brew install chromedriver
```

## Usage ##
```bash
./ade.py <trin_username> <trin_password> <loop index lower limit> <loop index upper limit>
```

## Related ##
[Blog Post #1](https://medium.com/@zorawar87/scraping-trincolls-alumni-database-c671c8aa09b8)
