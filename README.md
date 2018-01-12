# AiDE: Alumni Data Extractor #
Extract, parse and organise alumni information from [MyTrinNet](https://mytrinnet.trincoll.edu).

## Goal ##
Make it easier to find alumni with whom one's interests align. This way, we spend less time finding, and more time writing and contacting potential alumni.

## Setup ##
### Install python dependencies ###
`pip3 install --user splinter beautifulsoup4`

### Install the chrome web driver ###
#### For Linux: ####
```
wget https://chromedriver.storage.googleapis.com/2.34/chromedriver_linux64.zip
```

then
```
unzip chromedriver_linux64.zip; chmod +x chromedriver_linux64; mv chromedriver_linux64 ~/.local/bin; rm -f chromedriver_linux64.zip
```

(make sure that `~/.local/bin` is in your `$PATH`)

#### For Mac: ####
```
brew install chromedriver
```

## Usage ##
`./ade.py <trin_username> <trin_password> <loop index lower limit> <loop index upper limit>`

## Related ##
I'm trying to blog often, so I wrote about it [here](https://medium.com/@zorawar87/scraping-trincolls-alumni-database-c671c8aa09b8) (TODO: add link).

Once I close the project, I will write about it again.
