import os
import shutil
import hashlib # it will be used for MD5 checks
import time


def sync_folders(source, replica):
    """
    Synchronize two folders, maintaining an identical copy of the source folder at the replica folder.
    """
    # Make sure the source and replica folders exist
    if not os.path.exists(source):
        raise ValueError("Source folder does not exist")
    if not os.path.exists(replica):
        os.makedirs(replica)

    # Loop through all files in the source folder
    for filename in os.listdir(source):
        src_path = os.path.join(source, filename)
        dst_path = os.path.join(replica, filename)

        # If the file is a directory, recursively synchronize it
        if os.path.isdir(src_path):
            sync_folders(src_path, dst_path)

        # Otherwise, copy the file to the replica folder
        else:
            shutil.copy2(src_path, dst_path)

    # Remove any files or directories in the replica folder that do not exist in the source folder
    for filename in os.listdir(replica):
        src_path = os.path.join(source, filename)
        dst_path = os.path.join(replica, filename)

        if not os.path.exists(src_path):
            if os.path.isdir(dst_path):
                shutil.rmtree(dst_path)
            else:
                os.remove(dst_path)

    # Set the synchronization interval (in seconds)
    sync_interval = 60 * 60  # 1 hour

    # Loop indefinitely, synchronizing the folders periodically
    while True:
        sync_folders(source, replica)
        time.sleep(sync_interval)
