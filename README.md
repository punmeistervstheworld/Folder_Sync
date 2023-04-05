# Folder_Sync

This is the first version of the Folder Sync program meant for the VEEAM job application written in the Python programming language.

The program maintains a full, identical copy of source folder at replica folder as follows:

1. Synchronization is one-way: after the synchronization content of the replica folder should be modified to exactly match content of the source folder. In case the replica folder does NOT exist, the progam will automatically create the replica folder complete with the source contents.
2. Synchronization is performed periodically at the users' needs (in seconds).
3. File creation/copying/removal operations are logged to a file and to the console output.
4. Folder paths, synchronization interval and log file path are provided through command line arguments as follows:

python sync_folders.py source_path replica_path log_path interval

For example: python sync_folders.py C:\Users\thema\Desktop\Source C:\Users\thema\Desktop\Replica C:\Users\thema\Desktop\logfile.log 60

Libraries used: 
1. os (for navigating the OS);
2. shutil (for high-level file operations, such as copying and deleting);
3. time (for logging/console timestamps)
4. argparse (necessary for providing the command line arguments for the folders path, log file path and time interval)
5. logging (for creating the logs)





