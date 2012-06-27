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


# this class is designed to be inhereted from, not to be instantiated directly.
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
        queryset = Imagenes.objects.none()
    return queryset


###############################################################################


class Category:
    """Category plugins are common. This class isolates common behaviuor.

    The 'category_name', holding the categories of interest to the user,
    is expected in the qdict.

    An extending plugin should provide:
    - the PluginModel which holds the data for the plugin.
    - the name of the field in the plugin model which is relevant.
    - the 'category_name', the name expected in the qdict, which identifies
      this category to the end user.
    - the 'categories', with all possible values of the category.
    - the callable 'categorize_image', which takes an Imagenes and returns
      the particular category it belongs to (only one, in this implementation).
    """

    def __init__(self, plugin_model, category_field_name, category_name,
                 categories, *args, **kwargs):
        super(CategoryAspect, self).__init__(*args, **kwargs)
        self.plugin_model = plugin_model
        self.category_field_name = category_field_name
        self.category_name = category_name
        self.categories = categories

    def process_image(self, image_instance):
        """Store the resulting category of the image in the weight table."""
        categorized = self.plugin_model(image=image_instance)
        category = self.categorize_image(image_instance)
        setattr(categorized, self.category_field_name, category)
        categorized.save()

    def filter_images(self, qdict, queryset):
        """Apply this category filter to the Imagenes queryset.

        Assuming that the presence of 'weight' key in the qdict indicates its
        value is a non-empty collection, then... TODO """
        try:
            # assume the popped 'categories' its a non-emtpy collection.
            categories = qdict.pop(self.category_name)

            # create a list of filters based on the category criteria.
            queries = []
            query_selector = 'image__' + self.category_field_name
            for category in filter(lambda s: s in self.categories, categories):
                queries += queryset.filter(**{query_selector: category})

            # the resulting queryset is the OR'ed of the filtered.
            queryset = reduce(lambda q1, q2: q1 | q2, queries)
        except KeyError:
            # no criteria... this plugin does nothing.
            pass
        return queryset
