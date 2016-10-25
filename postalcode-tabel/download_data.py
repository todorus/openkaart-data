import urllib
testfile = urllib.URLopener()
testfile.retrieve("http://data.nlextract.nl/bag/csv/bag-adressen-laatst.csv.zip", "bag-addressess.csv.zip")
