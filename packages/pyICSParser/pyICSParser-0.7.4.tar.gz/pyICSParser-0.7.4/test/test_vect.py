# -*- coding:utf-8 -*-
"""
Created on Jul 28, 2011

@author: Oberron
@attention: icalendar list of test vectors 
@attention: http://www.calconnect.org/tests/iCalendar-RRULE-Interop/iCalendar-RRULE-Interop-Matrix.html
@attention:http://www.calconnect.org/tests/recurr_ical_streams.doc
@attention:http://icalevents.com/2555-paydays-last-working-days-and-why-bysetpos-is-useful/
@attention:http://icalevents.com/2559-week-numbers-and-week-starts/
"""
testvector_path = "./test_vect/"

version = "0.3.1"

parser = [
                ["icalvalid.wikidot/sc_calendar_3325.ics","20090101","20091231","icalvalid.wikidot/sc_calendar_3325.txt"] #source:http://icalvalid.wikidot.com/wild-examples
          ]

exdate_vects = [
                ["exdates/exdate01.ics","20220911","20220920","exdates/exdate01.json"],
                ["exdates/exdate02.ics","20220911","20220920","exdates/exdate02.json"],
               ]

rdate_vects = [
                ["RFC5545_3.8.5.2._4.ics","19910101","19981231","RFC5545_3.8.5.2._4.txt"]
              ]

rrule_vects = [
               ["RFC5545/RFC5545_3.6.ics","20080101","20081231","RFC5545/RFC5545_3.6.txt"],
               ["by_ferie.ics","20110101","20121231","by_ferie_res.txt"],
               ["rdate.ics","20110101","20121231","rdate.txt"],
               ["Ferien_Bayern_2012.ics","20110101","20121231","Ferien_Bayern_2012.txt"],
               ["deutschland.ics","20110101","20121231","deutschland.txt"],
               ["anmar1.ics","20050101","20051231","anmar1.txt"],
               ["anmar2.ics","20050101","20051231","anmar2.txt"],
               ["anmar3.ics","20050101","20051231","anmar3.txt"],
               ["anmar4.ics","20050101","20051231","anmar4.txt"],
               ["anmar5.ics","20050101","20051231","anmar5.txt"],
               ["anmar6.ics","20050101","20051231","anmar6.txt"],
               ["anmar7.ics","20050101","20051231","anmar7.txt"],
               ["anmar8.ics","20050101","20051231","anmar8.txt"],
               ["anmar9.ics","20050101","20051231","anmar9.txt"],
               ["calconnect/ical/01.ics","20110101","20121231","calconnect/ical/01.txt"],
               ["calconnect/mo/01.ics","20110101","20121231","calconnect/mo/01MO.txt"],
               ["calconnect/ol/01.ics","20110101","20121231","calconnect/ol/01OL.txt"],
               ["calconnect/ical/02.ics","20110101","20121231","calconnect/ical/02.txt"],
               ["calconnect/mo/02.ics","20110101","20121231","calconnect/mo/02MO.txt"],
               ["calconnect/ol/02.ics","20110101","20121231","calconnect/ol/02OL.txt"],
               ["calconnect/ical/03.ics","20110101","20121231","calconnect/ical/03.txt"],
               ["calconnect/mo/03.ics","20110101","20121231","calconnect/mo/03MO.txt"],
               ["calconnect/ol/03.ics","20110101","20121231","calconnect/ol/03OL.txt"],
               ["calconnect/ical/04.ics","20110101","20121231","calconnect/ical/04IC.txt"],
               ["calconnect/mo/04.ics","20110101","20121231","calconnect/mo/04MO.txt"],
               ["calconnect/ol/04.ics","20110101","20121231","calconnect/ol/04OL.txt"],
               ["calconnect/ical/05.ics","20110101","20121231","calconnect/ical/05IC.txt"],
               ["calconnect/mo/05.ics","20110101","20121231","calconnect/mo/05MO.txt"],
               ["calconnect/ol/05.ics","20110101","20121231","calconnect/ol/05OL.txt"],
               ["calconnect/ical/06.ics","20110101","20121231","calconnect/ical/06IC.txt"],
               ["calconnect/mo/06.ics","20110101","20121231","calconnect/mo/06MO.txt"],
               ["calconnect/ical/07.ics","20110101","20121231","calconnect/ical/07IC.txt"],
               ["calconnect/mo/07.ics","20110101","20121231","calconnect/mo/07MO.txt"],
               ["calconnect/ol/07.ics","20110101","20121231","calconnect/ol/07OL.txt"],
               ["calconnect/ical/12.ics","20110101","20121231","calconnect/ical/12IC.txt"],
               ["calconnect/mo/12.ics","20110101","20121231","calconnect/mo/12MO.txt"],
               ["calconnect/ol/12.ics","20110101","20121231","calconnect/ol/12OL.txt"],
               
               ["calconnect/ical/13.ics","20110101","20121231","calconnect/ical/13IC.txt"],
               ["calconnect/mo/13.ics","20110101","20121231","calconnect/mo/13MO.txt"],
               ["calconnect/ol/13.ics","20110101","20121231","calconnect/ol/13OL.txt"],

               ["calconnect/ol/14.ics","20110101","20121231","calconnect/ol/14OL.txt"],
               ["calconnect/ol/15.ics","20110101","20121231","calconnect/ol/15OL.txt"],

               ["calconnect/ical/16.ics","20110101","20121231","calconnect/ical/16IC.txt"],
               ["calconnect/mo/16.ics","20110101","20121231","calconnect/mo/16MO.txt"],
               ["calconnect/ol/16.ics","20110101","20121231","calconnect/ol/16OL.txt"],
               
               ["php0a.ics","19960101","20001231","php0a.txt"],
               ["php0b.ics","19960101","20001231","php0b.txt"],
               ["php0c.ics","19960101","20001231","php0c.txt"],
               ["php0d.ics","19960101","20001231","php0d.txt"],
               ["php0e.ics","19960101","20011231","php0e.txt"],
               ["php2a.ics","19960101","20011231","php2a.txt"],
               ["php2b.ics","19960101","20011231","php2b.txt"],
               ["php2c.ics","19960101","20011231","php2c.txt"],
               ["php2d.ics","19960101","20121231","php2d.txt"],
               ["php2e.ics","19960101","20121231","php2e.txt"],
               ["php2f.ics","19960101","20121231","php2f.txt"],
               ["php3a.ics","19960101","20011231","php3a.txt"],
               ["php3b.ics","19960101","20011231","php3b.txt"],
               ["php3c.ics","19960101","20011231","php3c.txt"],
               ["php3d.ics","19960101","20011231","php3d.txt"],
               ["php3e.ics","19960101","20011231","php3e.txt"],
               ["php3f.ics","19960101","20011231","php3f.txt"],
               ["php4a.ics","19960101","20011231","php4a.txt"],
               ["php4b.ics","19960101","20011231","php4b.txt"],
               ["php4c.ics","19960101","20011231","php4c.txt"],
               ["php4d.ics","19960101","20011231","php4d.txt"],
               ["php4e.ics","19960101","20011231","php4e.txt"],
               ["php4f.ics","19960101","20121231","php4f.txt"],
               ["php5a.ics","19960101","20121231","php5a.txt"],
               ["php5b.ics","19960101","20121231","php5b.txt"],
               ["php5c.ics","19960101","20121231","php5c.txt"],
               ["php5d.ics","19960101","20121231","php5d.txt"],
               ["php5e.ics","19960101","20121231","php5e.txt"],
               ["php5f.ics","19960101","20121231","php5f.txt"],
               ["wkst0.ics","19960101","20011231","wkst0.txt"],
               ["wkst1.ics","19960101","20011231","wkst1.txt"],
               ["uk_bank_2007_2013.ics","20120101","20131231","uk_bank_2007_2013.txt"],
               ["soldes_FR.ics","20100101","20141231","soldes_FR.txt"],
               ["france_doi_2007.ics","20100101","20141231","france_doi_2007.txt"],
               ["29fev.ics","20080101","20121231","29fev.txt"],
               ["RFC5545_3.8.5.3_2_RDATE.ics","19970101","19981231","RFC5545_3.8.5.3_2_RDATE.txt"],
               ["SO_14702482_1.ics","20120101","20301231","SO_14702482_1.txt"],
               ["SO_14702482_2.ics","20120101","20301231","SO_14702482_2.txt"],
               ["SCM5545_3.6.1_1.ics","20120101","20301231","SCM5545_3.6.1_1.txt"],
               ["SCM5545_5.2_1.ics","20050101","20061231","SCM5545_5.2_1.txt"]]

