#!/usr/bin/python
from __future__ import with_statement

import os
import EXIF
import mimetypes
import hashlib


def hash_file(filename):
    return hashlib.md5(filename.read()).hexdigest()


def is_image(file):
    valid_img_mimetype = [
        'image/bmp',
        'image/gif',
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/svg+xml',
        ]
    if mimetypes.guess_type(file)[0] in valid_img_mimetype:  
        return True

    return False


def read_file(fpath=None):
    file_data = None
    if is_image(fpath):
        ofile = open(fpath)

        file_data = {'hash':hash_file(fpath),
                     'name': os.path.basename(fpath),
                     'path': fpath,
                     'exif': EXIF.process_file(ofile)
                     }
        ofile.close()

    return file_data


def read_path(img_path, key):
    key = 'md5' if key not in ['md5','name'] else key
    img_data = {'dirpath':'','dirnames':'','filenames':{} }

    for dirpath, dirnames, filenames in os.walk(img_path):
        img_data = {'dirpath': dirpath,
                    'dirnames': dirnames,
                    'files':{}
                    }

        for filename in filenames:
            abs_path = os.path.join(dirpath, filename)
            imagen = read_file(abs_path)
            if imagen:
                try:
                    img_data['files'][ imagen[key] ] = imagen
                except:
                    pass

    return img_data


def yield_path(img_path, key='md5'):
    key = 'md5' if key not in ['md5','name'] else key
    img_data = {'dirpath':'','dirnames':'','filenames':{} }
    
    for dirpath, dirnames, filenames in os.walk(img_path):
        img_data = {'dirpath': dirpath,
                    'dirnames': dirnames,
                    'files':{}
                    }
    
        for filename in filenames:
            abs_path = os.path.join(dirpath, filename)
            imagen = read_file(abs_path)
            if imagen:
                try:
                    yield imagen 
                except:
                    pass
