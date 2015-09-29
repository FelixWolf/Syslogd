#!/usr/bin/env python
import math

"""See https://en.wikipedia.org/wiki/Syslog#Syslog_message_components for info"""
"""Where is the origin of the request?"""
origins = [
    "kern",     #0:  kernel messages
    "user",     #1:  user-level messages
    "mail",     #2:  mail system
    "system",   #3:  system daemons
    "auth",     #4:  security/authorization messages
    "syslog",   #5:  messages generated internally by syslogd
    "lpr",      #6:  line printer subsystem
    "news",     #7:  network news subsystem
    "uucp",     #8:  UUCP subsystem
    "time",     #9:  clock daemon
    "authpriv", #10: security/authorization messages
    "ftp",      #11: FTP daemon
    "ntp",      #12: NTP subsystem
    "logaudit", #13: log audit
    "logalert", #14: log alert
    "cron",     #15: scheduling daemon
    "local0",   #16: local use 0
    "local1",   #17: local use 1
    "local2",   #18: local use 2
    "local3",   #19: local use 3
    "local4",   #20: local use 4
    "local5",   #21: local use 5
    "local6",   #22: local use 6
    "local7"    #23: local use 7
]

"""Severities"""
severities = [
    "emergency", #0: System is unusable
    "alert",     #1: Should be corrected immediately
    "critical",  #2: Critical conditions
    "error",     #3: Error conditions
    "warning",   #4: May indicate that an error will occur if action is not taken.
    "notice",    #5: Events that are unusual, but not error conditions.
    "info",      #6: Normal operational messages that require no action.
    "debug"      #7: Information useful to developers for debugging the application.
]

"""Resolve a matrix"""
def resolveMatrix(num=0):
    originLoc = math.floor(num/8)
    severityLoc = num%8
    if -1 < originLoc < 24:
        return (origins[originLoc],severities[severityLoc])
    return ("","") #We can't return something we don't know!

"""Resolve recalculated"""
def resolve(o=16,s=6): #Default to local0 info
    if (-1 < originLoc < 24) and (-1 < severities < 8):
        return (self.origins[o],self.severities[s])
    return ("","") #We can't return something we don't know!

