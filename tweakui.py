# -*- coding: utf-8 -*-

"""

Gio.Settings example

Alternative to gsettings/dconf

Read in settings from YAML and apply using Gio dictionary access to settings

Shows
* Access settings as a dictionary
* Sync() to save, rather than accept()
* How to specify schemas, relocatable schemas and dynamic paths
* new_with_path()
* type="as" using tuple
* how to read in settings from YAML
* how to wrap long strings in a list in YAML using folded scalars

This one works with marco and mate, but could use any gnome, right?

YAML Format
Gio has schmas, and paths.  Sometimes the path is the schema, sometimes not
formatted dictionary:
    format 1:
        use this when the path is the same as the schema
        key name is schema
        value key is a dictionary of values to set for the schema
    format 1:
        use this when the path is DIFFERENT than the schema
        key name is path
        schema key s the name of the schema to use on the path
        value key is a dictionary of values to set for the schema

Resources

Location of schemas
/usr/share/glib-2.0/schemas

relocatable schema addressing
http://wiki.mate-desktop.org/docs:gsettings
https://www.reddit.com/r/Fedora/comments/4ti7ao/are_the_spins_lacking_complete_integration_simple/

Python class
https://lazka.github.io/pgi-docs/Gio-2.0/classes/Settings.html

Accessing settings as dictionary
https://github.com/GNOME/pygobject/blob/master/tests/test_gio.py

panel layout dumper
https://gist.github.com/flexiondotorg/858cfc8081d07f0e9b5f

Guide
https://people.gnome.org/~gcampagna/docs/Gio-2.0/Gio.Settings.html

GIO C docs
https://developer.gnome.org/gio/stable/GSettings.html

YAML "folded scalars"
https://www.jeffgeerling.com/blog/yaml-best-practices-ansible-playbooks-tasks

"""

import sys
import yaml
import re
from gi.repository import Gio


def get_local_settings(
    picture_filename=None,
    mytheme=None
):
    """ YAML settings for tweaks we  like

    Parameters
    ----------
    picture_filename : string
        name of the jpg to use as your background
    mytheme : string
        name of the theme for Mate

    Returns
    -------
    config : dictionary
       a dictionary of put in settings
    """
    ini_str = """

org.mate.background:
    value:
        picture-filename: {0}
org.mate.power-manager:
    value:
        button-lid-ac: nothing
org.mate.screensaver:
    value:
        lock-enabled: false
org.mate.Marco.general:
    value:
        theme: {1}
        compositing-manager: false
org.mate.interface:
    value:
        gtk-theme: {1}
org.mate.caja.desktop:
    value:
        computer-icon-visible: true
org.mate.caja.preferences:
    value:
        show-image-thumbnails: always
        default-folder-viewer: list-view
        date-format: iso
        enable-delete: true
        preview-sound: never
        show-hidden-files: true
/org/mate/panel/objects/clock/prefs/:
    schema: org.mate.panel.applet.clock
    value:
        format: 12-hour
        speed-unit: mph
        temperature-unit: Fahrenheit
        cities:
           - >
               <location name=""
               city="Houston"
               timezone="America/Chicago"
               latitude="29.992500"
               longitude="-95.363892"
               code="KIAH"
               current="false"
               />
           - >
               <location name=""
               city="Bangkok"
               timezone="Asia/Bangkok"
               latitude="13.916667"
               longitude="100.599998"
               code="VTBD"
               current="true"
               />

"""

    return ini_str.format(picture_filename, mytheme)


def get_launcher_settings():
    """ YAML settings for launchers we want

    Returns
    -------
    config : dictionary
       a dictionary of put in settings
    """
    lstr = """

/org/mate/panel/objects/object-5/:
    schema: org.mate.panel.object
    value:
        launcher-location: caja-browser.desktop
        position: 202
        toplevel-id: top
        object-type: launcher
        panel-right-stick: false
/org/mate/panel/objects/object-1/:
    schema: org.mate.panel.object
    value:
        launcher-location: firefox-esr.desktop
        position: 237
        toplevel-id: top
        object-type: launcher
        panel-right-stick: false
/org/mate/panel/objects/object-10/:
    schema: org.mate.panel.object
    value:
        launcher-location: /usr/share/applications/google-chrome.desktop
        position: 277
        toplevel-id: top
        object-type: launcher
        panel-right-stick: false
/org/mate/panel/objects/object-2/:
    schema: org.mate.panel.object
    value:
        launcher-location: terminator.desktop
        position: 304
        toplevel-id: top
        object-type: launcher
        panel-right-stick: false

"""

    return lstr


