#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Sawik
# Email: psawicki@mitr.p.lodz.pl
# License: GNU GPL
#

import wx
from MainFrame import MainFrame

if __name__ == "__main__":
    wx.SetDefaultPyEncoding("utf-8")
    app = wx.App()
    frm = MainFrame(None, title="Pompa")
    frm.Show()
    app.MainLoop()
