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

import wx, Pump, Events, gettext
from pymouse import PyMouse
from HelpFrame import HelpFrame

_ = wx.GetTranslation

class MainFrame(wx.Frame):
    
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        
        self.SIZER_PADDING = 5
        self.PUMP_STATUS_BAR = 2
        self.INJ_STATUS_BAR = 1
        
        self.portItems = []
        self.pump = Pump.Pump(self)
        
        self.mouse = PyMouse()

        self.MakeStatusBar()
        self.MakeMenuBar()
        self.MakeMainPanel()
        self.MakeToolBar()
        self.MakeTimer()
        self.MakeBindings()

        #~ self.OnRefreshPortMenu(None)
        
        return
    
    def MakeStatusBar(self):
        self.statusBar = self.CreateStatusBar(3)
        self.statusBar.SetStatusWidths([-6, -1, -1])
        self.SetStatusBar(self.statusBar)
        self.statusBar.SetStatusText(_(u"Detecting pump..."))
        self.statusBar.SetStatusText(u"P", self.PUMP_STATUS_BAR)
        
        return

    def MakeMenuBar(self):
        self.menuBar = wx.MenuBar()
        
        self.fileMenu = wx.Menu()
        self.connectPumpItem = self.fileMenu.Append(wx.ID_ANY, _(u"&Connect with the pump\tCtrl+P"))
        #~ self.refreshPortItem = self.fileMenu.Append(wx.ID_ANY, "&Odśwież porty\tCtrl+R").Enable(False)
        self.fileMenu.AppendSeparator()
        self.exitItem = self.fileMenu.Append(wx.ID_EXIT)
        
        #~ self.portMenu = wx.Menu()
        
        self.helpMenu = wx.Menu()
        
        self.aboutItem = self.helpMenu.Append(wx.ID_ABOUT)
        self.helpItem = self.helpMenu.Append(wx.ID_ANY, _(u"&User manual"))
        
        self.menuBar.Append(self.fileMenu, _(u"&File"))
        #~ self.menuBar.Append(self.portMenu, "&Port")
        self.menuBar.Append(self.helpMenu, _(u"&Help"))
        
        self.Bind(wx.EVT_MENU, self.pump.ConnectPump, self.connectPumpItem)
        #~ self.Bind(wx.EVT_MENU, self.OnRefreshPortMenu, self.refreshPortItem)
        self.Bind(wx.EVT_MENU, self.OnExit, self.exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.aboutItem)
        self.Bind(wx.EVT_MENU, self.OnHelp, self.helpItem)
        
        self.SetMenuBar(self.menuBar)
    
    def MakeMainPanel(self):
        self.mainPanel = wx.Panel(self)
        
        self.flowControlsGroup = wx.StaticBox(self.mainPanel, label=_(u'Flow'))
        self.flowTextCtrl = wx.TextCtrl(self.mainPanel, wx.ID_ANY, '0')
        self.setFlowButton = wx.Button(self.mainPanel, wx.ID_ANY, _(u'&Set'))
        
        self.timerControlsGroup = wx.StaticBox(self.mainPanel, label=_(u'Timer'))
        self.timerTextCtrl = wx.TextCtrl(self.mainPanel, wx.ID_ANY, '0');
        self.startTimerButton = wx.ToggleButton(self.mainPanel, wx.ID_ANY, u'&Start')
        self.startTimerButton.Enable(False)
        
        self.accusitionManualStartCheckBox = wx.RadioButton(self.mainPanel, wx.ID_ANY, _(u'&Manual measurement.'))
        self.accusitionAutoStartCheckBox = wx.RadioButton(self.mainPanel, wx.ID_ANY, _(u'Start accusition when &counting down ends.'))
        self.accusitionAutoStartAfterInjRadioBox = wx.RadioButton(self.mainPanel, wx.ID_ANY, _(u'Start accusition after sample &injection'))
        self.flowAutoStopCheckBox = wx.CheckBox(self.mainPanel, wx.ID_ANY, _(u'Start c&ounting down after sample injection'))
        self.flowAutoStartCheckBox = wx.CheckBox(self.mainPanel, wx.ID_ANY, _(u'Start &flow during sample load.'))
        self.startFlowButton = wx.ToggleButton(self.mainPanel, wx.ID_ANY, _(u'&Turn flow ON'))
        
        self.flowInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.flowInputSizer.Add(self.flowTextCtrl, 0, wx.ALL|wx.EXPAND)
        self.flowInputSizer.Add(wx.StaticText(self.mainPanel, wx.ID_ANY, u"µL/min"), 0, wx.LEFT, self.SIZER_PADDING)
        
        self.timerInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.timerInputSizer.Add(self.timerTextCtrl, 0, wx.ALL|wx.EXPAND)
        self.timerInputSizer.Add(wx.StaticText(self.mainPanel, wx.ID_ANY, u"s"), 0, wx.LEFT, self.SIZER_PADDING)
        
        self.flowControlsSizer = wx.StaticBoxSizer(self.flowControlsGroup, wx.VERTICAL)
        self.flowControlsSizer.Add(self.flowInputSizer, 0, wx.ALL|wx.EXPAND, self.SIZER_PADDING)
        self.flowControlsSizer.Add(self.setFlowButton, 0, wx.ALL|wx.EXPAND, self.SIZER_PADDING)
        
        self.timerControlsSizer = wx.StaticBoxSizer(self.timerControlsGroup, wx.VERTICAL)
        self.timerControlsSizer.Add(self.timerInputSizer, 0, wx.ALL|wx.EXPAND, self.SIZER_PADDING)
        self.timerControlsSizer.Add(self.startTimerButton, 0, wx.ALL|wx.EXPAND, self.SIZER_PADDING)

        self.controlsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.controlsSizer.Add(self.flowControlsSizer, 0, wx.ALL, self.SIZER_PADDING)
        self.controlsSizer.Add(self.timerControlsSizer, 0, wx.ALL, self.SIZER_PADDING)

        self.mainPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainPanelSizer.Add(self.controlsSizer, 0, wx.ALL|wx.EXPAND, self.SIZER_PADDING)      
        self.mainPanelSizer.Add(self.accusitionManualStartCheckBox, 0, wx.ALL, self.SIZER_PADDING)      
        self.mainPanelSizer.Add(self.accusitionAutoStartCheckBox, 0, wx.ALL, self.SIZER_PADDING)      
        self.mainPanelSizer.Add(self.accusitionAutoStartAfterInjRadioBox, 0, wx.ALL, self.SIZER_PADDING)      
        self.mainPanelSizer.Add(self.flowAutoStopCheckBox, 0, wx.ALL, self.SIZER_PADDING)      
        self.mainPanelSizer.Add(self.flowAutoStartCheckBox, 0, wx.ALL, self.SIZER_PADDING)      
        self.mainPanelSizer.Add(self.startFlowButton, 0, wx.ALL|wx.EXPAND, self.SIZER_PADDING)      
        self.mainPanel.SetSizer(self.mainPanelSizer)
        self.mainPanelSizer.SetSizeHints(self)
        
        self.mainPanel.Enable(False)
        
        return
        
    def MakeToolBar(self):
        return
        
    def MakeTimer(self):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimerTick, self.timer)
        self.timeToStopFlow = 0
        
    def MakeBindings(self):
        self.Bind(wx.EVT_TOGGLEBUTTON, self.pump.StartFlow, self.startFlowButton)
        self.Bind(wx.EVT_BUTTON, self.OnSetFlowButton, self.setFlowButton)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSetFlowButton, self.flowTextCtrl)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnStartTimerButton, self.startTimerButton)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnTimerTextCtrlKeyEnter, self.timerTextCtrl)
        
        self.Bind(Events.EVT_PUMP_CONNECTED, self.OnPumpConnected)
        self.Bind(Events.EVT_FLOW_IS_ON, self.OnFlowOn)
        self.Bind(Events.EVT_FLOW_INFO, self.OnSetFlow)
        self.Bind(Events.EVT_INJ_INFO, self.OnInject)
        self.Bind(Events.EVT_ERROR_MSG, self.OnErrorMsg)
    
    def OnAbout (self, event):
        wx.MessageBox(
        _(u"Program for controlling Knauer Azura P2.1S pump over serial port.\n\nAuthor: Sawik\npsawicki@mitr.p.lodz.pl"),
        _(u"About"),
        #~ "Program sterujący pompą Knauer Azura P2.1S za pomocą portu szeregowego.\n\nAutor: Sawik\npsawicki@mitr.p.lodz.pl",
        #~ "O programie",
        wx.OK|wx.ICON_INFORMATION
        )
    
    def OnHelp (self, event):
        """ Shows Help window. """
        self.helpPage = HelpFrame(self)
        self.helpPage.Show()
        
    #~ def OnRefreshPortMenu(self, event):
        #~ for item in self.portMenu.GetMenuItems():
            #~ self.portMenu.Delete(item.GetId())
        #~ ports = self.pump.GetAvailableComPorts()
        #~ self.portItems = []
        
        #~ if not ports:
            #~ self.portItems.append(self.portMenu.Append(wx.ID_ANY, "Brak podłączonych urządzeń").Enable(False))
            #~ self.statusBar.SetStatusText("Nie wykryto pompy.")
            #~ return
        
        #~ for item in ports:
            #~ self.portItems.append(self.portMenu.Append(wx.ID_ANY, item, kind=wx.ITEM_CHECK))
            #~ self.portItems[0].Check(True)
            #~ self.pump.ConnectPump()
            #~ self.mainPanel.Enable(True)
            #~ self.statusBar.SetStatusText("Wykryto urządzeń: {}".format(len(ports)))
        #~ return
        
    def OnExit(self, event):
        self.pump.DisconnectPump();
        self.Close(True)
        
    def OnFlowOn(self, event):
        if event.GetData():
            self.statusBar.SetStatusText(_(u"Flow is turned ON"))
            self.startFlowButton.SetLabel(_(u"Turn flow OFF"))
            self.startTimerButton.Enable(True)
            self.startFlowButton.SetValue(1)
            self.statusBar.SetStatusText(u"ON", self.PUMP_STATUS_BAR)
        else:
            self.statusBar.SetStatusText(_(u"Flow is turned OFF"))
            self.startFlowButton.SetLabel(_(u"Turn flow ON"))
            self.startTimerButton.Enable(False)
            self.startFlowButton.SetValue(0)
            self.statusBar.SetStatusText(u"OFF", self.PUMP_STATUS_BAR)
            
             
    def OnSetFlowButton (self, event):
        self.pump.SetFlow(self.flowTextCtrl.GetValue())
        
    def OnSetFlow (self, event):
        if event.data:
            self.statusBar.SetStatusText(_(u"Flow: {}").format(event.data))
        return
        
        try:
            flowInt = int(event.data)
        except Exception, ex:
            print(u"ERROR\t {}".format(ex.message))
        else:
            self.flowTextCtrl.SetLabel(event.data)
            
    
    def OnErrorMsg (self,event):
        if event.GetData():
            self.statusBar.SetStatusText(event.GetData())
    
    def OnInject (self, event):
        self.statusBar.SetStatusText(event.data, self.INJ_STATUS_BAR)
        
        if event.data == 'I':
            print(u"[INFO]\tSample injected.")
            
            if self.accusitionAutoStartAfterInjRadioBox.GetValue():
                self.StartAccusition()
            
            if self.flowAutoStopCheckBox.GetValue():
                self.startTimerButton.SetValue(1)
                self.OnStartTimerButton(None)
        
        if event.data == 'L':
            print(u"[INFO]\tLoading sample.")
            
            if self.flowAutoStartCheckBox.GetValue():
                self.pump.StartFlow(None)
                self.startFlowButton.SetValue(True)
    
    def OnPumpConnected (self, event):
        """ Function doc """
        self.statusBar.SetStatusText(event.GetMessage())
        if event.status:
            self.mainPanel.Enable(True)
        else:
            self.mainPanel.Enable(False)
            return
            
        if event.status == 3:
            self.flowAutoStartCheckBox.Enable(True)
            self.flowAutoStopCheckBox.Enable(True)
        else:
            self.accusitionAutoStartAfterInjRadioBox.Enable(False)
            self.flowAutoStartCheckBox.Enable(False)
            self.flowAutoStopCheckBox.Enable(False)
            
    def OnTimerTextCtrlKeyEnter (self, event):
        event = wx.MouseEvent(wx.EVT_LEFT_DOWN.typeId, self.startTimerButton.GetId())
        wx.PostEvent(self, event)
            
    def OnStartTimerButton(self, event):
        if not self.startTimerButton.GetValue():
            self.timer.Stop()
            self.statusBar.SetStatusText(_(u"Counting down aborted."))
            self.startTimerButton.SetLabel(_(u"Start"))

        else:
            try:
                self.timeToStopFlow = int(self.timerTextCtrl.GetValue())
            except Exception, ex:
                print("[ERROR]\t{}".format(ex.message))
                self.startTimerButton.SetValue(0)
                return
                
            if self.timeToStopFlow == 0:
                self.startTimerButton.SetValue(0)
                return
            
            self.startTimerButton.SetLabel(_(u"Stop"))
            self.statusBar.SetStatusText(_(u"Flow will stop in {} s").format(self.timeToStopFlow))
            self.timer.Start(1000)
        
    def OnTimerTick (self, event):
        """ Function doc """
        self.timeToStopFlow -= 1
        
        if self.timeToStopFlow > 0:
            self.statusBar.SetStatusText(_(u"Flow will stop in {} s").format(self.timeToStopFlow))
        
        else:
            self.timer.Stop()
            self.startTimerButton.SetLabel(_(u"Start"))
            self.statusBar.SetStatusText(_(u"Flow is stopped."))
            self.startTimerButton.SetValue(0)
            if self.pump.isFlowOn:
                self.pump.StartFlow(None)
            if self.accusitionAutoStartCheckBox.GetValue():
                self.StartAccusition()
                
    def StartAccusition (self):
        print(u"[INFO]\tAccusition started.")
        x_dim, y_dim = self.mouse.screen_size()
        self.mouse.click(70, y_dim - 55, 1)
        pass
        