def get_wm_settings(
    window_manager_name='i3',
    show_desktop_icons=False
):
    """ YAML settings to change window manager

    Parameters
    ----------
    show_desktop-icons : bool
        false keeps caja from opening
        tue had caja show desktop icons
    window-manager : string
        name of window manager to run

    Returns
    -------
    config : dictionary
       a dictionary of put in settings
    """

    lstr = """
org.mate.session.required-components:
    value:
        windowmanager: {}
org.mate.background:
    value:
        show-desktop-icons: {}
    """

    return lstr.format(window_manager_name, show_desktop_icons)


def _set_gio(
    schema,
    path=None,
    kvmap=None
):
    """ You could use _set_gio to write any dictionary

    Parameters
    ----------
    schema : string
        schema for Gio settings schema
    path : string
        path in settings tree
    kvmap : # list of k,v tuples - dictionary.items()
        k,v to be set

    """

    print('Setting schema: \'{}\''.format(schema))
    if path:
        print('    path {}'.format(path))

    # use path or not?
    settings = Gio.Settings.new(schema) if not path \
        else Gio.Settings.new_with_path(schema, path)

    for key, val in kvmap:
        # access settings as a dictionary
        # nice syntax, and handles conversion from nasty old C types bleh
        # this is the only lines that does any real work..
        settings[key] = val
        print('    {}: {}'.format(key, val))

    settings.sync()  # required to WRITE the settings to disk


def set_kv(
    pathstr,  # settings path
    pdict     # dict of values
):
    """ Convenient way to set a section for our personal format dictionaries
    pdict: a dictionary used to update settings, containing
       schema: use this schema, if path is not a schema

    Parameters
    ----------
    pathstr : string
        settings path to use - schema or path
    pdict : dict
       dictionary of data to set

    """

    # does this path have a schema?
    cschema = pdict.get('schema', None)

    # if no schema, then the section is schema and no path
    # if section is a path, use the schema found
    schema, path = (pathstr, None) if not cschema \
        else (cschema, pathstr)

    _set_gio(
        schema,                        # will be validated
        path=path,                     # may be None
        kvmap=pdict['value'].items())  # dictionary list


def add_launchers():
    """ This routines adds launcher to the mate "panel" """

    config = yaml.load(get_launcher_settings())

    obj_ids = []  # collect object ids as we make them
    for pathkey, pdict in config.items():

        # set the settings
        set_kv(pathkey, pdict)

        # hang on to object-id string for later
        ostr = re.search('(object-\\d+)', pathkey)
        obj_ids.append(ostr.group(1))

    # get current object id list in Mate
    settings = Gio.Settings.new('org.mate.panel')
    curr_oid_list = settings['object-id-list']

    # filter "object-" ids from current list
    new_oid_list = [cobj for cobj in curr_oid_list if 'object-' not in cobj]

    # add object ids for our launchers
    new_oid_list.extend(obj_ids)

    # write new object id list via settings dictionary
    settings['object-id-list'] = new_oid_list
    settings.sync()


def set_config(config):
    """ This routines adds luancher to the mate "panel"

    Parameters
    ----------
    config : dict
       matches the yaml format
          path-to-section: # value will be the schema name or a path
              schema: #if a path, value will be the schema to use
              value:  # a dictionary of key/values to set

    """
    for pathkey, pdict in config.items():
        set_kv(pathkey, pdict)


def set_i3():
    """ Set the i3 window manager"""

    set_config(
        yaml.load(
            get_wm_settings(
                window_manager_name='i3',
                show_desktop_icons=False)))


def set_mate():
    """ Set the marco (mate) window manager"""
    set_config(
        yaml.load(
            get_wm_settings(
                window_manager_name='marco',
                show_desktop_icons=True)))


def my_gsettings(
    picture_filename='/home/user/Wallpaper/good-art.jpg',
    mytheme='BlackMATE'
):
    """ A routine to do "my" Mate desktop settings via Gnome gsettings python

    Parameters
    ----------
    picture_filename : string
        name of the jpg to use as your background
    mytheme : string
        name of the theme for Mate
    """

    set_config(
        yaml.load(
            get_local_settings(
                picture_filename,
                mytheme)))


def main(argv=None):
    if argv is None:
        argv = sys.argv

    my_gsettings()

    add_launchers()

    set_i3()
    # set_mate()

    print('completed settings')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
