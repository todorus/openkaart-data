from owslib.wfs import WebFeatureService


# wfs11 = WebFeatureService(url='https://geodata.nationaalgeoregister.nl/bag/wfs', version='1.1.0')
wfs11 = WebFeatureService(url='https://geodata.nationaalgeoregister.nl/inspireadressen/wfs', version='1.1.0')
# print "title\n"
# print wfs11.identification.title

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
