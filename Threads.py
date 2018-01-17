#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Sawik
# Email: psawicki@mitr.p.lodz.pl
# License: GNU GPL
#

import wx, threading, serial, Events, Queue

class PumpThread(threading.Thread):
    
    def __init__ (self, port, queue, parent):
        """ Function doc """
        super(PumpThread, self).__init__()
        self.port = port
        self.queue = queue
        self.parent = parent
        
        self.serial = serial.Serial()
        self.serial.port = self.port
        self.serial.timeout = 0.5
        self.serial.baudrate = 9600
        self.serial.parity = 'N'
        
        self.stopRequest = threading.Event()
                        
    def run (self):
        try:
            self.serial.open()
        except Exception, ex:
            print ("[ERROR]\tUnable to open port {}".format(self.port))
            print ("[ERROR]\t{}\n\n{}".format(ex.message, ex.traceback))
            self.stopRequest.set()
        else:
            print ("[INFO]\tListening port {}".format(self.port))
            self.serial.write("FLOW?\r")
        
        while not self.stopRequest.isSet():
            msg = ''
            if not self.queue.empty():
                try:
                    command = self.queue.get()
                    self.serial.write(command)
                except Queue.Empty:
                    continue

            while self.serial.inWaiting():
                char = self.serial.read(1)
                if '\r' in char and len(msg) > 1:
                    char = ''
                    #~ print('[DATA]\t{}'.format(msg))
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
        if self.serial.is_open:
            self.queue.put(msg)
        else:
            print("[ERROR]\tPort {} is not open!".format(self.port))
        
    def Stop(self):
        if self.isAlive():
            self.join()
