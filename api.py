#!/usr/bin/env python3
import argparse
import os
import subprocess

def main():
    # Argparse code
    parser = argparse.ArgumentParser()
    parser.add_argument("-db", help="database name")
    parser.add_argument("-n", help="file name")
    args = parser.parse_args()
    db_name = args.db
    filename = args.n

    # print(db_name)
    # print(filename)

    for file_name in file_names:
        try:
            DB_Manager.build_table(db_name, file_name)
            DB_Manager.import_data(db_name, file_name)
        except Exception as e:
            # rollback operation
            print('initialization failed.', e)
            failed_tables.append(file_name)
            DB_Manager.delete_tables(db_name, file_name)

    if len(failed_tables) > 0:
        print('failed tables: ')
        print(failed_tables)
    else:
        print('initialization successful.')

if __name__ == "__main__":
    main()