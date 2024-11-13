import sqlite3

import pandas as pd

absolute_path = 'data/'


def find_cds_position(db_name, table):
    con = sqlite3.connect(absolute_path+db_name)
    cur = con.cursor()
    result = cur.execute("SELECT start_position, end_position FROM " + table).fetchall()
    con.close()
    return result


# building a DataFrame Format Data for distribution of lengths.
def build_distribution_dataframe(name, operons):
    operons_group = [name for _ in range(len(operons))]
    list_of_tuples = list(zip(operons_group, [operons[i][-1] - operons[i][0] for i in range(len(operons))]))
    df = pd.DataFrame(list_of_tuples, columns=['group', 'length'])
    return df


def find_candidate_operon(db_name, prokaryotes_name):
    operons = []
    position_list = find_cds_position(db_name, prokaryotes_name)
    for cds in position_list:
        start = cds[0]
        end = cds[1]
        if operons and (start - operons[-1][-1] <= 100):
            # distance of 100 bases or fewer (include minus)
            operons[-1].append(end)
        else:
            # new group
            operons.append([start, end])
    return operons


def size_of_fragments_obtained(sites, seq_length, linear=True):
    # Calculate the length of each fragment of prokaryotic dna treated with Biopython.Restriction,
    # distinguish between linear and circular.
    prev = 1
    lens = []

    if linear:
        for frag in sites:
            lens.append(frag - prev)
            prev = frag
        lens.append(seq_length + 1 - prev)
    else:
        for frag in sites:
            lens.append(frag - prev)
            prev = frag
        lens[0] = lens[0] + (seq_length + 1 - prev)
    return lens


def read_cds_data(db_name, table):
    con = sqlite3.connect(absolute_path+db_name)
    cur = con.cursor()
    res = cur.execute("SELECT locus_tag, definition, translation, seq FROM "+table).fetchall()
    con.close()
    return res



