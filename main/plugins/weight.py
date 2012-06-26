from django.db import models
from models import PluginModel
from interface import Aspect

_weights = (('t', 'tiny'), ('s', 'small'), ('m', 'medium'), ('l', 'large'))


class ImageWeight(PluginModel):
    weight = models.CharField(max_length=1, choices=_weights)


class Weight(Aspect):
    # provide the acceptable key-value combinations for the GET request.
    acceptable_qstring_values = {'weight': [s[1] for s in _weights]}

    def __init__(self, lower_bound=100, medium_bound=1024, upper_bound=3072):
        """Set the bounds used during processing, to categorize the images
        (given in kilobytes)."""
        self.lower_bound = lower_bound
        self.medium_bound = medium_bound
        self.upper_bound = medium_bound

    def process_image(self, image_instance):  # DEBUG
        """Store the weight results of the image in the weight table."""
        weight_register = ImageWeight(image=image_instance)
        weight_register.weight = 'small'  # DEBUG
        weight_register.save()

    def filter_images(self, qdict, queryset):
        """Apply the weight filter to the Imagenes queryset.

        Assuming that the presence of 'weight' key in the qdict indicates its
        value is a non-empty collection, then... TODO """
        try:
            # assume the popped 'weights' its a non-emtpy collection.
            weights = qdict.pop('weight')

            # create a list of filters based on the weight's criteria.
            acceptable = Weight.acceptable_qstring_values
            queries = []
            for weight in filter(lambda s: s in acceptable['weight'], weights):
                queries += queryset.filter(image__weight=weight)

            # the resulting queryset is the OR'ed of the filtered.
            queryset = reduce(lambda q1, q2: q1 | q2, queries)
        except KeyError:
            # no 'weight' criteria... this plugin does nothing.
            pass
        return queryset
