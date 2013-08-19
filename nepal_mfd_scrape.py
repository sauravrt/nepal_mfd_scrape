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
    for m in range(1, 13):   #use of xrange is considered better
        foo, days = calendar.monthrange(y, m)
        for d in range(1, days+1): #xrange
            url = 'http://www.mfd.gov.np/archivereport.php?year=' + \
                  str(y) + '&month=' + str(m)+'&day=' + str(d)
            page = urllib2.urlopen(url)
            #you might want to pass a parser to BeautifulSoup. The default parser does not parse malformed html pages correctly.
            #apt-get install python-lxml
            #soup = BeautifulSoup(page, "lxml")
            soup = BeautifulSoup(page)

            #### Please try to separate the parsing logic to a different function. This will make the code easy to maintain if ever the structure of the page changes.
            citytag  = soup.find_all('td', text=re.compile("Kathmandu "))
            try:
                max_temp_tag = citytag[0].find_next('td')
            except:
                continue
            min_temp_tag =  max_temp_tag.find_next('td')

            #### Forecasted temperature
            btag = soup.find_all('b')
            fmintemp = str(btag[9].get_text())
            sepidx = fmintemp.find('-', 1)
            fmin_temp_lo = (fmintemp[:sepidx])
            fmin_temp_hi = (fmintemp[sepidx+1:])
                
            fmaxtemp = str(btag[11].get_text())
            sepidx = fmaxtemp.find('-', 1)                          
            fmax_temp_lo = (fmaxtemp[:sepidx])
            fmax_temp_hi = (fmaxtemp[sepidx+1:])
        
            #### Also you might want to delegate this to a different function (collect the data in some data structure and pass it to the function)
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





