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
            soup = BeautifulSoup(page, "lxml")
            temp_data = get_temp_data(soup)
            print 'Writing data for' + str(m)+ "/" + str(d)
            write_temp_data(f, temp_data)
    f.close()
    print 'Closed'

    # -----------------------------------------------------------------------

def get_temp_data(soup):
    '''
    Get temperature data from the soup
    '''
    citytag  = soup.find_all('td', text=re.compile("Kathmandu "))
    # Try to get the tag. Sometimes the data is missing resulting in Out of Index error. In that case just ignore and continue.
    try:
        max_temp_tag = citytag[0].find_next('td')
        data = True
    except:
        data = False
    temp_data = {}
    if data:
        temp_data['max_temp'] = max_temp_tag.text        
        min_temp_tag =  max_temp_tag.find_next('td')
        temp_data['min_temp'] = min_temp_tag.text        
        #### Forecasted temperature
        btag = soup.find_all('b')
        fmintemp = str(btag[9].get_text())
        sepidx = fmintemp.find('-', 1)
        temp_data['fmin_temp_lo'] = (fmintemp[:sepidx])
        temp_data['fmin_temp_hi'] = (fmintemp[sepidx+1:])
        fmaxtemp = str(btag[11].get_text())
        sepidx = fmaxtemp.find('-', 1)                          
        temp_data['fmax_temp_lo'] = (fmaxtemp[:sepidx])
        temp_data['fmax_temp_hi'] = (fmaxtemp[sepidx+1:])
        
    return temp_data

    # -----------------------------------------------------------------------
    
def write_temp_data(fh, temp_data):
    # Write temp_data to csv file
    fh.write(temp_data['fmin_temp_lo'] + ',' + \
            temp_data['fmin_temp_hi'] + ',' + \
            temp_data['fmax_temp_lo'] + ',' + \
            temp_data['fmax_temp_hi'] + ',' + \
            temp_data['max_temp'] + ',' + \
            temp_data['min_temp'] + '\n')
    # -----------------------------------------------------------------------

if __name__ == "__main__":
    get_ktm_temp_data(2012)





