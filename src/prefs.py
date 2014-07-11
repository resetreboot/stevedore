#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

import os
import os.path

class Preferences(object):
    """
    This class allows us to control and maintain preferences and
    store them
    """
    def __init__(self):
        self.options = dict()
        try:
            self.load_preferences()

        except IOError as e:
            # for debuggin purposes
            print "Error loading preferences file: " + str(e)
            self.create_preferences()

    def load_preferences(self):
        """
        Loads the preferences from the default filename
        """
        with open('~/.config/stevedore/main.conf', 'r') as f:
            for line in f:
                if line[0] != '#':
                    try:
                        option = line.split('=')[0].trim()
                        value = line.split('=')[1].trim()

                        self.options[option] = value

                    except Exception as e:
                        # for debugging purposes
                        print "Problem reading the file: " + str(e)
                        # We'd rather ignore the problems and keep loading
                        pass

    def create_preferences(self):
        """
        If we don't have any preferences file, we create it
        """
        if not os.path.isdir('~/.config/stevedore'):
            # We create the directory
            os.mkdir('~/.config/stevedore')
            self.set_default_options()
            self.save_preferences()







