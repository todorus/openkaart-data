from owslib.wfs import WebFeatureService


wfs11 = WebFeatureService(url='https://geodata.nationaalgeoregister.nl/cbsgebiedsindelingen/ows', version='1.1.0')
# print "title\n"
# print wfs11.identification.title

print "options\n======"
print wfs11['cbsgebiedsindelingen:cbs_gemeente_2016_gegeneraliseerd'].crsOptions


print "operations\n=========="
for operation in wfs11.operations:
    print operation.name
print"\n\n\n\n\n"
#
print "contents\n========"
contents = list(wfs11.contents)
contents.sort()
for content in contents:
    print content

# response = wfs11.describefeaturetype('cbsgebiedsindelingen:cbs_gemeente_2016_gegeneraliseerd')
# out = open('response', 'wb')
# out.write(bytes(response.read()))
# out.close()
# print "saved response"
