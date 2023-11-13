import json
from ise import ISE

ise = ISE()
sponsorPortals = ise.get_sponsor_portals()

print("------------Available sponsor portals:--------------")
for portal in sponsorPortals['SearchResult']['resources']:
    print(f"{portal['name']} - ID {portal['id']}")