RFC5545_ical = [["RFC5545/RFC5545_3.8.5.3_1.ics","20070101","20070530","RFC5545/RFC5545_3.8.5.3_1.txt"],
                ["RFC5545/RFC5545_3.8.5.3_40a.ics","20070101","20070530","RFC5545/RFC5545_3.8.5.3_40a.txt"]
                ]

#SCM test vect templates:
#list of test vectors + for each test vector the list of all exceptions

SCM_withWildICS = [
            ["sc_calendar_3325.ics",['3.4_2','3.1_3', '3.1_2', '3.1_2', '8.3.2_1', '8.3.2_1', '3.8.2.2_1', '3.8.2.2_1', '3.8.2.2_1', '3.8.2.2_1']],
            ["artdoll.ics",['3.4_2','3.1_3', '3.1_2', '8.3.2_1', '3.6_2']],
            ["GilsumNH.ics",['3.4_1', '3.4_2', '3.1_2', '3.6_1', '3.6_2', '3.3.5_1','3.3.5_2']],
            ["projo.ics", ['3.4_2', '3.1_3', '3.1_2', '3.1_3', '3.1_2', '3.1_2']],
            ["carnation.ics",['3.4_2', '3.1_3', '3.1_2', '8.3.2_1']],
            ["SO_15002203.ics",[]],
            ["SO_15047977.ics",['3.4_2', '3.8.4.7_1', '3.8.4.7_1', '3.8.4.7_1', '3.8.4.7_1', '3.8.4.7_1', '3.8.4.7_1', '3.8.4.7_1', '3.8.4.7_1', '3.8.4.7_1', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3', '3.3.5_3']]
            ]
            

SCM_5545 = [["RFC5545/RFC5545_3.8.4.7_1.ics",["3.8.4.7_1"]]
            ]

                    
