# timezones
List of current timezones and the python to generate it.  Useful for generating a list of possible timezones 
for a user to select on a device that simply needs to track time via NTP or a realtime clock.

## Usage

```python timezones.py > timezones.json```

## Caveats

It simply picks a date in winter and a date in summer for each timezone available from pytz (derived from IANA data), 
and determines the offset from GMT.  It then groups all timezones that have the same offset(s) together.  It's 
possible that some timezones that observe daylight savings time are grouped together, but have different rules for 
when DST applies.  For example, one one TZ, it may start on the first Sunday in March.  In another TZ, it may start 
on the second Monday.  These two will be grouped together if they have the same offset for the winter and summer 
dates tested (January 1 and July 1).  Because of this, it's probably best to allow a user to select any TZ that 
doesn't use DST, and add timezones that do use DST on an as-needed basis.

## Further work

It is possible to derive the DST transition rules from the pyTZ library.  This could be used to provide
accurate groupings.
