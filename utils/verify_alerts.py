#!/usr/bin/env python

import os
import sys
from os.path import dirname, join, realpath
from optparse import OptionParser

# Get the current working directory of this file.
# http://stackoverflow.com/a/4060259/120999
__location__ = realpath(join(os.getcwd(), dirname(__file__)))

# Add the shared settings file to namespace.
sys.path.insert(0, join(__location__, '..', 'src'))
import settings
# Add the analyzer file to namespace.
sys.path.insert(0, join(__location__, '..', 'src', 'analyzer'))
from alerters import trigger_alert

parser = OptionParser()
parser.add_option("-t", "--trigger", dest="trigger", default=False,
                  help="Actually trigger the appropriate alerts (default is False)")

parser.add_option("-m", "--metric", dest="metric", default='skyline.horizon.queue_size',
                  help="Pass the metric to test (default is skyline.horizon.queue_size)")

(options, args) = parser.parse_args()

try:
    alerts_enabled = settings.ENABLE_ALERTS
    alerts = settings.ALERTS
except:
    print "Exception: Check your settings file for the existence of ENABLE_ALERTS and ALERTS"
    sys.exit()

print 'Verifying alerts for metric: "' + options.metric + '"'

# Send alerts
if alerts_enabled:
    print 'Alerts Enabled'
    for alert in alerts:
        if alert[0] in options.metric:
            print 'Metric name contains: "' + alert[0]
            if options.trigger:
                print '... Alert sent via ' + alert[1]
                trigger_alert(alert, options.metric)
            else:
                print '... Alert would be sent via ' + alert[1]              
else:
    print 'Alerts are Disabled'


