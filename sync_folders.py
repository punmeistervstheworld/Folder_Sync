import os
import shutil
import time
import argparse
import logging

time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def sync_folders(source_path, replica_path, log_path, interval):
    logging.basicConfig(filename=log_path, level=logging.INFO)

    while True:
        print("Synchronization started at " + time_now)
        logging.info("Synchronization started at %s", time_now)

        for dirpath, dirnames, filenames in os.walk(source_path):
            relative_path = os.path.relpath(dirpath, source_path)
            replica_dirpath = os.path.join(replica_path, relative_path)

            if not os.path.exists(replica_dirpath):
                os.makedirs(replica_dirpath)
                print("Created directory " + replica_dirpath)
                logging.info("Created directory %s", replica_dirpath)

            for filename in filenames:
                source_filepath = os.path.join(dirpath, filename)
                replica_filepath = os.path.join(replica_dirpath, filename)

                if os.path.exists(replica_filepath):
                    if os.path.getmtime(source_filepath) > os.path.getmtime(replica_filepath):
                        shutil.copy2(source_filepath, replica_filepath)
                        print("Copied " + source_filepath + " to " + replica_filepath)
                        logging.info("Copied %s to %s", source_filepath, replica_filepath)
                else:
                    shutil.copy2(source_filepath, replica_filepath)
                    print("Copied " + source_filepath + " to " + replica_filepath)
                    logging.info("Copied %s to %s", source_filepath, replica_filepath)

            for dirname in dirnames:
                source_dirpath = os.path.join(dirpath, dirname)
                replica_dirpath = os.path.join(replica_path, relative_path, dirname)

                if not os.path.exists(replica_dirpath):
                    os.makedirs(replica_dirpath)
                    print("Created directory " + replica_dirpath)
                    logging.info("Created directory %s", replica_dirpath)

        for dirpath, dirnames, filenames in os.walk(replica_path):
            relative_path = os.path.relpath(dirpath, replica_path)
            source_dirpath = os.path.join(source_path, relative_path)

            if not os.path.exists(source_dirpath):
                shutil.rmtree(dirpath)
                print("Removed directory " + dirpath)
                logging.info("Removed directory %s", dirpath)

            for filename in filenames:
                replica_filepath = os.path.join(dirpath, filename)
                source_filepath = os.path.join(source_dirpath, filename)

                if not os.path.exists(source_filepath):
                    os.remove(replica_filepath)
                    print("Removed file " + replica_filepath)
                    logging.info("Removed file %s", replica_filepath)

        print("Synchronization ended at " + time_now)
        logging.info("Synchronization ended at %s", time_now)

        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("source_path", help="path to source folder")
    parser.add_argument("replica_path", help="path to replica folder")
    parser.add_argument("log_path", help="path to log file")
    parser.add_argument("interval", type=int, help="synchronization interval in seconds")
    args = parser.parse_args()

    sync_folders(args.source_path, args.replica_path, args.log_path, args.interval)
