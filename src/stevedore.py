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
from docker_iface import DockerInterface, DockerImage, DockerContainer, DockerNotConnectedException

import time


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
        self.status_bar = self.builder.get_object('AppStatus')
        self.status_context_id = self.status_bar.get_context_id('main_app')
        self.add_window(self.window)
        self.window.show()
        self.set_app_status(u'Not connected to Docker server.')

    def refresh_views(self, refresh_iface = True):
        """
        Refresh the docker interface object and the reload the ListViews
        to get a fresh snapshot of the system
        """
        # If we have to refresh the Docker interface, we do so
        if refresh_iface:
            self.docker.update_images()
            self.docker.update_containers()

        # Fetch the lists
        container_view = self.builder.get_object('ContainerListView')
        images_view = self.builder.get_object('ImagesListView')

        container_list = container_view.get_model()
        image_list = images_view.get_model()

        # Clear them all
        container_list.clear()
        image_list.clear()

        # And now we populate them back
        for container in self.docker.containers:
            status = container.return_status_string()
            container_list.append(row = [container.names[0],
                                         unicode(container.image),
                                         unicode(container.container_id)[:12],
                                         status])

        for image in self.docker.images:
            size_text = self.size_to_human(image.size)
            virtual_size_text = self.size_to_human(image.virtual_size)
            human_date = time.ctime(int(image.created))
            image_list.append(row = [image.repository,
                                     image.tag,
                                     size_text,
                                     virtual_size_text,
                                     unicode(human_date)])

    def size_to_human(self, size_in_bytes):
        """
        Transforms the size given in bytes to a human readable form, appending
        the units and making it a more manageable size

        Modified from this: http://stackoverflow.com/questions/13343700/bytes-to-human-readable-and-back-without-data-loss
        """
        final_format = u"%(value).2f %(symbol)s"
        symbols = (u'B', u'Kb', u'Mb', u'Gb', u'Tb', u'Pb', u'Eb', u'Zb', u'Yb')
        prefix = {}
        for i, s in enumerate(symbols[1:]):
            prefix[s] = 1 << (i+1)*10
        for symbol in reversed(symbols[1:]):
            if size_in_bytes >= prefix[symbol]:
                value = float(size_in_bytes) / prefix[symbol]
                return final_format % locals()
        return final_format % dict(symbol = symbols[0], value = size_in_bytes)

    def set_app_status(self, message):
        """
        Shows the current application status in the status bar
        """
        try:
            self.status_bar.pop(self.status_context_id)

        except:
            pass

        self.status_bar.push(self.status_context_id, message)

    # Events and "natural" callbacks

    def on_MainWindow_delete_event(self, obj, event = None):
        """
        The main window is deleted
        """
        pass

    ### Action callbacks ###

    def on_connect_action_activate(self, obj, event = None):
        """
        Connection action has been triggered
        """
        # TODO: Get the parameters from configuration
        try:
            self.set_app_status(u"Connecting to Docker server...")
            self.docker = DockerInterface()

        except Exception as e:
            # FIXME: Show a nicer message with a MessageBox
            self.set_app_status(u"Error connecting to Docker Server: " + unicode(e))
            self.docker = None

            return

        self.set_app_status(u"Connected to Docker server successfully. Fetching container and image data.")
        self.refresh_views(refresh_iface = False)
        self.set_app_status(u"Connected to Docker server.")

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

