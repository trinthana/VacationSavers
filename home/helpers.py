
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present LBF Travel Inc..us
"""

import base64
import os
import random
import string

from django.conf                import settings
from storages.backends.ftp      import FTPStorage

def upload(username, image):
    file_obj = image

    # do your validation here e.g. file size/type check

    # organize a path for the file in bucket
    file_directory_within_bucket = f'{username}'

    # synthesize a full file path; note that we included the filename
    file_path_within_bucket = os.path.join(
        file_directory_within_bucket,
        file_obj.name
    )

    media_storage = FTPStorage()

    if not media_storage.exists(file_path_within_bucket):  # avoid overwriting existing file
        media_storage.save(file_path_within_bucket, file_obj)

    return media_storage.url(file_path_within_bucket)

    if user_query.exists():
        return user_query.first()

    return False

def cfg_val( aVarName ): 

    return getattr(settings, aVarName, None)

def cfg_LOGIN_ATTEMPTS():

    return cfg_val( "LOGIN_ATTEMPTS" )

def cfg_FTP_UPLOAD(): 
    return cfg_val( "FTP_UPLOAD" )

def delete_user(to_delete_user_username):
    user = to_delete_user_username
    if user.count() == 0:
        return False, 'User not found.'
    if user.last().is_superuser:
        return False, 'Cannot delete superuser.'
    try:
        user.delete()
    except Exception as e:
        return False, str(e)
    return True, f'{to_delete_user_username} deleted successfully.'
