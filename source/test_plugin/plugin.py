#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# to do / notes
#   work on
#  raise exception doesnt stop other plugins in stack from running after
#
#
#
# a setting to  mark as failed or succuss based on if it will keep new file
#


import random  # for testing only



import logging
import os
import shutil
from configparser import NoSectionError, NoOptionError




from unmanic.libs.directoryinfo import UnmanicDirectoryInfo
from unmanic.libs.unplugins.settings import PluginSettings



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
    """
    Runner function - enables additional actions during the library management file tests.

    The 'data' object argument includes:
        path                            - String containing the full path to the file being tested.
        issues                          - List of currently found issues for not processing the file.
        add_file_to_pending_tasks       - Boolean, is the file currently marked to be added to the queue for processing.

    :param data:
    :return:
    
    """
    headers = {"filename" : None, 
            "original size" : None,
            "added_on" : None,
            "transcoded_size": None,
            "transcoded_time" : None,
            "path" : None          
            }

# name of csv file 
    csvfilePath = "/config/.unmanic/userdata/test_plugin/data.csv"


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





    status = True









    status = csvReadFunction(file_path,file_size)

    data['add_file_to_pending_tasks'] = status









  #  temp_dict = {file_path : getDate() }
  #  logger.debug(temp_dict)
    global test_plugin_dict
    test_plugin_dict[file_path] = getDate()


    #logger.debug("test_plugin_dict = ")
    #logger.debug(test_plugin_dict)
    test_plugin_dict[file_path + " 2"] = getDate()
    test_plugin_dict[file_path + " 3456"] = getDate()
    test_plugin_dict[file_path + " 23422"] = getDate()
    
    

    






  


    return data





def csvReadFunction(file_path,file_size):
   # logger.debug("csvReadFunction")
    csvfilePath = "/config/.unmanic/userdata/test_plugin/data.csv"
    status = False
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
            # writing the fields 
            csvwriter.writeheader()
            csvfile.close()
            logger.debug("data.csv does not exist and has been created. doesnt need to check farther")

            status = True
            return status

    logger.debug("checking")

    a='file_23'     #String that you want to search
#csvfilePath
    with open(csvfilePath, 'r') as csvfile: 
        x = csv.DictReader(csvfile)

        for row in x:
           # logger.debug(row) #displays all rows
            path = row['path']
            size = row['original size']
            
           # logger.debug(path)

            if  path == file_path:
                #logger.debug('existing path found = ' + path)
               # logger.debug(type(file_size))
               # logger.debug(type(size))

                if size == str(file_size):
                    #logger.debug('matching size found = ' + size)
                   # logger.debug('match - ' + path)
                    logger.debug('MATCH - FILE HAS BEEN BLACKLISTED ALREADY SKIP')
                    status = False

                    break
                else:
                    logger.debug('FAIL - matching path - different size')
                    status = True

            else:
                logger.debug('no match')
                status = True

    logger.debug("finished")
    csvfile.close()


    return status






def csvWriteFunction(x):
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
    logger.debug("on_worker_process started")


    



   # logger.debug('original_file_path = ' + original_file_path)


    # Get the original file stats
    original_file_path = data.get('original_file_path')
    original_file_stats = os.stat(os.path.join(original_file_path))
    original_file_size = original_file_stats.st_size
    file_name = os.path.basename(original_file_path)



    # Current cache file stats
    file_in = data.get('file_in')
    working_file_stats = os.stat(os.path.join(file_in))
    working_file_size = working_file_stats.st_size


    #logger.debug( working_file_stats)
    #logger.debug( original_file_stats)

    if working_file_size > original_file_size:
        logger.debug("NEW FILE BIGGER DISCARD CHANGES")
        # The current file is larger than the original. Reset the cache file to the file in


        added_on = "error"
        temp_dict = dict(test_plugin_dict)
        for x in temp_dict:
            logger.debug(x + " : " + temp_dict[x]) 
            if x == original_file_path:
                logger.debug("dict key match found")
                added_on = test_plugin_dict[x]
                row = {        "filename" : file_name, 
                          "original size" : original_file_size,
                               "added_on" : added_on,
                         "transcoded_size": working_file_size,
                        "transcoded_time" : getDate(),
                                   "path" : original_file_path          
                         }
                #DELETE THIS KEY FROM THE DICT \/
                test_plugin_dict.pop(x)

                csvWriteFunction(row) #dont need this here jsut for testing



                break



            else:     
                logger.debug("no key match found") 



      


        raise Exception ("FAIL because of something")                

         
    else:    
        logger.debug("New file smaller - keeping changes")




    return data











