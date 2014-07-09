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
from docker_iface import DockerInterface, DockerImage, DockerContainer


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

        # Add window to the App and show it
        self.window = self.builder.get_object('MainWindow')
        self.add_window(self.window)
        self.window.show()

    def refresh_views(self):
        """
        Refresh the docker interface object and the reload the ListViews
        to get a fresh snapshot of the system
        """
        print "Not Implemented: refresh_views"

    # Events and "natural" callbacks

    def on_MainWindow_delete_event(self, obj, event = None):
        "on_MainWindow_delete_event activated"
        print 'on_MainWindow_delete_event activated'

    # Action callbacks

    def on_connect_action_activate(self, obj, event = None):
        """
        Connection action has been triggered
        """
        # TODO: Get the parameters from configuration
        try:
            self.docker = DockerInterface()
            self.refresh_views()

        except Exception as e:
            # FIXME: Show a nicer message with a MessageBox
            print u"Error connecting to Docker Server: " + unicode(e)
            self.docker = None

    def on_preferences_action_activate(self, obj, event = None):
        """
        We've been asked for the preferences window
        """
        # TODO
        print "Not implemented: on_preferences_action_activate"

    def on_refresh_action_activate(self, obj, event = None):
        """
        The user wants to reload the listings
        """
        print "on_refresh_action_activate"
        self.refresh_views()

    def on_start_action_activate(self, obj, event = None):
        """
        The user demands a certain container to be started
        """
        print "Not implemented: on_start_action_activate"

    def on_stop_action_activate(self, obj, event = None):
        """
        The user wants to stop a certain container
        """
        # TODO: Remember to show a warning and a yes-no choice before proceeding!
        print "Not implemented: on_stop_action_activate"

    def on_attach_action_activate(self, obj, event = None):
        """
        Here we're requested to attach to a running container
        """
        # TODO: We should launch $TERM with the attach command
        # if the container is running. If not, we display an error or warning
        # Maybe offer the option to start it and then attach?
        print "Not implemented: on_attach_action_activate"

    def on_log_action_activate(self, obj, event = None):
        """
        User wants to see the log output of a certain container
        """
        # TODO: We should launch $TERM with the log command and the -f option
        # unless it is not running, where we remove the -f option and launch it 
        # anyway.
        print "Not implemented: on_log_action_activate"

    def on_build_action_activate(self, obj, event = None):
        """
        Command for building new images from Dockerfiles
        """
        # TODO: Open a OpenFileDialog and build the image.
        print "Not implemented: on_build_action_activate"

    def on_remove_image_action_activate(self, obj, event = None):
        """
        We've been asked to remove an existing image
        """
        print "Not implemented: on_remove_image_action_activate"

    def on_runimage_action_activate(self, obj, event = None):
        """
        Launch selected image into a running container
        """
        print "Not implemented: on_runimage_action_activate"


# run main loop
def main():
    main_window = MainWindow()
    main_window.run(None)

if __name__ == "__main__":
    main()

