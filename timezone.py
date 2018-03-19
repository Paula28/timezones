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
# IDs are unique and sized to fit into a int16_t (signed 16 bits)
#   When a zone does NOT use DST, the ID == the offset from UTC, in minutes
#   When a zone DOES use DST, the ID is just a unique ID
#
# You would then use it by having a lookup from ID to TZ rules for those zones
# you want to care about.  And use the generic offset for any others.
#
from pytz import common_timezones, timezone
from datetime import datetime
import json
import sys

zones = {}

def generate():
    thisyear = datetime.now().year
    winter = datetime(thisyear, 1, 1, 12, 0)
    summer = datetime(thisyear, 7, 1, 12, 0)
    for tz in common_timezones:
        zone = timezone(tz)
        winter_offset = zone.utcoffset(winter).total_seconds()
        summer_offset = zone.utcoffset(summer).total_seconds()
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
    ids = set()
    for key, d in sorted(zones.iteritems()):
        utcstr = "UTC{0:+d}:{1:02d}".format(int(key[0]/3600), int(key[0]/60%60))
        id = int(key[0]/60)
        dst = key[0] != key[1]
        if dst:
            utcstr += "/{0:+d}:{1:02d}".format(int(key[1]/3600), int(key[1]/60%60))
            id += 16000 + int(key[1]/60) * 10
        if id in ids:
            print >> sys.stderr, "Duplicate ID: %s" % id 
        else:
            ids.add(id)
        tzname = d["names"][-1]
        tzutc = utcstr
        abbrevs = ",".join(d["abbrevs"])
        list_of_zones.append({"id": id, "name": tzname,
            "utc": utcstr, "dst": dst, "abbrs": abbrevs, 
            "offset": int(key[0]/60), "offset_dst": int(key[1]/60)})

    print json.dumps(list_of_zones)

if __name__ == "__main__":
    generate()
