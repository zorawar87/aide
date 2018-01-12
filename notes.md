# notes
## Sample URLs: 
1. `/s/1490/index-3Col.aspx?sid=1490&gid=1&pgid=275&cid=735&mid=27299#/PersonalProfile`
2. `/s/1490/index-3Col.aspx?sid=1490&pgid=275&mid=23690#/PersonalProfile`

## GET variables:
* `gid`,`sid`: removing theses alum's info still shows up
* `pgid`: removing causes a session error? needs more investigation.
* `mid`: incrementing this pulls up new alumni. ***Users are serialised!***


## possible requirements
at some level, curl + python should be able to extract information. extracted information can be parsed into a `.csv` (cURL!!!!!!)

data extraction may not be too hard, representation and organisation might be. 
