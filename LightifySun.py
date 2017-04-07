#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import sys
import logging
import datetime
from time import sleep
import ephem
from operator import itemgetter

from pylightify import *
import config as cfg


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

# Setup logging.
logging.basicConfig(level=cfg.loglevel, format='%(levelname)-8s %(message)s')


def sleep_until(wakeuptime):
    interval = 3600
    #
    logging.info ('Sleeping till %s' % wakeuptime)
    #
    time_diff = wakeuptime - datetime.datetime.now() 
    time_diff_in_seconds = (time_diff.days * 86400) + time_diff.seconds + cfg.additionalseconds
    #
    if (time_diff_in_seconds > 0):
        deltasec = time_diff_in_seconds % interval
        logging.debug ('Sleeping for %s of %s seconds = %s hours' % (deltasec, str(time_diff_in_seconds), str(time_diff_in_seconds/3600)))
        sleep (deltasec)
        time_diff_in_seconds -= deltasec
        #
        while (time_diff_in_seconds > 0):
            logging.debug ('Sleeping for %s of %s seconds = %s hours' % (interval, str(time_diff_in_seconds), str(time_diff_in_seconds/3600)))
            sleep (interval)
            time_diff_in_seconds -= interval
    else:
        logging.error ('Time to sleep was null or negative!')

def setlights(onoff):
    logging.info ('Switching lights %s' % str(onoff))
    at = post_gettoken(cfg.user, cfg.password, cfg.serialnumber)
    logging.debug (at)
    result = "Undefined onoff value!"
    if (onoff == 0):
        result = get_turngroupoff(at, cfg.groupid)
    elif (onoff == 1):
        result = get_turngroupon(at, cfg.groupid)
    logging.debug (result)
    
while True:
    # Calculate the sunset for our position
    s=ephem.Sun()
    o=ephem.Observer()
    o.lat=cfg.location[0]
    o.long=cfg.location[1]
    o.elevation = cfg.hight
    # Calculate next sunset
    s.compute(o)
    nextsunset = ephem.localtime(o.next_setting(s))
    prevsunset = ephem.localtime(o.previous_setting(s))
    
    # Get current time
    now = datetime.datetime.now()
    
    # logging.info some information
    logging.debug ('It is: ' + str(now))
    
    # Update times to switch off the lights
    nextlightsouttime = now.replace(hour=cfg.lightsout[0], minute=cfg.lightsout[1], second=0)
    if (now.time() < nextlightsouttime.time()):
        logging.debug('nextlightsouttime should be today')
    else:
        logging.debug('nextlightsouttime should be tomorrow')
        nextlightsouttime += datetime.timedelta(days = 1)
    logging.info ('next_light_off: ' + str(nextlightsouttime))
    
    
    # Update times to switch on the lights
    if (nextsunset.date() == now.date()):
        logging.debug('nextlightsontime should be today')
        nextlightsontime = nextsunset + datetime.timedelta(minutes = cfg.minutesaftersunset)
    elif (now < (prevsunset + datetime.timedelta(minutes = cfg.minutesaftersunset))):
        logging.debug('It is after sunset but before nextlightsontime')
        nextlightsontime = prevsunset + datetime.timedelta(minutes = cfg.minutesaftersunset)
    elif ((prevsunset + datetime.timedelta(minutes = cfg.minutesaftersunset)) < now < nextlightsouttime < (nextsunset + datetime.timedelta(minutes = cfg.minutesaftersunset))):
        logging.debug('Lights should be on right now!')
        nextlightsontime = now + datetime.timedelta(seconds = 5)
    else:
        logging.debug('nextlightsontime should be tomorrow')
        nextlightsontime = nextsunset + datetime.timedelta(minutes = cfg.minutesaftersunset)
    logging.info ('next_light_on: ' + str(nextlightsontime))
    
    
    data = [('nextlightsontime', nextlightsontime, 1), ('nextlightsouttime', nextlightsouttime, 0)]
    data = sorted(data, key=itemgetter(1),reverse=False)
    logging.debug (data)
    
    for i in data:
        logging.info ('Waiting for: ' + i[0])
        sleep_until(i[1])
        setlights(i[2])
    
    