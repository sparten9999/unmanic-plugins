#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# to do / notes
#   
#  raise exception doesnt stop other plugins in stack from running after? not actually a problem?
#

#   rename 'test_plugin' to final name
#   add setting for date format
#   add button to erase data.csv and the temp dict
#   add setting to  mark as failed or succuss based on if it will keep new file
#   would be nice to set a percent to reject,
#       example I would rather keep the original file if the size reduction is  10% or lower
#
#
#  add setting that if new file is bigger that it will fail and stop all further processing 
#       or reuse original data and continue with the flow and mark as success (still add to blacklist so it wont be picked up again)
#


#   ?what happens if file is remuxed or name change?


import random  # for testing only




# i dont know what i actually need here
import logging
import os
#import shutil
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
logger = logging.getLogger("Unmanic.Plugin.test_plugin")



test_plugin_dict = {}






#class Settings(PluginSettings):
#    settings = {
#        "Boolean Option ":      True,
#        "Custom String Option": "",
#    }



def getDate():
   # logger.debug("getDate called")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()
    date1 = today.strftime("%d/%m/%Y")  #dd/mm/YY  16/09/2019
    date2 = today.strftime("%B %d, %Y") #Textual month, day and year	 September 16, 2019
    date3 = today.strftime("%m/%d/%y")  #mm/dd/y    09/16/19
    date4 = today.strftime("%b-%d-%Y")  #Month abbreviation, day and year   Sep-16-2019	

    string = (date3 + " " + current_time) 
   # logger.debug(string)

    return string









def on_library_management_file_test(data):
    #logger.debug("on_library_management_file_test")

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
        global test_plugin_dict
        test_plugin_dict[file_path] = getDate()

        logger.debug("test point 1: ")
        logger.debug(len(test_plugin_dict))
    



    data['add_file_to_pending_tasks'] = status










    return data









def csvReadFunction(file_path,file_size):
    logger.debug("csvReadFunction called")
    csvfilePath = "/config/.unmanic/userdata/test_plugin/data.csv"
    status = "none"
    headers = {"filename" : None, 
            "original size" : None,
            "added_on" : None,
            "transcoded_size": None,
            "transcoded_time" : None,
            "path" : None          
            }
    #Check if file exists. if not create it
    if (os.path.exists(csvfilePath) == False): 
        with open(csvfilePath, 'w') as csvfile: 
            # creating a csv writer object                                     
            csvwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=headers)
            # writing the header 
            csvwriter.writeheader()
            csvfile.close()
            logger.debug("data.csv not found, file created.")
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
        size = row['original size']
        
        logger.debug("test point 5: ")
        logger.debug(path)

        if  path == file_path:
            #logger.debug('existing path found = ' + path)
            if size == str(file_size):
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
           

    logger.debug("csvreader finished")


    return status






def csvWriteFunction(x):  #will be added inline later. i dont think i need a special function for this
    #logger.debug("csvWriteFunction called")
    csvfilePath = "/config/.unmanic/userdata/test_plugin/data.csv"
    headers = {"filename" : None, 
            "original size" : None,
            "added_on" : None,
            "transcoded_size": None,
            "transcoded_time" : None,
            "path" : None          
            }
    with open(csvfilePath, 'a+') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.DictWriter(csvfile, fieldnames=headers) 
        csvwriter.writerow(x)
        csvfile.close()
    return 






def on_worker_process(data):
    #logger.debug("on_worker_process started")

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

        if original_file_path in test_plugin_dict:
            logger.debug("dict key match found")
            added_on = test_plugin_dict[original_file_path]

            #DELETE THIS KEY FROM THE DICT \/ so it doesnt get bigger and bigger
           # logger.debug(test_plugin_dict)
            test_plugin_dict.pop(original_file_path)
           # logger.debug(test_plugin_dict)



        else:
            logger.debug("error no key match found: this shouldnt happen?") 

        row = {            "filename" : file_name, 
                      "original size" : original_file_size,
                           "added_on" : added_on,
                     "transcoded_size": working_file_size,
                    "transcoded_time" : getDate(),
                               "path" : original_file_path          
                         }


        csvWriteFunction(row) #log file, size, and times

        raise Exception ("FAIL because of transcoded file is larger then orginal file")                

         
    else:    #if new file is smaller then original do this
        if original_file_path in test_plugin_dict:
            logger.debug("dict key match found")

            #DELETE THIS KEY FROM THE DICT \/ so it doesnt get bigger and bigger

            #logger.debug("test point 9: ")
            #logger.debug(test_plugin_dict)
            test_plugin_dict.pop(original_file_path)
           # logger.debug(test_plugin_dict)



        else:
            logger.debug("error no key match found: this shouldnt happen?") 







    #logger.debug("test point 2: ")
    #logger.debug(len(test_plugin_dict))


    return data

















