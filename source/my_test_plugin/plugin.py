#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    example_library_management_file_test

    Docs:
        https://docs.unmanic.app/docs/plugins/writing_plugins/plugin_runner_types/

"""

import logging
import os
import shutil
from configparser import NoSectionError, NoOptionError

from unmanic.libs.directoryinfo import UnmanicDirectoryInfo
from unmanic.libs.unplugins.settings import PluginSettings


# Configure plugin logger
logger = logging.getLogger("Unmanic.Plugin.reject_files_larger_than_original")




class Settings(PluginSettings):
    settings = {
        'if_end_result_file_is_still_larger_mark_as_ignore': False, 
        'log_info': False,
    }
    form_settings = {
        "if_end_result_file_is_still_larger_mark_as_ignore": {
            "label": "If the final result is still larger than the original file, ignore this file in the future.",
        "log_info":{
            "label":"Check to log certain events to logger",
        }
        
        },
    }

def on_library_management_file_test(data):
    """
    Runner function - enables additional actions during the library management file tests.

    The 'data' object argument includes:
        path                            - String containing the full path to the file being tested.
        issues                          - List of currently found issues for not processing the file.
        add_file_to_pending_tasks       - Boolean, is the file currently marked to be added to the queue for processing.

    :param data:
    :return:
    """

    # Get the file extension
    file_extension = os.path.splitext(data.get('path'))[-1][1:]

    # Ensure the file's extension is lowercase
    file_extension = file_extension.lower()

    # If this is flash video file, add it to pending tasks
    if file_extension.lower() in ['m4v']:
        data['add_file_to_pending_tasks'] = True
        logger.debug("File is .m4v - true")

    if file_extension.lower() in ['mkv']:
        data['add_file_to_pending_tasks'] = False
        logger.debug("File already is .mkv - failed")


    return data





