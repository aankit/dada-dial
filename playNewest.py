#!/usr/bin/env python

import sys, time, os
from asterisk.agi import *

agi = AGI()

agi.verbose("python agi started")
callerId = agi.env['agi_callerid']
agi.verbose("call from %s" % callerId)

current = time.time()
newest = 0
newestFile = ''
diff = current - newest
path = '/home/abp225/asterisk_sounds'
for f in os.listdir(path):
  test = current - os.stat(path+'/'+f).st_mtime
  if test < diff:
    diff = test
    newestFile = f
newestFile = newestFile[:-4]
toPlay = '%s/%s' %(path, newestFile) 
# phone.verbose(toPlay)

agi.stream_file(toPlay)
agi.appexec('Wait', 2)
result = agi.stream_file(path + '/another', escape_digits="123456789*#")
if not result:
	result = agi.wait_for_digit(5)
agi.verbose("got digit %s" % result)
if result.isdigit() or result=='*' or result=='#':
    agi.set_context('abp225_dada_dial')
    agi.set_extension('s')
    agi.set_priority(2)
    sys.exit()
else:
  agi.verbose("bye!")
  agi.hangup()
  sys.exit()