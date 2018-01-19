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

import wx, wx.lib.wxpTag

class HelpFrame(wx.Frame):
    """This window displays manual."""
    
    def __init__ (self, parent):
        """ Function doc """
        wx.Frame.__init__(self, parent, title="Instrukcja obsługi", size=(500, 400))

        htmlwin = wx.html.HtmlWindow(self)
        #~ htmlwin.LoadPage("help.html")
        htmlwin.LoadPage("help.html")
