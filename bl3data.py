# bl3data.py
# Original: https://github.com/BLCM/bl3mods/blob/master/python_mod_helpers/bl3data/bl3data.py
# Modifications: [
#   Removed: Global Lists, enforce_config_section, serialize_path, get_data, find, find_data, 
#            glob, glob_data, get_export_idx, get_exports, get_refs_to_data, get_refs_from_data,
#            datatable_lookup, process_bvc, process_bvc_struct, cache_part_category_name, guess_part_category_name,
#            get_parts_category_name, get_extra_anoints
#   Altered: init
# ]

# Copyright 2019-2020 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
#
# Copyright (C) 2021-2022 Angel LaVoie
# https://github.com/SSpyR
#
# Borderlands 3 Data Library is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# Borderlands 3 Data Library is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Borderlands 3 Data Library.  If not, see
# <https://www.gnu.org/licenses/>.

import os
import re
import sys
import json
import glob
import appdirs
import sqlite3
import subprocess
import configparser


class BL3Data(object):
    """
    Class to assist in programmatically inspecting Borderlands 3 data as much as
    possible.  The first time this class is instantiated, it'll create a config
    file and then error out.  To use the class, populate at least the "filesystem"
    section of the config file (the path will be provided on the console).

    The "filesystem" section contains two config values:

        1) data_dir - This is a directory containing data extracted from the BL3
           .pak files using UnrealPak.  It should also be processed so that the
           pathnames on the filesystem match the object names exactly.

        2) ueserialize_path - This is the path to a 'ueserialize' binary from the
           JohnWickParse project, used to serialize borderlands .uasset/.umap files
           to a JSON object.  This is what's used to process the extracted data into
           a format we can work with, on an on-demand basis.

           I highly recommend you use my own JWP fork, available here:
           https://github.com/apocalyptech/JohnWickParse/releases

    The "database" section contains the single parameter "dbfile", which should be
    the path to the SQLite BL3 reference data, available at:

        http://apocalyptech.com/games/bl3-refs/

    This is only required if you want to use the `get_refs_to()` or `get_refs_from()`
    methods of this class.
    """

    # Data serialization version requirements
    data_version = 21

    def __init__(self):
        """
        Initialize a BL3Data object.  Will create a sample config file if one
        is not already found.  Will require that the "filesystem" section be
        properly filled in, or we'll raise an exception.
        """

        # Now the rest of the vars we'll use
        self.cache = {}
        self.db = None
        self.curs = None

    def _connect_db(self):
        """
        Attempts to connect to the refs database, if we haven't already done so.
        This used to connect to a MySQL/MariaDB database but we've since switched
        to using SQLite.
        """
        if self.db is None:
            dir=os.path.dirname(__file__)
            dbpath=os.path.join(dir, 'utils/bl3refs.sqlite3')
            if not os.path.exists(dbpath):
                raise RuntimeError('Database file not found: {}'.format(dbpath))
            self.db = sqlite3.connect(dbpath)
            self.curs = self.db.cursor()

    def get_refs_to(self, obj_name):
        """
        Find all object names which reference the given `obj_name`, and return
        a list of those objects.  Requires a database connection to the refs
        database.
        """
        self._connect_db()
        self.curs.execute("""select o2.name
                from bl3object o, bl3refs r, bl3object o2
                where
                    o.name=?
                    and o.id=r.to_obj
                    and o2.id=r.from_obj
                """, (obj_name,))
        return [row[0] for row in self.curs.fetchall()]

    def get_refs_from(self, obj_name):
        """
        Find all object names which `obj_name` references, and return
        a list of those objects.  Requires a database connection to the refs
        database.
        """
        self._connect_db()
        self.curs.execute("""select o2.name
                from bl3object o, bl3refs r, bl3object o2
                where
                    o.name=?
                    and o.id=r.from_obj
                    and o2.id=r.to_obj
                """, (obj_name,))
        return [row[0] for row in self.curs.fetchall()]

    def get_refs_objects_by_short_name(self, short_name):
        """
        Find all objects in our references database whose "short" object
        name (ie: the last path component) is `short_name`.  Requires a
        database connection to the refs database.
        """
        self._connect_db()
        self.curs.execute('select name from bl3object where name like ?',
                (f'%/{short_name}',))
        return [row[0] for row in self.curs.fetchall()]

