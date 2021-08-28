#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     5 April 2021, (10:00 PM)
 
    Copyright:
        Copyright (C) 2021 Josh Sunnex

        This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
        Public License as published by the Free Software Foundation, version 3.

        This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
        implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
        for more details.

        You should have received a copy of the GNU General Public License along with this program.
        If not, see <https://www.gnu.org/licenses/>.

"""
from unmanic.libs.unplugins.settings import PluginSettings

from plexapi.server import PlexServer


class Settings(PluginSettings):
    settings = {
        'Plex URL':                'http://localhost:32400',
        'Plex Token':              '',
        'Notify on Task Failure?': False,
    }


def update_plex(plex_url, plex_token):
    plex = PlexServer(plex_url, plex_token)
    # Call to Plex to trigger an update
    plex.library.update()


def on_postprocessor_task_results(data):
    """
    Runner function - provides a means for additional postprocessor functions based on the task success.

    The 'data' object argument includes:
        task_processing_success         - Boolean, did all task processes complete successfully.
        file_move_processes_success     - Boolean, did all postprocessor movement tasks complete successfully.
        destination_files               - List containing all file paths created by postprocessor file movements.
        source_data                     - Dictionary containing data pertaining to the original source file.

    :param data:
    :return:
    
    """
    plugin_settings = Settings()

    if not data.get('task_processing_success') and not plugin_settings.get_setting('Notify on Task Failure?'):
        return data

    plex_url = plugin_settings.get_setting('Plex URL')
    plex_token = plugin_settings.get_setting('Plex Token')
    update_plex(plex_url, plex_token)

    return data