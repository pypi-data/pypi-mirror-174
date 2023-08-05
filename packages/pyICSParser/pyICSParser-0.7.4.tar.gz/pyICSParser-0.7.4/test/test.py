import datetime
import json
from os.path import abspath, dirname, exists, join, pardir
import sys
from test_vect import rrule_vects as rrule_vectors
from test_vect import parser, rdate_vects, rrule_vects, RFC5545_ical, exdate_vects

SCRIPT_DIR = dirname(abspath("E:\\gitw\\pyICSParser\\src\\pyiCalendar.py"))
sys.path.append(dirname(SCRIPT_DIR))

from src import pyiCalendar

def res_2_json():
    for t in testvectors:
        ics_fp, dtstart, dtend, res = t
        with open(abspath(join(__file__,pardir,"ics",res))) as fi:
            res_lines = fi.readlines()
        results = []
        for l in res_lines:
            #for key in ["summary","datetime-start","uid"]:
            #    l=l.replace(key,f'"{key}"')
            l = l.replace("{","").replace("}","")
            dtstart, summary = l.split(", summary")
            summary, uid = summary.split(", uid")
            line_dict={}
            line_dict["datetime-start"]=dtstart.split(":")[1].replace(" ","")
            line_dict["summary"]=summary.split(": ")[1].strip()
            line_dict["uid"]=uid.replace(" ","").replace("\n","")
            results.append(line_dict)
        if res=="Ferien_Bayern_2012.txt":
            errors=["according to RFC5545 6.1 DTEND is non-inclusive end of evenement, DTEND should not be in results"]
        elif res=="php0b.txt":
            errors = ["according to rFC5545 3.3.10 UNTIL is synchronized with the specified recurrence,\
                    this DATE or DATE-TIME becomes the last instance"]
        else:
            errors = []
        results = {"known errors":errors,"instances":results}
        with open(abspath(join(__file__,pardir,"results",res.replace(".txt",".json"))),'w') as fo:
            fo.write(json.dumps(results,indent=4))
            



def comp_results(vectors):
    total = len(vectors)
    errors = 0
    for count, t in enumerate(vectors):
        ics_fn, dtstart, dtend, res = t
        ics_fp = abspath(join(__file__,pardir,"ics",ics_fn))
        res_fp = abspath(join(__file__,pardir,"results",res.replace(".txt",".json")))
        if exists(ics_fp) and exists(res_fp):
            with open(ics_fp) as fi:
                res_lines = fi.readlines()
            
            with open(res_fp) as fi:
                res = json.load(fi)
            
            res_dates = set([r['datetime-start'] for r in res["instances"]])
            possible_errors = res["known errors"]
            
            mycal = pyiCalendar.iCalendar()
            mycal.local_load(ics_fp)
            
            try:
                dates = mycal.get_event_instances(dtstart,dtend)
            except:
                print(f"error for icas: {ics_fn}")
                raise
            
            dates = set([d[0].strftime("%Y%m%d") for d in dates])
            
            
            if set(res_dates)==dates:
                print(f"{ics_fp} OK")
            else:
                errors+=1
                
                print(f"passed: {int(count/total*100)} %")
                print(f"KKKKKOOOOOOO {ics_fn}")
                print(f"test vector from : {dtstart} to {dtend}")
                print(f"known errors for this vector: {possible_errors}")
                print("missing in pyICSParser",sorted(list(set(res_dates)-dates)))
                print("missing from Results",sorted(list(dates-set(res_dates))))
                dates2 = dates.copy()
                dates2 = sorted(dates2)
                #print("**********dates2")
                #while dates2:
                #    a,b,c,d, *dates2 = dates2
                #    print("\t\t",a,b,c,d)
                #exit()
        else:
            log_msg = f"missing either {ics_fp} or {res_fp}"
            print(log_msg)
            raise Exception(log_msg)
    print(f"total errors: {errors} out of a # of {total} test vectors <=> {int(errors/total*100)} %")
    return errors
# res_2_json()
test_vectors = [("parser", parser), 
                ("rdate", rdate_vects), 
                ("rrule", rrule_vects), 
                ("exdate", exdate_vects)]
staging_test_vectors = [("RFC5545_ica", RFC5545_ical)
                        ]
for (test, vectors) in test_vectors[-3:]:
    try:
        res = comp_results(vectors)
    except:
        print(f"failed {test}")
        raise
    else:
        if res == 0:
            print(f"{test} -- OK")
        else:
            print(f"failed {test} -- {res}")