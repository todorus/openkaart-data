import csv, json

CSV_FILE_NAME = "bagadres.csv"
JSON_FILE_NAME = "postalcode-tabel.json"
CODES_FILE_NAME = "gemeenten-alfabetisch-2016.csv"

result = []

municipality_codes = {}
province_codes = {}
with open(CODES_FILE_NAME, 'rb') as f:
    print "checking csv dialect of %s" % CODES_FILE_NAME
    dialect = csv.Sniffer().sniff(f.readline(), delimiters=';,')
    f.seek(0)
    reader = csv.reader(f, dialect)

    print "read %s into memory" % CODES_FILE_NAME
    next(reader, None)  # skip the headers
    data = list(reader)
    # Gemeentecode;Gemeentenaam;Provincienaam;Provinciecode;
    for entry in data:
        municipality_codes[entry[1]] = int(entry[0])
        province_codes[entry[2]] = int(entry[3])

with open(CSV_FILE_NAME, 'rb') as f:
    print "checking csv dialect of %s" % CSV_FILE_NAME
    dialect = csv.Sniffer().sniff(f.readline(), delimiters=';,')
    f.seek(0)
    reader = csv.reader(f, dialect)

    print "read %s into memory" % CSV_FILE_NAME
    next(reader, None)  # skip the headers
    data = list(reader)

    postal = None
    # 0openbareruimte;1huisnummer;2huisletter;3huisnummertoevoeging;4postcode;5woonplaats;6gemeente;7provincie;object_id;object_type;nevenadres;x;y;lon;lat
    POSTAL_INDEX = 4
    PLACE_INDEX = 5
    MUNICIPALITY_INDEX = 6
    PROVINCE_INDEX = 7

    print "starting process"
    for entry in data:
        entry_postal = entry[POSTAL_INDEX][:-2]

        if entry_postal != postal:
            result_entry = {
                "postal": entry_postal,
                "municipality": entry[MUNICIPALITY_INDEX],
                "municipality_code": municipality_codes[entry[MUNICIPALITY_INDEX]],
                "province": entry[PROVINCE_INDEX],
                "province_code": province_codes[entry[PROVINCE_INDEX]],
            }
            result.append(result_entry)
            postal = entry_postal

            print json.dumps(result_entry)

print "writing to json file %s" % JSON_FILE_NAME
with open(JSON_FILE_NAME, 'w') as f:
    json.dump(result, f)
