#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Sawik
# Email: psawicki@mitr.p.lodz.pl
# License: GNU GPL
#

import wx, serial.tools.list_ports, Events, threading

class Pump(wx.EvtHandler):
    PORT_BAUD_RATE = 9600
    E_CONNECTION = "Nie można nawiązać połączenia."
    MIN_FLOW = 100
    MAX_FLOW = 5000

    def __init__(self, parent, *args, **kw):
        super(Pump, self).__init__(*args, **kw)
        self.id = wx.NewId()
        self.parent = parent

        self.isConnected = False
        self.isFlowOn = False
        
        self.ConnectPump(None)
                
    def GetId(self):
        return self.id
    
    def GetAvailableComPorts(self):
        self.ports = serial.tools.list_ports.comports()
        self.availableComPorts = []
        for port in serial.tools.list_ports.comports():
            self.availableComPorts.append(port.device)
        
        if len(self.availableComPorts) < 1:
            print ("[ERROR]\tNo devices connected!")
            return []
            
        print("[INFO]\tConnected COM ports: " + str(self.availableComPorts))

        return self.availableComPorts


    def ConnectPump(self, event):
        self.DisconnectPump()
        if not self.GetAvailableComPorts():
            wx.PostEvent(self.parent, Events.PumpConnectedEvent(Events.PUMP_CONNECTED, self.GetId(), 0, "Nie podłączono żadnych urządzeń!"))
            return
        numberOfDevices = len(self.availableComPorts)


        wx.PostEvent(self.parent, Events.PumpConnectedEvent(Events.PUMP_CONNECTED, self.GetId(), 2, "Podłączono urządzeń: {}".format(numberOfDevices)))
        
        return
        
    def DisconnectPump(self):
        return
    
    def ListenPort (self, serial, kill):
        while not kill.isSet():
            msg = ''
            while serial.inWaiting():
                char = serial.read(1)
                if '\r' in char and len(msg) > 1:
                    char = ''
                    event = Events.PumpDataEvent(Events.SERIALRX, wx.ID_ANY, msg)
                    wx.PostEvent(self.parent, event)
                    msg = ''
                    break
                msg += char
        serial.close()
        
    def ParsePumpResponse(self, event):
        try:
            pumpResponse = event.data.strip().split(":")
        except Exception, ex:
            print ex.message
            return
        print('  Komunikat pompy: {}'.format(pumpResponse))

        newEvent = False
        
        if pumpResponse[0] == "ON":
            newEvent = Events.FlowIsOnEvent(Events.FLOW_IS_ON, self.parent.GetId(), True)
        
        if pumpResponse[0] == "OFF":
            newEvent = Events.FlowIsOnEvent(Events.FLOW_IS_ON, self.parent.GetId(), False)
        
        if pumpResponse[0] == "FLOW":
            newEvent = Events.FlowInfoEvent(Events.FLOW_INFO, self.parent.GetId(), pumpResponse[1])
        
        if pumpResponse[0] == "INJ":
            newEvent = Events.InjInfoEvent(Events.INJ_INFO, self.parent.GetId(), pumpResponse[1])
        
        if newEvent:
            wx.PostEvent(self, newEvent)
            #~ wx.PostEvent(self.parent, newEvent)
        
    def StartFlow(self, event):
        return
    
    def OnStartFlow(self, event):
        return
    
    def SetFlow(self, flow):
        return
        
            
