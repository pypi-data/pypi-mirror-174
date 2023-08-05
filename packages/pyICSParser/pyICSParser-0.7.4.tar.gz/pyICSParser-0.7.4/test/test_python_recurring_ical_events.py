from calendar import day_abbr
from datetime import datetime
import json
from os.path import abspath,exists, join, pardir
import sys
from test_vect import rrule_vects as testvectors

try:
    import icalendar
    import recurring_ical_events
except:
    print("pip install icalendar recurring_ical_events")
    raise

from test_vect import rrule_vects as testvectors

def test():
    ok = 0
    for count, t in enumerate(testvectors):
            ics_fn, dtstart, dtend, res = t
            ics_fp = abspath(join(__file__,pardir,"ics",ics_fn))
            res_fp = abspath(join(__file__,pardir,"results",res.replace(".txt",".json")))
            with open (ics_fp) as fi:
                ical_string=fi.read()

            with open(res_fp) as fi:
                res = json.load(fi)
            res_dates = set([r['datetime-start'] for r in res["instances"]])
            dtstart = datetime.strptime(dtstart,"%Y%m%d")
            dtend = datetime.strptime(dtend,"%Y%m%d")
            url = "http://tinyurl.com/y24m3r8f"
            try:
                calendar = icalendar.Calendar.from_ical(ical_string)
                events = recurring_ical_events.of(calendar).between(dtstart, dtend)
                ical_res = []
                for event in events:
                    y, m, d = event["DTSTART"].dt.year, event["DTSTART"].dt.month, event["DTSTART"].dt.day

                    #duration = event["DTEND"].dt - event["DTSTART"].dt
                    #print("start {} duration {}".format(start, duration))
                    ical_res.append(f"{y}{m:02d}{d:02d}")
                if set(res_dates)==set(ical_res):
                    print(f"{ics_fp} ......OK")
                    ok+=1
                else:
                    print(f"{ics_fp} ####  KO")
            except:
                 print(f"{ics_fp} !!!!!  KO")
    print(f"ok ratio : {ok/count}")
test()