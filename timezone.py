#
# Crappy little script to generate a list of possible current timezones.
# It doesn't not include all old timezones and deduplicate them by
# grouping them by winter/summer UTC offsets.  This isn't perfect.
#
# Copyright 2018 Jonathan Poland
#
# Depends on the pytz package
#
# Usage: python timezone.py > timezones.json
#
from pytz import common_timezones, timezone
from datetime import datetime
import json

zones = {}

def generate():
    thisyear = datetime.now().year
    winter = datetime(thisyear, 1, 1, 12, 0)
    summer = datetime(thisyear, 7, 1, 12, 0)
    for tz in common_timezones:
        zone = timezone(tz)
        winter_offset = zone.utcoffset(winter).total_seconds()/60
        summer_offset = zone.utcoffset(summer).total_seconds()/60
        winter_name = zone.tzname(winter)
        summer_name = zone.tzname(summer)
        key = (winter_offset, summer_offset)
        if key in zones:
            zones[key]["names"].append(tz)
        else:
            zones[key] = {"names": [tz], "abbrevs": set()}
        zones[key]["abbrevs"].add(winter_name)
        zones[key]["abbrevs"].add(summer_name)


    list_of_zones = []
    for key, d in sorted(zones.iteritems()):
        utcstr = "UTC{0:+d}:{1:02d}".format(int(key[0]/60), int(key[0]%60))
        if key[0] != key[1]:
            utcstr += "/{0:+d}:{1:02d}".format(int(key[1]/60), int(key[1]%60))
        tzname = d["names"][-1]
        tzutc = utcstr
        abbrevs = ",".join(d["abbrevs"])
        list_of_zones.append({"id": int(key[0] + key[1]), "name": tzname,
            "utc": utcstr, "abbrs": abbrevs, 
            "offset": int(key[0]), "offset_dst": int(key[1])})

    print json.dumps(list_of_zones)

if __name__ == "__main__":
    generate()
