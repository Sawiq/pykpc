#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Sawik
# Email: psawicki@mitr.p.lodz.pl
# License: GNU GPL
#

import wx
import Pump
import Events

class MainFrame(wx.Frame):
    
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        
        self.SIZER_PADDING = 5
        self.PUMP_STATUS_BAR = 2
        self.INJ_STATUS_BAR = 1
        
        self.portItems = []
        self.pump = Pump.Pump(self)
        
        self.MakeStatusBar()
        self.MakeMenuBar()
        self.MakeMainPanel()
        self.MakeToolBar()
        self.MakeBindings()

        #~ self.OnRefreshPortMenu(None)
        
        return
    
    def MakeStatusBar(self):
        self.statusBar = self.CreateStatusBar(3)
        self.statusBar.SetStatusWidths([-6, -1, -1])
        self.SetStatusBar(self.statusBar)
        self.statusBar.SetStatusText("Wykrywanie pompy...")
        self.statusBar.SetStatusText("P", self.PUMP_STATUS_BAR)
        
        return

    def MakeMenuBar(self):
        self.menuBar = wx.MenuBar()
        
        self.fileMenu = wx.Menu()
        self.connectPumpItem = self.fileMenu.Append(wx.ID_ANY, "&Połącz się z pompą\tCtrl+P")
        #~ self.refreshPortItem = self.fileMenu.Append(wx.ID_ANY, "&Odśwież porty\tCtrl+R").Enable(False)
        self.fileMenu.AppendSeparator()
        self.exitItem = self.fileMenu.Append(wx.ID_EXIT)
        
        #~ self.portMenu = wx.Menu()
        
        self.helpMenu = wx.Menu()
        
        self.aboutItem = self.helpMenu.Append(wx.ID_ABOUT)
        
        self.menuBar.Append(self.fileMenu, "&Plik")
        #~ self.menuBar.Append(self.portMenu, "&Port")
        self.menuBar.Append(self.helpMenu, "P&omoc")
        
        self.Bind(wx.EVT_MENU, self.pump.ConnectPump, self.connectPumpItem)
        #~ self.Bind(wx.EVT_MENU, self.OnRefreshPortMenu, self.refreshPortItem)
        self.Bind(wx.EVT_MENU, self.OnExit, self.exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.aboutItem)
        
        self.SetMenuBar(self.menuBar)
    
    def MakeMainPanel(self):
        self.mainPanel = wx.Panel(self)
        
        self.flowControlsGroup = wx.StaticBox(self.mainPanel, label='Przepływ')
        self.flowTextCtrl = wx.TextCtrl(self.mainPanel, wx.ID_ANY, '0')
        self.setFlowButton = wx.Button(self.mainPanel, wx.ID_ANY, '&Ustaw')
        
        self.timerControlsGroup = wx.StaticBox(self.mainPanel, label='Odliczanie')
        self.timerTextCtrl = wx.TextCtrl(self.mainPanel, wx.ID_ANY, '0');
        self.startTimerButton = wx.ToggleButton(self.mainPanel, wx.ID_ANY, '&Start')
        
        self.accusitionAutoStartCheckBox = wx.CheckBox(self.mainPanel, wx.ID_ANY, 'Rozpocznij pomiar po &zakończeniu odliczania.')
        self.flowAutoStopCheckBox = wx.CheckBox(self.mainPanel, wx.ID_ANY, 'Rozpocznij &odliczanie po nastrzyku.')
        self.flowAutoStartCheckBox = wx.CheckBox(self.mainPanel, wx.ID_ANY, 'Uruchom &przepływ podczas napełniania pętli.')
        self.startFlowButton = wx.ToggleButton(self.mainPanel, wx.ID_ANY, '&Włącz przepływ')
        
        self.flowInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.flowInputSizer.Add(self.flowTextCtrl, 0, wx.ALL|wx.EXPAND)
        self.flowInputSizer.Add(wx.StaticText(self.mainPanel, wx.ID_ANY, "µL/min"), 0, wx.LEFT, self.SIZER_PADDING)
        
        self.timerInputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.timerInputSizer.Add(self.timerTextCtrl, 0, wx.ALL|wx.EXPAND)
        self.timerInputSizer.Add(wx.StaticText(self.mainPanel, wx.ID_ANY, "s"), 0, wx.LEFT, self.SIZER_PADDING)
        
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
        self.mainPanelSizer.Add(self.accusitionAutoStartCheckBox, 0, wx.ALL, self.SIZER_PADDING)      
        self.mainPanelSizer.Add(self.flowAutoStopCheckBox, 0, wx.ALL, self.SIZER_PADDING)      
        self.mainPanelSizer.Add(self.flowAutoStartCheckBox, 0, wx.ALL, self.SIZER_PADDING)      
        self.mainPanelSizer.Add(self.startFlowButton, 0, wx.ALL|wx.EXPAND, self.SIZER_PADDING)      
        self.mainPanel.SetSizer(self.mainPanelSizer)
        self.mainPanelSizer.SetSizeHints(self)
        
        self.mainPanel.Enable(False)
        
        return
        
    def MakeToolBar(self):
        return
        
    def MakeBindings(self):
        self.Bind(wx.EVT_TOGGLEBUTTON, self.pump.StartFlow, self.startFlowButton)
        self.Bind(wx.EVT_BUTTON, self.OnSetFlowButton, self.setFlowButton)
        
        self.Bind(Events.EVT_PUMP_CONNECTED, self.OnPumpConnected)
        self.Bind(Events.EVT_FLOW_IS_ON, self.OnFlowOn)
        self.Bind(Events.EVT_FLOW_INFO, self.OnSetFlow)
        self.Bind(Events.EVT_INJ_INFO, self.OnInject)
    
    def OnAbout (self, event):
        wx.MessageBox(
        "Program sterujący pompą Knauer Azura P2.1S za pomocą portu szeregowego.\n\nAutor: Sawik\npsawicki@mitr.p.lodz.pl",
        "O programie",
        wx.OK|wx.ICON_INFORMATION
        )
        
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
        if event.data:
            self.statusBar.SetStatusText("Przepływ włączony")
            self.startFlowButton.SetLabel("Wyłącz przepływ")
        else:
            self.statusBar.SetStatusText("Przepływ wyłączony")
            self.startFlowButton.SetLabel("Włącz przepływ")
             
    def OnSetFlowButton (self, event):
        self.pump.SetFlow(self.flowTextCtrl.GetValue())
        
    def OnSetFlow (self, event):
        if event.data:
            self.flowTextCtrl.SetText(event.data)
            self.statusBar.SetStatusText("Przepływ: {}".format(event.data))
        return
    
    def OnInject (self, event):
        self.statusBar.SetStatusText(event.data, self.INJ_STATUS_BAR)
        if event.data == 'I':
            if self.flowAutoStopCheckBox.GetValue():
                self.statusBar.SetStatusText("Odliczanie...")
        if event.data == 'L':
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
            
        if event.status > 1:
            self.flowAutoStartCheckBox.Enable(True)
            self.flowAutoStopCheckBox.Enable(True)
        else:
            self.flowAutoStartCheckBox.Enable(False)
            self.flowAutoStopCheckBox.Enable(False)
