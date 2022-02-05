"""
    Written by:               sparten9999
    Date:                     23 Jan 2022, (04:10 PM)
 
    Copyright:
        Copyright (C) 2022 sparten9999
        This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
        Public License as published by the Free Software Foundation, version 3.
        This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
        implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
        for more details.
        You should have received a copy of the GNU General Public License along with this program.
        If not, see <https://www.gnu.org/licenses/>.
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# to do / notes
#   
#  raise exception doesnt stop other plugins in stack from running after? not actually a problem?
#

#   rename 'test_plugin' to final name
#   
#   add button to erase data.csv and the temp dict   - i dont think buttons are allowed
#       turns out temp dict is reset when the plugin is enabled
#
#
#
#   would be nice to set a percent to reject,
#       example I would rather keep the original file if the size reduction is  10% or lower
#
# if the plugin stack fails somewhere else then the test_plugin_dict will get larger over time



#   ?what happens if file is remuxed or name change?
#   so i think if you do data['add_file_to_pending_tasks'] = True it will force it to the queue and skip further tests

# add some documentation like if you are using this plugin it has to be ran with no existing items in pending tasks or else 
#       it wont make the csv right or have the start time
#
#
#   by putting the add time in the library test its actually getting the job add time not the job start time
#       would have have this plugin be before transocder in worker process to get time. then convert the current worker process to be a later one
#
#
# it didnt seem to make header row for 1 person?

#   have it check both path/filename AND size incase you upgrade a file later
#
#
#
# convert to the sizes to mb
#
#    headers = {"filename" : None, 
#            "original_size" : None,
#            "job_added_on" : None,
#            "transcoded_size": None,
#            "transcoded_time" : None,
#            "path" : None,
#            "sized_saved": None          
#
#               
#               }
#

#            
#
#
#




headers = {"filename" : None,         
        "original_size" : None,
            "job_added_on" : None,
            "transcoded_size": None,
            "transcoded_time" : None,
            "path" : None,
           "sized_saved": None          

               
               }




import random  # for testing only




# i dont know what i actually need here
import logging
import os
import shutil
from configparser import NoSectionError, NoOptionError
from unmanic.libs.directoryinfo import UnmanicDirectoryInfo
from unmanic.libs.unplugins.settings import PluginSettings
from marshmallow import Schema, fields, validate




import os.path
from os import path

import csv 

from datetime import datetime
from datetime import date

# Configure plugin logger
logger = logging.getLogger("Unmanic.Plugin.blacklist_files_larger_than_original")



blacklist_files_larger_than_original_dict = {}
logger.debug("blacklist_files_larger_than_original_dict set")






class Settings(PluginSettings):
    settings = {
        "Date Format": "date3",
        "Mark task as failure or continue processing" : "opt1",
    }
    form_settings = {
        "Date Format": {
            "input_type":     "select",
            "select_options": [
                {
                    'value': "date1",
                    'label': "05/04/2012",
                },
                {
                    'value': "date2",
                    'label': "May 1, 2015",
                },
                {
                    'value': "date3",
                    'label': "04/27/2018",
                },
                {
                    'value': "date4",
                    'label': "Apr-26, 2019",
                },
            ],
        },

        "Mark task as failure or continue processing": {
            "input_type":     "select",
            "select_options": [
                {
                    'value': "opt1",
                    'label': "If transcode is larger then original, fail immediatly and stop processing",
                },
                {
                    'value': "opt2",
                    'label': "If transcode is larger then original, reuse original file and continue processing (file is still blacklisted from being added to pending task later on rescan)",
                },

            ],
        },



    }

    
def convert_bytes(bytes_number):
    tags = [ "Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte" ]
 
    i = 0
    double_bytes = bytes_number
 
    while (i < len(tags) and  bytes_number >= 1024):
            double_bytes = bytes_number / 1024.0
            i = i + 1
            bytes_number = bytes_number / 1024
 
    return str(round(double_bytes, 2)) + " " + tags[i]


def getDate():
    #logger.debug("getDate called")
    settings = Settings()
    date_setting = settings.get_setting('Date Format')

    #logger.debug(date_setting)


    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()

    if date_setting == "date1":
        date_format = today.strftime("%d/%m/%Y")  #dd/mm/YY  16/09/2019
    elif date_setting == "date2":
        date_format = today.strftime("%B %d, %Y") #Textual month, day and year	 September 16, 2019
    elif date_setting == "date3":
        date_format = today.strftime("%m/%d/%y")  #mm/dd/yy    09/16/19
    elif date_setting == "date4":   
        date_format = today.strftime("%b-%d-%Y")  #Month abbreviation, day and year   Sep-16-2019	




    string = (date_format + " " + current_time) 

    #logger.debug(string)

    return string









def on_library_management_file_test(data):
    #logger.debug("on_library_management_file_test")
    #logger.warning("on_library_management_file_test")
    #logger.error("on_library_management_file_test")

    work_file = data.get('path')
    # Get the file extension
    file_extension = os.path.splitext(work_file)[-1][1:]
    file_path = data.get('path')
    file_name = os.path.basename(file_path)
    
    if file_name == 'TEST_FILE.mkv':
        logger.debug("test file detected")
        file_size =random.randint(1, 5)
    else:
        file_size = os.path.getsize(file_path)
    # Ensure the file's extension is lowercase
    file_extension = file_extension.lower()


    status = csvReadFunction(file_path,file_size)
#    status = True # for making it ignore the results of the if the item is in the blacklist




  


    #only attempt to log stuff if it gets added to queue
    if status == True:
        global blacklist_files_larger_than_original_dict
        blacklist_files_larger_than_original_dict[file_path] = getDate()

      #  logger.debug("test point 1: ")
      #  logger.debug(len(blacklist_files_larger_than_original_dict))
    else: 
        data['add_file_to_pending_tasks'] = False
        #data['issues'] = "" gotta figure this out


 
    #data['add_file_to_pending_tasks'] = status



    return data









def csvReadFunction(file_path,file_size):
    #logger.debug("csvReadFunction called")
    csvfilePath = "/config/.unmanic/userdata/blacklist_files_larger_than_original/data.csv"
    status = "none"
#    headers = {"filename" : None, 
#            "original size" : None,
#            "added_on" : None,
#            "transcoded_size": None,
#            "transcoded_time" : None,
#            "path" : None          
#            }
    #Check if file exists. if not create it
    if (os.path.exists(csvfilePath) == False): 
        with open(csvfilePath, 'w') as csvfile: 
            # creating a csv writer object                                     
            csvwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=headers)
            # writing the header 
            csvwriter.writeheader()
            csvfile.close()
            logger.warning("data.csv not found, file created.")
            #since file doesnt exist yet there is no need to check it for a blacklist
            status = True
            return status
    else:
        logger.debug("data.csv found.")



    logger.debug("checking blacklist for file")

 

    reader = csv.DictReader(open(csvfilePath))

    for row in reader:
       # logger.debug(row) #displays all rows
        path = row['path']
        size = row['original_size']
        
      #  logger.debug("test point 5: ")
       # logger.debug(path)

        if  path == file_path:
            #logger.debug('existing path found = ' + path)
            if convert_bytes(size) == str(file_size):
                #logger.debug('matching size found = ' + size)
                logger.debug('MATCH - FILE HAS BEEN BLACKLISTED ALREADY SKIP')
                status = False

                break
            else:
                logger.debug('FAIL - matching path but different size')
                status = True
        else:
            #logger.debug('non match continuing search')
            status = True

    if status == "none":
        logger.debug('file empty')
        status = True



    #logger.debug('status = ')        
    #logger.debug(status)
           

   # logger.debug("csvreader finished")


    return status






def csvWriteFunction(x):  #will be added inline later. i dont think i need a special function for this
    #logger.debug("csvWriteFunction called")
    csvfilePath = "/config/.unmanic/userdata/blacklist_files_larger_than_original/data.csv"
#    headers = {"filename" : None, 
#            "original size" : None,
#            "added_on" : None,
#            "transcoded_size": None,
#            "transcoded_time" : None,
#            "path" : None          
#            }








            
    with open(csvfilePath, 'a+') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.DictWriter(csvfile, fieldnames=headers) 
        csvwriter.writerow(x)
        csvfile.close()
    return 






def on_worker_process(data):
    #logger.debug("on_worker_process started")
    global blacklist_files_larger_than_original_dict


    settings = Settings()
    mark_as_setting = settings.get_setting('Mark task as failure or continue processing')
    #opt1 = fail out and stop processing
    #opt2 = reuse original file and continue 





    # Get the original file stats
    original_file_path = data.get('original_file_path')
    original_file_stats = os.stat(os.path.join(original_file_path))
    original_file_size = original_file_stats.st_size
    file_name = os.path.basename(original_file_path)

    # Current cache file stats
    file_in = data.get('file_in')
    working_file_stats = os.stat(os.path.join(file_in))
    working_file_size = working_file_stats.st_size

    added_on = "error"

    if working_file_size > original_file_size:
        logger.debug("NEW FILE BIGGER DISCARD CHANGES")

        logger.debug(original_file_path)
        logger.debug(blacklist_files_larger_than_original_dict)


        if original_file_path in blacklist_files_larger_than_original_dict:
            logger.debug("e12: dict key match found")
            added_on = blacklist_files_larger_than_original_dict[original_file_path]
            #DELETE THIS KEY FROM THE DICT \/ so it doesnt get bigger and bigger
           # logger.debug(blacklist_files_larger_than_original_dict)
            blacklist_files_larger_than_original_dict.pop(original_file_path)
           # logger.debug(blacklist_files_larger_than_original_dict)



        else:
            logger.error("e14: error no key match found: this shouldnt happen?") 

        row = {            "filename" : file_name, 
                      "original_size" : original_file_size,
                       "job_added_on" : added_on,
                     "transcoded_size": working_file_size,
                    "transcoded_time" : getDate(),
                               "path" : original_file_path          
                         }


        sized_saved = working_file_size - original_file_size

        row = {            "filename" : file_name, 
                      "original_size" : convert_bytes(original_file_size),
                       "job_added_on" : added_on,
                     "transcoded_size": convert_bytes(working_file_size),
                    "transcoded_time" : getDate(),
                         "sized_saved": convert_bytes(sized_saved),          
                               "path" : original_file_path          
                         }


                   




        csvWriteFunction(row) #log file, size, and times


    # here is where the option for continuing processing would go
        if mark_as_setting == "opt1": 
            logger.debug("transcoded file larger. stopping further processing") 
            raise Exception ("FAIL because of transcoded file is larger then orginal file")                
        else:
            logger.debug("transcoded file larger. copying original file into workspace and continue processing") 
            data['exec_command'] = [
            'cp',
            '-fv',
            original_file_path,
            data.get('file_out')
            ]


    else:    #if new file is smaller then original do this
        if original_file_path in blacklist_files_larger_than_original_dict:
            logger.debug("d13: dict key match found")

            #DELETE THIS KEY FROM THE DICT \/ so it doesnt get bigger and bigger

            #logger.debug("test point 9: ")
            #logger.debug(blacklist_files_larger_than_original_dict)
            blacklist_files_larger_than_original_dict.pop(original_file_path)
           # logger.debug(blacklist_files_larger_than_original_dict)



        else:
            logger.error("e15: error no key match found: this shouldnt happen?") 







    #logger.debug("test point 2: ")
    #logger.debug(len(blacklist_files_larger_than_original_dict))


    return data

















