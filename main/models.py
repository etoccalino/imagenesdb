# -*- coding: utf-8 -*-
from django.db import models
import imagereader
import interface


class Imagenes(models.Model):
    filehash = models.CharField(max_length=255, editable=False)
    exif = models.TextField(editable=False)
    archivo = models.ImageField(upload_to=".",
                                verbose_name="Imagen:",
                                max_length=500, blank=True, null=True)
    deleted = models.BooleanField(default=False, editable=False)

    def _parse_imagen(self):
        if not self.archivo:
            return

        data_imagen = imagereader.read_file(self.imagen.path)
        self.filehash = data_imagen['hash']
        self.exif = data_imagen['exif']
        self.save()

    def save(self):
        super(Imagenes, self).save()

    def __unicode__(self):
        return self.filename


class PluginModel(models.Model):
    """Plugins will index Imagenes through this relation.

    Notice that a OneToOne would forbid fuzzy categorization."""
    image = models.ForeignKey(Imagenes, related_name='+')

    class Meta:
        abstract = True


###############################################################################


class BuscaImagenes(Imagenes):
    class Meta:
        proxy = True

    model = Imagenes
    search_fields = ('filehash',
                     'exif',
                     'archivo',
                     'deleted')

    def search_image(self, httprequest):
        if httprequest.method == "GET":
            qdict = httprequest.GET.copy()
            return interface.exclusive_search(qdict)
