import os
import shutil
import time
import argparse
import logging
import hashlib

time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def compare_files(file1, file2):
    # This function compares two files with their hashes. We will open the files only for reading in a binary format,
    # or rb for short.
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest():
                return True
            else:
                return False


def compare_folders(source, replica):
    # compare hash source
    # it either returns True if all files are the same, or false if any of the files are different.
    # get all files in source
    files_source = os.listdir(source)
    # get all files in replica
    files_replica = os.listdir(replica)
    # compare 2 list
    if len(files_source) != len(files_replica):
        return False

    for file in files_source:
        if file in files_replica:
            if not compare_files(source + '/' + file, replica + '/' + file):
                return False
        else:
            return False
    return True


def synchronize_folders(source_path, replica_path, log_path, interval):
    logging.basicConfig(filename=log_path, level=logging.INFO)

    while True:
        logging.info("Synchronization started at %s", time_now)

        for dirpath, dirnames, filenames in os.walk(source_path):
            relative_path = os.path.relpath(dirpath, source_path)
            replica_dirpath = os.path.join(replica_path, relative_path)

            if not os.path.exists(replica_dirpath):
                os.makedirs(replica_dirpath)
                logging.info("Created directory %s", replica_dirpath)

            for filename in filenames:
                source_filepath = os.path.join(dirpath, filename)
                replica_filepath = os.path.join(replica_dirpath, filename)

                if os.path.exists(replica_filepath):
                    if os.path.getmtime(source_filepath) > os.path.getmtime(replica_filepath):
                        shutil.copy2(source_filepath, replica_filepath)
                        logging.info("Copied %s to %s", source_filepath, replica_filepath)
                else:
                    shutil.copy2(source_filepath, replica_filepath)
                    logging.info("Copied %s to %s", source_filepath, replica_filepath)

            for dirname in dirnames:
                source_dirpath = os.path.join(dirpath, dirname)
                replica_dirpath = os.path.join(replica_path, relative_path, dirname)

                if not os.path.exists(replica_dirpath):
                    os.makedirs(replica_dirpath)
                    logging.info("Created directory %s", replica_dirpath)

        for dirpath, dirnames, filenames in os.walk(replica_path):
            relative_path = os.path.relpath(dirpath, replica_path)
            source_dirpath = os.path.join(source_path, relative_path)

            if not os.path.exists(source_dirpath):
                shutil.rmtree(dirpath)
                logging.info("Removed directory %s", dirpath)

            for filename in filenames:
                replica_filepath = os.path.join(dirpath, filename)
                source_filepath = os.path.join(source_dirpath, filename)

                if not os.path.exists(source_filepath):
                    os.remove(replica_filepath)
                    logging.info("Removed file %s", replica_filepath)

        logging.info("Synchronization ended at %s", time_now)

        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("source_path", help="path to source folder")
    parser.add_argument("replica_path", help="path to replica folder")
    parser.add_argument("log_path", help="path to log file")
    parser.add_argument("interval", type=int, help="synchronization interval in seconds")
    args = parser.parse_args()

    synchronize_folders(args.source_path, args.replica_path, args.log_path, args.interval)
