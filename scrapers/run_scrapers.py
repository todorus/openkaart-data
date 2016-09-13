from scraper import WFSScraper
from municipalities import MunicipalityWFSScraper
from addresses import AddressWFSScraper
import logging

logging.basicConfig(filename='scrapers.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s'))
logging.getLogger().addHandler(ch)

cbsRegionsWFS = 'https://geodata.nationaalgeoregister.nl/cbsgebiedsindelingen/ows'
# WFSScraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_provincie_2016_gegeneraliseerd', '../data/provinces.geo.json', None).start()
MunicipalityWFSScraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_gemeente_2016_gegeneraliseerd', '/Volumes/openkaart_data/municipalities.geo.json', None).start()
# WFSScraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_wijk_2016_gegeneraliseerd', '../data/district.geo.json', None).start()
# WFSScraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_buurt_2016_gegeneraliseerd', '../data/neighborhoods.geo.json', None).start()
# WFSScraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_ggdregio_2016_gegeneraliseerd', '../data/ggd.geo.json', None).start()
# WFSScraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_jeugdzorgregio_2016_gegeneraliseerd', '../data/youthcare.geo.json', None).start()

bagAddressWFS = 'https://geodata.nationaalgeoregister.nl/inspireadressen/wfs'
AddressWFSScraper(bagAddressWFS, 'inspireadressen:inspireadressen', '/Volumes/openkaart_data/adressen.geo.json', None).start()
