# 7DaysToBan  

A small python script for a 7DaysToDieServer to make it easier to ban people from the Server after they left.  

to start, use  
`python3 blacklist.py`  

On first startup, you will be asked to define your output_log directory, which is usually the 7DaysToDieServer_Data directory within your 7DaysToDie Server installation, and the directory where the serveradmin.xml file is located, which is usually the Saves directory within your UserDataFolder.  
This information will be saved in a file named "config.json" in the same directory as the script.  

On every startup, the script will read the config.json file and use the information to connect to the server, and will start scanning your log files for users that have ever played on your Server (note if you have a lot of log files this might take a moment) and give you a selection of all users. Simply type in the number of the user that shall be banned and you (or better they) are done ;)  

the script also creates a backup of the serveradmin.xml called serveradmin.xml.bak in the same directory, so if something went wrong you can revert it.  

I'll be honest here, this was a quick thing to help someone, so its mostly done by blackbox.ai and i just fixed it. It's nothing fancy and you can change it according to your needs.  

Tested on python3.8 on linux, so please report back if there is issues with other python versions or OS.  
