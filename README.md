# BoxMongoDBMySQLSync
### Project for MSDS7330 to synchronize files across Box.com and local MySQL and MongoDB databases.
##### Dana Geislinger
##### MSDS7330 Final Project
##### 8/13/2018

## Synchronization
The synchronization script was created with the intent of synchronizing files between MySQL, MongoDB, and Box.com. By running *sync.py*, you will first be prompted to authenticate your Box.com account and allow access to your files for the Box app. Then, the script will automatically synchronize all files between the 3 data sources. Any files found in one of the databases will be mirrored to the other two if they do not exist there. Furthermore, the script will update files in each database if a more updated version of the file was found in the other database. Since Box.com does not allow more than one file with the same name per folder, this script is not designed to synchronize multiple files with the same name.

## REST Service
This REST service is designed to take a file as an argument, and upload it across MySQL, MongoDB, and Box.com at the same time. The file will be synchronized as well; duplicate files will not be uploaded and existing files will be updated only if the version to upload is newer.

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
2. Run *rest_upload.py*, with the file you want to upload as an argument to the script.
  * Dragging a file onto *rest_upload.py* in the file explorer is the easiest way to do this.
  * If no file is provided as an argument, the default file in config.ini under [REST] will be used.
3. The REST service has now synchronized the file across all platforms, and files should be accessible from any of the three.

# Notes
* MySQL may not accomodate large files. The data type is set to LONGBLOB, which should accomodate files up to 4GB, but I have had issues synchronizing large files.
* Your Box.com username or password is never shared with scripts in this package, (authentication is handled only by the official Box website), but the script does store tokens allowing the script access to your Box files. These keys are stored insecurely in 'cache/auth.pkl'. The cache folder can be deleted after running the script if you do not wish these tokens to be stored locally. If the cache is deleted, you will need to re-authenticate through Box.com the next time the script is run.
