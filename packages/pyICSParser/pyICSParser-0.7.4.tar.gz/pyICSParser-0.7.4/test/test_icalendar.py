from datetime import datetime
import json
from os.path import abspath,exists, join, pardir
import sys
from test_vect import rrule_vects as testvectors

try:
    from icalevents import icalevents
except:
    print("pip -m iicalendar")
    raise

from test_vect import rrule_vects as testvectors

def test():
    for count, t in enumerate(testvectors):
            ics_fn, dtstart, dtend, res = t
            if not ics_fn=="SCM5545_3.6.1_1.ics":
                continue
            dtstart = datetime.strptime(dtstart,"%Y%m%d")
            dtend = datetime.strptime(dtend,"%Y%m%d")
            ics_fp = abspath(join(__file__,pardir,"ics",ics_fn))
            res_fp = abspath(join(__file__,pardir,"results",res.replace(".txt",".json")))

            with open(res_fp) as fi:
                    res = json.load(fi)
            res_dates = set([r['datetime-start'] for r in res["instances"]])
            try:
                evs = icalevents.events(url=None, file=ics_fp, start=dtstart, end=dtend)
                ical_res = []
                for ev in evs:
                    print(31,ev)
                    y, m, d = ev.start.year, ev.start.month, ev.start.day
                    ical_res.append(f"{y}{m:02d}{d:02d}")
                if set(ical_res)==res_dates:
                    print(ics_fn,".........OK")
                else:
                    print(ics_fn,"XXXXXXXX NOK")
                    print("missing from test vector results",set(ical_res)-res_dates)
                    print("missing from icalendar results",res_dates-set(ical_res))
                    exit()
            except:
                print(ics_fn,"!!!!!!!!!! NOK")

def SO_1167333():
    #https://stackoverflow.com/q/70543472/1167333
    from icalendar import Event
    from datetime import datetime
    ev = Event()
    ev.add('dtstart', datetime(2013,11,22,8))
    ev.add('dtend', datetime(2013,11,22,12))
    ev.add('rrule', {'until': datetime(2022,5,2),'freq': 'daily','wkst': 'SU','byday': ['MO', 'WE']})
    print(ev.to_ical().decode("utf-8"))
    

SO_1167333()