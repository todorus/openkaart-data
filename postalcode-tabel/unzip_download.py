import zipfile
zip_file = zipfile.ZipFile("bag-addressess.csv.zip")
zip_file.extractall()
zip_file.close()
