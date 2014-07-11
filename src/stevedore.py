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

from gi.repository import Gtk, Gdk, Gio
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
        self.ui_manager = Gtk.UIManager()
        try:
            self.builder.add_from_file(resource_string(__name__, 'stevedore.glade'))
            self.ui_manager.add_ui_from_file(resource_string(__name__, 'ui_builder.xml'))

        except:
            self.builder.add_from_file('../res/stevedore.glade')
            self.ui_manager.add_ui_from_file('../res/ui_builder.xml')

        # connect handlers
        self.builder.connect_signals(self)
        self.ui_manager.insert_action_group(self.builder.get_object('ContainerActionGroup'))
        self.ui_manager.insert_action_group(self.builder.get_object('ImagesActionGroup'))

        # Prepare certain widgets
        self.status_bar = self.builder.get_object('AppStatus')
        self.status_context_id = self.status_bar.get_context_id('main_app')
        self.builder.get_object('StartButton').set_sensitive(False)
        self.builder.get_object('StopButton').set_sensitive(False)
        self.builder.get_object('AttachButton').set_sensitive(False)
        self.builder.get_object('LogButton').set_sensitive(False)
        self.builder.get_object('DeleteContainerButton').set_sensitive(False)

        # Add window to the App and show it
        self.window = self.builder.get_object('MainWindow')
        self.add_window(self.window)
        self.window.show()
        self.set_app_status(u'Not connected to Docker server.')

    def refresh_views(self, refresh_iface = True):
        """
        Refresh the docker interface object and the reload the ListViews
        to get a fresh snapshot of the system
        """
        # If we have to refresh the Docker interface, we do so
        if hasattr(self, 'docker') and self.docker is not None:
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
            for container_index in self.docker.containers:
                container = self.docker.get_container_by_id(container_index)
                status = container.return_status_string()
                container_list.append(row = [container.names[0],
                                             unicode(container.image),
                                             unicode(container.container_id)[:12],
                                             status,
                                             unicode(container.container_id)])

            for image in self.docker.images:
                size_text = self.size_to_human(image.size)
                virtual_size_text = self.size_to_human(image.virtual_size)
                human_date = time.ctime(int(image.created))
                image_list.append(row = [image.repository,
                                         image.tag,
                                         size_text,
                                         virtual_size_text,
                                         unicode(human_date)])

        else:
            self.set_app_status("Not connected to Docker server.")
            message_dialog = Gtk.MessageDialog(self.window, 0, 
                                               Gtk.MessageType.INFO,
                                               Gtk.ButtonsType.OK,
                                               u"First connect to a Docker server.")
            message_dialog.run()
            message_dialog.destroy()

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

    def on_PreferencesWindow_delete_event(self, obj, event = None):
        """
        The Preferences window has been closed by clicking the close window
        button from the window manager
        
        obj -- 
        event -- 
        """
        preferences_window = self.builder.get_object('PreferencesWindow')
        preferences_window.hide()

        # TODO: Save the preferences
        return True

    def on_PrefsCloseButton_clicked(self, obj, event = None):
        """
        The close button at the preferences has been pressed
        
        obj -- 
        event -- 
        """
        preferences_window = self.builder.get_object('PreferencesWindow')
        preferences_window.hide()
        # TODO: Save the preferences

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
            self.set_app_status(u"Error connecting to Docker Server.")
            message_dialog = Gtk.MessageDialog(self.window, 0, 
                                               Gtk.MessageType.ERROR,
                                               Gtk.ButtonsType.OK,
                                               u"Error connecting to Docker Server:\n {ExceptionMessage}".format(ExceptionMessage = unicode(e)))
            message_dialog.run()
            message_dialog.destroy()
            self.docker = None

            return

        self.set_app_status(u"Connected to Docker server successfully. Fetching container and image data.")
        self.refresh_views(refresh_iface = False)
        self.set_app_status(u"Connected to Docker server.")

    def on_preferences_action_activate(self, obj, event = None):
        """
        We've been asked for the preferences window
        """
        preferences_window = self.builder.get_object('PreferencesWindow')

        # TODO: Set up the window to the current preferences before showing it up
        preferences_window.show()

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

    def on_delete_container_action_activate(self, obj, event = None):
        """
        User wants to delete a selected container
        """
        container_view = self.builder.get_object('ContainerListView')
        selection = container_view.get_selection()
        model, selected = selection.get_selected()
        # selection is a treeiter
        if selected is not None:
            selected_container_id = model[selected][4]
            container = self.docker.get_container_by_id(selected_container_id)

            if container is not None:
                message_dialog = Gtk.MessageDialog(self.window, 0, 
                                                   Gtk.MessageType.QUESTION,
                                                   Gtk.ButtonsType.YES_NO,
                                                   u"Are you sure you want to remove {name} container?".format(name = container.names[0]))
                response = message_dialog.run()
                if response == Gtk.ResponseType.YES:
                    self.docker.remove_container(container.container_id)
                    self.refresh_views()

                message_dialog.destroy()

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

    def on_ContainerListView_button_press_event(self, obj, event = None):
        """
        This hook checks the mouse interaction with the ContainerListView
        """
        if event is not None:
            if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
                container_view = self.builder.get_object('ContainerListView')
                selection = container_view.get_selection()
                model, selected = selection.get_selected()
                # selection is a treeiter
                if selected is not None:
                    selected_container_id = model[selected][4]
                    container = self.docker.get_container_by_id(selected_container_id)

                    if container is not None:
                        if container.status == DockerContainer.EXITED:
                            popup = self.ui_manager.get_widget('/ContainerStoppedPopup')

                        elif container.status == DockerContainer.UP:
                            popup = self.ui_manager.get_widget('/ContainerStartedPopup')

                        else:
                            popup = self.ui_manager.get_widget('/ContainerStoppedPopup')

                        popup.popup(None, None, None, None, event.button, event.time)

                        return True

    def on_container_view_selection_changed(self, selection):
        """
        We control which element is selected on the ContainerListView to enable and disable
        certain button actions
        """
        start_button = self.builder.get_object('StartButton')
        stop_button = self.builder.get_object('StopButton')
        attach_button = self.builder.get_object('AttachButton')
        log_button = self.builder.get_object('LogButton')
        delete_container_button = self.builder.get_object('DeleteContainerButton')

        model, treeiter = selection.get_selected()
        if treeiter is not None:
            container_id = model[treeiter][4]
            container = self.docker.get_container_by_id(container_id)

            if container.status == DockerContainer.UP:
                start_button.set_sensitive(False)
                stop_button.set_sensitive(True)
                attach_button.set_sensitive(True)
                log_button.set_sensitive(True)
                delete_container_button.set_sensitive(False)

            elif container.status == DockerContainer.EXITED:
                start_button.set_sensitive(True)
                stop_button.set_sensitive(False)
                attach_button.set_sensitive(False)
                log_button.set_sensitive(True)
                delete_container_button.set_sensitive(True)

            else:
                start_button.set_sensitive(False)
                stop_button.set_sensitive(False)
                attach_button.set_sensitive(False)
                log_button.set_sensitive(True)
                delete_container_button.set_sensitive(True)

        else:
            start_button.set_sensitive(False)
            stop_button.set_sensitive(False)
            attach_button.set_sensitive(False)
            log_button.set_sensitive(False)
            delete_container_button.set_sensitive(False)



# run main loop
def main():
    main_window = MainWindow()
    main_window.run(None)

if __name__ == "__main__":
    main()

