#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Sawik
# Email: psawicki@mitr.p.lodz.pl
# License: GNU GPL
#

import wx

SERIALRX = wx.NewEventType()
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 1)

class PumpDataEvent(wx.PyCommandEvent):
    eventType = SERIALRX

    def __init__(self, eventType, windowID, data='', *args, **kargs):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.eventType = eventType
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)
        
    def GetId(self):
        return self.windowID
    
    def GetData(self):
        return self.data

FLOW_IS_ON = wx.NewEventType()
EVT_FLOW_IS_ON = wx.PyEventBinder(FLOW_IS_ON, 2)

class FlowIsOnEvent(wx.PyCommandEvent):
    eventType = FLOW_IS_ON

    def __init__(self, eventType, windowID, data, *args, **kargs):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.eventType = eventType
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)
        
    def GetId(self):
        return self.windowID

    def GetData(self):
        return self.data
        
FLOW_INFO = wx.NewEventType()
EVT_FLOW_INFO = wx.PyEventBinder(FLOW_INFO, 2)

class FlowInfoEvent(wx.PyCommandEvent):
    eventType = FLOW_INFO

    def __init__(self, eventType, windowID, data, *args, **kargs):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.eventType = eventType
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)
        
    def GetId(self):
        return self.windowID

    def GetData(self):
        return self.data
        
INJ_INFO = wx.NewEventType()
EVT_INJ_INFO = wx.PyEventBinder(INJ_INFO, 2)

class InjInfoEvent(wx.PyCommandEvent):
    eventType = INJ_INFO

    def __init__(self, eventType, windowID, data, *args, **kargs):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.eventType = eventType
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)
        
    def GetId(self):
        return self.windowID

    def GetData(self):
        return self.data

"""
Jeżeli status:
0 - Nic nie jest podłączone
1 - Podłączona jest pompa
2 - Podłączony jest wstrzykiwacz
3 - Oba elementy są podłączone
"""
PUMP_CONNECTED = wx.NewEventType()
EVT_PUMP_CONNECTED = wx.PyEventBinder(PUMP_CONNECTED, 2)

class PumpConnectedEvent(wx.PyCommandEvent):
    eventType = PUMP_CONNECTED

    def __init__(self, eventType, windowID, status, msg="", *args, **kargs):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.eventType = eventType
        self.status = status
        self.msg = msg

    def Clone(self):
        self.__class__(self.GetId(), self.data)
        
    def GetId(self):
        return self.windowID

    def GetStatus (self):
        return self.status
        
    def GetMessage (self):
        """ Function doc """
        return self.msg
