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

import wx, os, MainFrame

_ = wx.GetTranslation

class App(wx.App):
    """ Main App class """
    
    def __init__ (self, *args, **kw):
        """ Class initialiser """
        super(App, self).__init__(*args, **kw)
        pass

    def OnInit (self):
        """ App initialiser """
        wx.SetDefaultPyEncoding("utf-8")
        
        self.SetAppName(u'pykpc')
        
        config = wx.Config()
        lang = config.Read('lang', 'LANGUAGE_DEFAULT')
        
        self.locale = wx.Locale(getattr(wx, lang))
        self.localePath = os.path.abspath('./locale') + os.path.sep
        self.locale.AddCatalogLookupPathPrefix(self.localePath)
        self.locale.AddCatalog(self.AppName)
        
        self.frame = MainFrame.MainFrame(None, title=_("Pump"))
        self.frame.Show()
        return True
