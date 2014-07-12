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

class Preferences(dict):
    """
    This class allows us to control and maintain preferences and
    store them
    """
    def __init__(self):
        self._options = dict()
        self._header = "# Stevedore configuration file\n# This file may be overwritten by the program itself\n"
        home_directory = os.path.expanduser('~')
        self._directory = os.path.join(home_directory, '.config/stevedore')
        self._filename = 'main.conf'
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
        with open(os.path.join(self._directory, self._filename), 'r') as f:
            for line in f:
                if line[0] != '#':
                    try:
                        self._set_config_from_string(line)

                    except Exception as e:
                        # for debugging purposes
                        print "Problem reading the file: " + str(e)
                        # We'd rather ignore the problems and keep loading
                        pass

    def create_preferences(self):
        """
        If we don't have any preferences file, we create it
        """
        if not os.path.isdir(self._directory):
            # We create the directory
            os.mkdir(self._directory)

        if not os.path.exists(os.path.join(self._directory, self._filename)):
            self.set_default_options()
            self.save_preferences()

    def set_default_options(self):
        """
        Set preferences to the defaults
        """
        self._options['localhost'] = True
        self._options['host'] = 'localhost'
        self._options['port'] = 0

        self._header = "# Default options for stevedore.\n# This file may be overwritten from the program itself\n"

    def save_preferences(self):
        """
        Stores the preferences into a file
        """
        try:
            prefs_file = open(os.path.join(self._directory, self._filename), 'w')

        except IOError as e:
            # Debugging
            print "Creating new preferences file"
            self.create_preferences()
            prefs_file = open(os.path.join(self._directory, self._filename), 'w')

        prefs_file.write(self._header + "\n")

        for key in self._options:
            line = self._get_config_string(key)
            if line != "":
                prefs_file.write(line + "\n")

        prefs_file.close()

    def _get_config_string(self, key):
        """
        Turns an option key into a string for the config file
        """
        value = self._options.get(key, None)
        if value is None:
            return ""

        else:
            return key + " = " + str(value)

    def _set_config_from_string(self, config_line):
        """
        Turns an option line into an option
        """
        line_split = config_line.split('=')
        try:
            key = line_split[0].strip()
            val = line_split[1].strip()

        except:
            return

        if val.isdigit():
            value = int(val)

        elif val == 'True':
            value = True

        elif val == 'False':
            value = False

        else:
            value = val

        self._options[key] = value

    def __setitem__(self, key, value):
        """
        Safe option setting
        """
        if type(value) == str or type(value) == unicode:
            if value == 'True':
                value = True

            elif value == 'False':
                value = False

            elif value.isdigit():
                value = int(value)

        self._options[key] = value

    def __getitem__(self, key):
        """
        Return an option value safely. None if it does not exist.
        """
        return self._options.get(key, None)

    def __len__(self):
        """
        Return the number of current options
        """
        return len(self._options)

    def __delitem__(self, key):
        """
        Delete an option
        """
        try:
            del(self._options[key])

        except:
            pass
