from django.db import models
from models import PluginModel
from interface import CategoryAspect


_weights = (('t', 'tiny'), ('s', 'small'), ('m', 'medium'), ('l', 'large'))


class ImageWeight(PluginModel):
    weight = models.CharField(max_length=1, choices=_weights)


class Weight(CategoryAspect):
    configuration = {
        plugin_model: ImageWeight,
        category_name: 'weight',
        category_field_name: 'weight',
        categories: ['tiny', 'small', 'medium', 'large']
        }
    
    def __init__(self, lower_bound=100, medium_bound=1024, upper_bound=3072):
        """Set the bounds used during processing, to categorize the images
        (given in kilobytes)."""
        super(Weight, self).__init__(**configuration)
        self.lower_bound = lower_bound
        self.medium_bound = medium_bound
        self.upper_bound = medium_bound

    def categorize_image(self, image_instance):  # DEBUG
        """Return the weight category this image belongs to."""
        return "small"
