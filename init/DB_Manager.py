import sqlite3
from init.Read_Data import integrate_data


def build_table(db_name, table_name):
    absolute_path = 'data/'
    con = sqlite3.connect(absolute_path+db_name)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS " + table_name + "(locus_tag TEXT , definition TEXT, protein_id TEXT "
                                                     "PRIMARY KEY,"
                                                     "translation TEXT, start_position INTEGER, "
                                                     "end_position INTEGER, seq TEXT)")
    con.commit()
    con.close()


def import_data(db_name, table_name):
    absolute_path = 'data/'
    con = sqlite3.connect(absolute_path+db_name)
    cur = con.cursor()
    batch_size = 500
    all_cds = integrate_data(table_name)
    for i in range(0, len(all_cds), batch_size):
        cur.executemany(
            "INSERT INTO " + table_name + "(locus_tag, definition, protein_id, translation, start_position, "
                                          "end_position, seq) VALUES (?, ?, ?,"
                                          "?, ?, ?, ?)",
            all_cds[i:i + batch_size])
    con.commit()
    return con.close()


def delete_tables(db_name, tables_name):
    absolute_path = 'data/'
    con = sqlite3.connect(absolute_path+db_name)
    cur = con.cursor()
    for table_name in tables_name:
        cur.execute("DROP TABLE "+table_name)
        print("Table dropped... ")
    con.commit()
    con.close()