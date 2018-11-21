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

import wx, wx.lib.wxpTag, serial.tools.list_ports

_ = wx.GetTranslation

class SettingsDialog(wx.Dialog):
    """ Class doc """

    def __init__(self, *args, **kw):
        super(SettingsDialog, self).__init__(*args, **kw)

        self.SIZER_PADDING = 10
        
        self.SetTitle(_(u"Settings"))
        
        self.MakeMainPanel()
        self.MakeBindings()
        
        self.Show()
        return
    
    def MakeMainPanel(self):
        """ Generates Main Panel layout """
        self.mainPanel = wx.Panel(self)
        
        self.serialPortsGroup = wx.StaticBox(self.mainPanel, label=_(u"Serial ports"))
        self.serialPortsSizer = wx.StaticBoxSizer(self.serialPortsGroup, wx.VERTICAL)
        self.serialPortsFlexSizer = wx.FlexGridSizer(2, 2, self.SIZER_PADDING, self.SIZER_PADDING)
        
        self.pumpSerialLabel = wx.StaticText(self.serialPortsGroup, wx.ID_ANY, _(u"Pump port"))
        self.injectorSerialLabel = wx.StaticText(self.serialPortsGroup, wx.ID_ANY, _(u"Injector port"))
        self.pumpSerialComboBox = wx.ComboBox(self.serialPortsGroup, wx.ID_ANY)
        self.injectorSerialComboBox = wx.ComboBox(self.serialPortsGroup, wx.ID_ANY)
        
        self.serialPortsFlexSizer.Add(self.pumpSerialLabel)
        self.serialPortsFlexSizer.Add(self.pumpSerialComboBox, 1, wx.EXPAND)
        self.serialPortsFlexSizer.Add(self.injectorSerialLabel)
        self.serialPortsFlexSizer.Add(self.injectorSerialComboBox, 1, wx.EXPAND)
        self.serialPortsSizer.Add(self.serialPortsFlexSizer, 0, wx.ALL|wx.EXPAND, self.SIZER_PADDING)
        
        self.flowLimitsGroup = wx.StaticBox(self.mainPanel, label=_(u"Flow Limits"))
        self.flowLimitsSizer = wx.StaticBoxSizer(self.flowLimitsGroup, wx.HORIZONTAL)
        self.flowLimitsFlexSizer = wx.FlexGridSizer(2, 3, self.SIZER_PADDING, self.SIZER_PADDING)
        
        self.minFlowCtrl = wx.TextCtrl(self.flowLimitsGroup, wx.ID_ANY, '100');
        self.maxFlowCtrl = wx.TextCtrl(self.flowLimitsGroup, wx.ID_ANY, '5000');
        
        self.flowLimitsFlexSizer.Add(wx.StaticText(self.flowLimitsGroup, wx.ID_ANY, _(u"Min flow:")))
        self.flowLimitsFlexSizer.Add(self.minFlowCtrl, 1, wx.EXPAND)
        self.flowLimitsFlexSizer.Add(wx.StaticText(self.flowLimitsGroup, wx.ID_ANY, _(u"µL")), 2, wx.EXPAND)
        self.flowLimitsFlexSizer.Add(wx.StaticText(self.flowLimitsGroup, wx.ID_ANY, _(u"Max flow:")))
        self.flowLimitsFlexSizer.Add(self.maxFlowCtrl, 1, wx.EXPAND)
        self.flowLimitsFlexSizer.Add(wx.StaticText(self.flowLimitsGroup, wx.ID_ANY, _(u"µL")), 2, wx.EXPAND)
        self.flowLimitsSizer.Add(self.flowLimitsFlexSizer, 0, wx.ALL|wx.EXPAND, self.SIZER_PADDING)

        self.flushCellGroup = wx.StaticBox(self.mainPanel, label=_(u"Flush Cell"))
        self.flushCellSizer = wx.StaticBoxSizer(self.flushCellGroup, wx.VERTICAL)
        self.flushCellFlexSizer = wx.FlexGridSizer(2, 3, self.SIZER_PADDING, self.SIZER_PADDING)
        
        self.flushCellFlowCtrl = wx.TextCtrl(self.flushCellGroup, wx.ID_ANY, '1000');
        self.flushCellTimeCtrl = wx.TextCtrl(self.flushCellGroup, wx.ID_ANY, '120');
        
        self.flushCellFlexSizer.Add(wx.StaticText(self.flushCellGroup, wx.ID_ANY, _(u"Flush flow:")))
        self.flushCellFlexSizer.Add(self.flushCellFlowCtrl, 1, wx.EXPAND)
        self.flushCellFlexSizer.Add(wx.StaticText(self.flushCellGroup, wx.ID_ANY, _(u"µL")), 2, wx.EXPAND)
        self.flushCellFlexSizer.Add(wx.StaticText(self.flushCellGroup, wx.ID_ANY, _(u"Flush time:")))
        self.flushCellFlexSizer.Add(self.flushCellTimeCtrl, 1, wx.EXPAND)
        self.flushCellFlexSizer.Add(wx.StaticText(self.flushCellGroup, wx.ID_ANY, _(u"s")), 2, wx.EXPAND)
        self.flushCellSizer.Add(self.flushCellFlexSizer, 0, wx.ALL|wx.EXPAND, self.SIZER_PADDING)
        
        self.saveButton = wx.Button(self.mainPanel, wx.ID_OK, _(u'&OK'))
        self.cancelButton = wx.Button(self.mainPanel, wx.ID_CANCEL, _(u'&Cancel'))
        
        self.buttonsSizer = wx.StdDialogButtonSizer()
        self.buttonsSizer.AddButton(self.saveButton)
        self.buttonsSizer.AddButton(self.cancelButton)
        self.buttonsSizer.Realize()

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.mainSizer.Add(self.serialPortsSizer, 0, wx.ALL|wx.EXPAND|wx.BOTTOM, self.SIZER_PADDING)
        self.mainSizer.Add(self.flowLimitsSizer, 0, wx.ALL|wx.EXPAND|wx.BOTTOM, self.SIZER_PADDING)
        self.mainSizer.Add(self.flushCellSizer, 0, wx.ALL|wx.EXPAND|wx.BOTTOM, self.SIZER_PADDING)
        self.mainSizer.Add(self.buttonsSizer, 0, wx.ALL|wx.EXPAND|wx.BOTTOM, self.SIZER_PADDING)
        self.mainPanel.SetSizer(self.mainSizer)
        self.mainSizer.SetSizeHints(self)
        
        return
        
    def MakeBindings(self):
        """ Binds widgets with respective functions """
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.saveButton)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelButton)
        
    def OnSave(self, event):
        event.Skip()
        self.Close()

    def OnCancel(self, event):
        event.Skip()
        self.Close()
