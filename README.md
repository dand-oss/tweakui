

# Gio.Settings example

Alternative to gsettings/dconf

Read in settings from YAML and apply using Gio dictionary access to settings

## Shows
* Access setings as a dictionary
* Sync() to save, rather than accept()
* How to specify schemas, relocatable schemas and dynamic paths
* new_with_path()
* type="as" using tuple
* how to read in settings from YAML
* how to wrap long strings in a list in YAML using folded scalars

This one works with marco and mate, but could use any gnome, right?

## YAML Format
Gio has schemas, and paths.  Sometimes the path is the schema, sometimes not

formatted dictionary:
###    format 1:
use this when the path is the same as the schema
* key name is schema
* value key is a dictionary of values to set for the schema
### format 2:
use this when the path is DIFFERENT than the schema
* key name is path
* schema key is the name of the schema to use on the path
* value key is a dictionary of values to set for the schema

See the code for examples...

## Resources

Location of schemas
/usr/share/glib-2.0/schemas

relocatable schema addressing
* http://wiki.mate-desktop.org/docs:gsettings
* https://www.reddit.com/r/Fedora/comments/4ti7ao/are_the_spins_lacking_complete_integration_simple/

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
