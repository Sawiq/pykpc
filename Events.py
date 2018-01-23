#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Sawik
# Email: psawicki@mitr.p.lodz.pl
# License: GNU GPL
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import wx, gettext

gettext.install('pykpc', './locale', unicode=True)

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

ERROR_MSG = wx.NewEventType()
EVT_ERROR_MSG = wx.PyEventBinder(ERROR_MSG, 2)

class ErrorMsgEvent(wx.PyCommandEvent):
    eventType = ERROR_MSG

    def __init__(self, eventType, windowID, data, *args, **kargs):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.eventType = eventType
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)
        
    def GetId(self):
        return self.windowID

    def GetData(self):
        return "Błąd: {}".format(self.data)

"""
Status codes:
0 - Nothing is connected
1 - Pump connected
2 - Injector connected
3 - Both pump and injector connected
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
