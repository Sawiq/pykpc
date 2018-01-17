#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Sawik
# Email: psawicki@mitr.p.lodz.pl
# License: GNU GPL
#

import wx, serial.tools.list_ports, Events, Threads, Queue

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
        
        self.pumpQueue = Queue.Queue()
        self.injQueue = Queue.Queue()
        
        self.Bind(Events.EVT_SERIALRX, self.ParsePumpResponse)
        
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
            event = Events.PumpConnectedEvent(Events.PUMP_CONNECTED, self.GetId(), 0, "Nie podłączono żadnych urządzeń!")
            wx.PostEvent(self.parent, event)
            return
            
        numberOfDevices = len(self.availableComPorts)
        
        code = 0
        
        if numberOfDevices > 0:
            try:
                print("[INFO]\tCreating pump thread...")
                self.pumpThread = Threads.PumpThread(self.availableComPorts[0], self.pumpQueue, self)
                self.pumpThread.start()
                self.pumpThread.Write("FLOW?\r")
            except Exception, ex:
                print ("[ERROR]\t {}".format(ex.message))
            else:
                print("[INFO]\t {}".format("Pump thread created."))
                code += 1
                
        if numberOfDevices > 1:
            try:
                print("[INFO]\tCreating injector thread...")
                self.injThread = Threads.PumpThread(self.availableComPorts[1], self.injQueue, self)
                self.injThread.start()
            except Exception, ex:
                print ("[ERROR]\t {}".format(ex.message))
            else:
                print("[INFO]\t {}".format("Injector thread created."))
                code += 1
                
        if code == 0:
            msg = "Błąd połączenia!"
        if code == 1:
            msg = "Podłączono pompę, brak wstrzykiwacza."
        if code == 2:
            msg = "Podłączono wstrzykiwacz, brak pompy."
        if code == 3:
            msg = "Podłączono pompę i wstrzykiwacz."
            
        event = Events.PumpConnectedEvent(Events.PUMP_CONNECTED, self.GetId(), code, msg)
        wx.PostEvent(self.parent, event)
        
        return
        
    def DisconnectPump(self):
        if hasattr(self, 'pumpThread'):
            print("[INFO]\tOdłączam pompę...")
            self.pumpThread.Stop()
            print("[INFO]\tPompa odłączona.")
        if hasattr(self, 'injThread'):
            print("[INFO]\tOdłączam wstrzykiwacz...")
            self.injThread.Stop()
            print("[INFO]\tWstrzykiwacz odłączony.")
        return
    
    def ParsePumpResponse(self, event):
        try:
            pumpResponse = event.data.strip().split(":")
        except Exception, ex:
            print ex.message
            return
        print('[DATA]\t{}'.format(pumpResponse))

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
        if hasattr(self, 'pumpThread'):
            self.pumpThread.Write("ON\r")
        return
    
    def OnStartFlow(self, event):
        return
    
    def SetFlow(self, flow):
        
        return
        
            
