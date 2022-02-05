if the transcoded video size would be larger then the original file size it would log the file path, original file size, and new file size to data.csv

there is 2 modes to this plugin. 
    mode 1  if the new file would be larger then it would stop proccessing immediately and be marked as failed in the completed tasks list
    mode 2  if the new file would be larger it would reuse the original video file and continue processing. (so if you have an audio encoder after this plugin
                it   should continue and do the audio encode still)
in both modes the above information is still logged and if the path and file name are the same then when you rescan your library it wont ever get readded to your 
    pending tasks list.

for this plugin to work properly it needs to be started with a clean pending tasks list or else data will not get logged.
    you will have to let all entries encode again so it can see the new file size and log the data.
    disable the "Reject File if Larger than Original" plugin as this does something similar
your plugin flow should be 
    Library Management - File test > blacklist should be at the top of the list. 
    Worker - Processing File > blacklist should be right after your video encoder (the video encoder and blacklist should be first
                                    2 in the stack if you want to continue processing wiht other plugins i think)

to reprocess a blacklisted file
    to remove an entry from the blacklist find the entry in the data.csv file and delete it 
    if you used mode 1 and let it be marked as failed then find it in completed tasks list and remove it from there
    rescan library should allow it to be readded to pending tasks

if you have any questions/concerns im in the unmanic discord as "sparten9999#0146" 
    I made this in my spare time so if I dont reply back right away im sorry.

Notes: 
    if you see a raised exception from this plugin in the logs that is normal when using mode 1. 
    use at your own risk. this plugin shouldnt break anything but please try to test with a few problem files first to see if it works for you
    date/time isnt really being used for much other then being logged to the csv.
    