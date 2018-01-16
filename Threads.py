#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Sawik
# Email: psawicki@mitr.p.lodz.pl
# License: GNU GPL
#

import wx, threading, serial, Events

class PumpThread(threading.Thread):
    
    def __init__ (self, serial, parent):
        """ Function doc """
        super(PumpThread, self).__init__()
        self.serial = serial
        self.parent = parent
        
        self.stopRequest = threading.Event()
                        
    def run (self):
        while not self.stopRequest.isSet():
            msg = ''
            while self.serial.inWaiting():
                char = self.serial.read(1)
                if '\r' in char and len(msg) > 1:
                    char = ''
                    event = Events.PumpDataEvent(Events.SERIALRX, wx.ID_ANY, msg)
                    wx.PostEvent(self.parent, event)
                    msg = ''
                    break
                msg += char
        self.serial.close()
    
    def join (self, timeout=None):
        """ Function doc """
        self.stopRequest.set()
        super(PumpThread, self).join(timeout)
        
    def SetPort (self, serial):
        self.serial = serial

    def Write (self, msg):
        """ Function doc """
        self.serial.write(msg)
