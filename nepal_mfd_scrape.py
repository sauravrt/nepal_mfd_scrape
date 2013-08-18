#!/usr/bin/env python
## nepal_mfd_scrape.py --- 

##  Author: sauravtuladhar@gmail.com
## Saurav R. Tuladhar <sauravtuladhar@gmail.com>
## Version: $Id: nepal_mfd_scrape.py,v 0.0 2013/08/18 13:56:52 saurav Exp$

import urllib2
import re
import calendar
from bs4 import BeautifulSoup

'''
Scrape off max min temperature data from Nepal Meteorological Forecasting Dept
http://www.mfd.gov.np
Currently data is available for year 2011 - 2013 for 17 different locations within the country.
'''

def get_ktm_temp_data(y):
    fname = 'ktm_temp_data' + str(y) + '.csv'
    f = open(fname, 'w')
    f.write('fmin_lo, fmin_hi, fmax_lo, fmax_hi, max, min \n')
    for m in range(1, 13):
        foo, days = calendar.monthrange(y, m)
        for d in range(1, days+1):
            url = 'http://www.mfd.gov.np/archivereport.php?year=' + \
                  str(y) + '&month=' + str(m)+'&day=' + str(d)
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            citytag  = soup.find_all('td', text=re.compile("Kathmandu "))
            try:
                max_temp_tag = citytag[0].find_next('td')
            except:
                continue
            min_temp_tag =  max_temp_tag.find_next('td')

        # Forecasted temperature
            btag = soup.find_all('b')
            fmintemp = str(btag[9].get_text())
            sepidx = fmintemp.find('-', 1)
            fmin_temp_lo = (fmintemp[:sepidx])
            fmin_temp_hi = (fmintemp[sepidx+1:])
                
            fmaxtemp = str(btag[11].get_text())
            sepidx = fmaxtemp.find('-', 1)                          
            fmax_temp_lo = (fmaxtemp[:sepidx])
            fmax_temp_hi = (fmaxtemp[sepidx+1:])
        
            print 'Writing data for' + str(m)+ "/" + str(d)
            f.write(fmin_temp_lo + ',' + \
                    fmin_temp_hi + ',' + \
                    fmax_temp_lo + ',' + \
                    fmax_temp_hi + ',' + \
                    max_temp_tag.text + ',' + \
                    min_temp_tag.text + '\n')
    f.close()
    print 'Closed'    



if __name__ == "__main__":
    get_ktm_temp_data(2012)





