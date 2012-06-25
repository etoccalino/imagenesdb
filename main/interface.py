# -*- coding: utf-8 -*-

from models import Imagenes

# This code is greatly inspired by (a prettier wording than "copied from")
# "A Simple Plugin Framework", by Marty Alchin on January 10, 2008.
# http://martyalchin.com/2008/jan/10/simple-plugin-framework/


# This class is designed to be a metaclass, not to be instantiated directly.
class Pluggable(type):
    """Provide a mount point for extensions ("plugins").

    A class built using Pluggable becomes a registry: its children are
    automatically registered in the pluggable class "plugins" attribute.
    This allows the system to decouple from the different pieces of code,
    which are now implemented as plugins."""

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)


# this class is designed to be inhereted, not to be instantiated directly.
class Aspect:
    """Mount point for the Aspect-plugins.

    Plugins implementing this protocol should provide:

    TODO: thoroughly describe `filter_images` and `process_image` functions.
    """
    __metaclass__ = Pluggable


def process_image(image_instance):
    """Populate the plugins tables for this image."""
    for plugin in Aspect.plugins:
        plugin().process_image(image_instance)


def exclusive_search(qdict):
    """Produce Imagenes that meet all search criteria simultaneously."""
    qset = Imagenes.objects.filter(deleted=False)
    for plugin in Aspect.plugins:
        qset = plugin().filter_images(qdict, qset)
    return qset


def inclusive_search(qdict):
    """Produce Imagenes that meet any of the search criteria."""
    # Results from each individual plugin are collected.
    qset = Imagenes.object.filter(deleted=False)
    queries = []
    for plugin in Aspect.plugins:
        queries += plugin().filter_images(qdict, qset)

    # All results are joined into one big queryset.
    if queries:
        queryset = reduce(lambda q1, q2: q1 | q2, queries)
    else:
        queryset = Imagenes.objects.null()
    return queryset
