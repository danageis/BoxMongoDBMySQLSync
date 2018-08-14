# BoxMongoDBMySQLSync
### Project for MSDS7330 to synchronize files across Box.com and local MySQL and MongoDB databases.
##### Dana Geislinger
##### MSDS7330 Final Project
##### 8/13/2018

## Synchronization
The synchronization script was created with the intent of synchronizing files between MySQL, MongoDB, and Box.com. By running *sync.py*, you will first be prompted to authenticate your Box.com account and allow access to your files for the Box app. Then, the script will automatically synchronize all files between the 3 data sources. Any files found in one of the databases will be mirrored to the other two if they do not exist there. Furthermore, the script will update files in each database if a more updated version of the file was found in the other database. Since Box.com does not allow more than one file with the same name per folder, this script is not designed to synchronize multiple files with the same name.

## REST Service
This REST service is designed to take a file as an argument, and upload it across MySQL, MongoDB, and Box.com at the same time.

# Setup Instructions
## Box.com
* Make sure you have a Box.com account (SMU provides this as part of your university account).
* Create a folder to sync files to on Box.com (can be anywhere in the folder structure) and record the folder_id in 'config.ini' under [Box] FolderID.

## MySQL
* Create the necessary schema by running 'setup.sql' in the 'setup' folder.
* Modify settings under [MySQL] in 'config.ini' as necessary for your system.

## MongoDB
* Modify settings under [MongoDB] in 'config.ini' as necessary for your system.
* Start a MongoDB instance before running any of the scripts in this package:
  * *mongod --dbpath 'path_to_your_mongodb_data_folder'*

## Python
* Developed and tested using Python 3.7 (should work fine with Python 2 as well).
* Install all modules listed in requirements.txt:
  * *pip install -r requirements.txt*
  
# Usage Instructions
## Synchronization
1. Update 'FolderID' under [Box] in *config.ini* to the folder you want to synchronize with on Box.com.
2. Run *sync.py*.
3. Authenticate your Box.com account to allow the script access to your files.
4. The script will automatically upload any missing files it finds between the 3 databases, and update any files that have newer versions in a different database.

## REST Service
1. Run *rest_server.py* to start the REST service HTTP server.
2. Update 'UploadPath' under [REST] in *config.ini* to reflect the file you want to upload.
3. Run *rest_upload.py*.
4. The REST service has now uploaded the file across all platforms, and files should be accessible from any of the three.

# Caveats
* The synchronization service was designed to be very robust in terms of duplicate files (files with the same name should be updated if they are more up to date than a file that already exists, and will be ignored otherwise). However, the REST service was designed to quickly upload files across the 3 platforms, and is not currently equipped to handle multiple files with the same name. As such, files that already exist on any of the platforms should not be uploaded to the REST service.
* There are likely undocumented filesize limitations associated with files uploaded using these tools with MySQL. Synchronizing files larger than 2-3 MB is currently not recommended.