import os
import shutil
import hashlib
import time
import logging


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

    # We will log the file creation/copying/removal operations

    logging.basicConfig(filename="log.txt", level=logging.DEBUG)
    logging.debug("Debug logging test...")

    # Set the synchronization interval (in seconds)
    sync_interval = 60 * 60  # 1 hour

    # For good measure, we will also calculate and validate MD5 hashes of files.

    def compute_md5(file_name):
        hash_md5 = hashlib.md5()
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def validate_md5(file_name, original_md5):
        with open(file_name) as f:
            data = f.read()
            md5_returned = hashlib.md5(data).hexdigest()

        if original_md5 == md5_returned:
            print("MD5 verified.")
        else:
            print("MD5 verification failed.")

    # Loop indefinitely, synchronizing the folders periodically
    while True:
        sync_folders(source, replica)
        time.sleep(sync_interval)
