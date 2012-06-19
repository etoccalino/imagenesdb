# # -*- coding: utf-8 -*-
import models 
from django.conf import settings
from django.forms import ModelForm, CharField, TextInput
from django.forms import Form, FileField
from django.forms.util import ErrorList
from django.forms.extras import widgets


filter_by = {'deleted':False,}


class ErrorLabelImportant(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div>%s</div>' % ''.join(
                [u'<span class="badge badge-error">%s</span>' % e \
                 for e in self])


class ImagenesForm(ModelForm):
    def __init__(self, *args, **kwargs):
         kwargs_new = dict(kwargs, **{'error_class': ErrorLabelImportant})
         super(ImagenesForm, self).__init__(*args, **kwargs_new)

    archivo = FileField()

    class Meta:
        model = models.Imagenes
        exclude = ( 'filehash', 'exif')


class BuscaImagenesForm(Form):
    keyword = CharField(label='', 
                        widget = TextInput(attrs={'placeholder':
                                                      'Imagen keyword'}))
