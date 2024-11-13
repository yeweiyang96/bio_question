import os

from Bio import SeqIO

import DB_Manager

if __name__ == '__main__':
    db_name = 'prokaryotes.db'
    prokaryote_name = ['GCF_000005845_2', 'GCF_000008865_2']

    try:
        for name in prokaryote_name:
            DB_Manager.build_table(db_name, name)
            DB_Manager.import_data(db_name, name)
        print('Initialization successful')
    except Exception as e:
        # rollback operation
        print('initialization failed.', e)
        DB_Manager.delete_tables(db_name, prokaryote_name)

