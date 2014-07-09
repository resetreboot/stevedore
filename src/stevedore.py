#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Generated with glade2py script
# glade2py script can be found at hocr web site http://hocr.berlios.de

from gi.repository import Gtk, Gio
from pkg_resources import resource_string


class MainWindow(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id = "apps.gnome.stevedore",
                                 flags = Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self.on_app_start)

    def on_app_start(self, data = None):
        
        # create widget tree ...
        self.builder = Gtk.Builder()
        try:
            self.builder.add_from_file(resource_string(__name__, 'stevedore.glade'))

        except:
            self.builder.add_from_file('../res/stevedore.glade')

        # connect handlers
        self.builder.connect_signals(self)

        # widgets
        self.window = self.builder.get_object('MainWindow')
        self.add_window(self.window)
        self.window.show()

        # Remember to add your Gtk.Window to the object with self.add_window(my_gtk_window)

        # signal handlers
        # def on_action_save_activate(self, obj, event = None):
        #     "on_action_save_activate activated"
        #     print 'on_action_save_activate activated'

        # def on_action_record_activate(self, obj, event = None):
        #     "on_action_record_activate activated"
        #     print 'on_action_record_activate activated'

        # def on_MainWindow_delete_event(self, obj, event = None):
        #     "on_MainWindow_delete_event activated"
        #     print 'on_MainWindow_delete_event activated'

        # def on_SaveWindow_delete_event(self, obj, event = None):
        #     "on_SaveWindow_delete_event activated"
        #     print 'on_SaveWindow_delete_event activated'


# run main loop
def main():
    main_window = MainWindow()
    main_window.run(None)

if __name__ == "__main__":
    main()

