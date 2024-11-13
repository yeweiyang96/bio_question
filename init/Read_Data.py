import re

from Bio import SeqIO


# Getting Key and Value in record.description
def get_key_value(string: str):
    kv = string.split('=')
    k: str = kv[0][1:]
    v: str = kv[1][:-1]
    return k, v


def pseudo_is_in(full_str):
    regex = re.compile(r"\bpseudo\b")
    if regex.findall(full_str):
        return True
    else:
        return False


def get_protein_nucleotide_seq(table_name):
    result = {}
    regex = re.compile(r"\[.*?]")
    absolute_path = '/Users/wangzekun/bioinfomatics/data/'
    records = SeqIO.parse(absolute_path+table_name+"/cds_from_genomic.fna", "fasta")
    for record in records:
        if pseudo_is_in(record.description):
            continue
        qualifiers = regex.findall(record.description)
        for qualifier in qualifiers:
            key, value = get_key_value(qualifier)
            if key == 'protein_id':
                result[value] = str(record.seq)
                break
    return result


def get_chromosome_name(record_id):
    regex = re.compile(r"NC_.*?\.\d")
    return regex.match(record_id)


def integrate_data(name):
    # Add nucleotide sequences to genbank format data. name is prokaryote's id
    # Take only the first chromosome
    absolute_path = '/Users/wangzekun/bioinfomatics/data/'
    record = next(SeqIO.parse(absolute_path + name + '/genomic.gbff', 'genbank'))
    index = 0
    all_cds = []
    cds_seq = get_protein_nucleotide_seq(name)
    for feature in record.features:
        if feature.type == "CDS":
            try:
                cds = (feature.qualifiers['locus_tag'][0],
                       feature.qualifiers['product'][0],
                       feature.qualifiers['protein_id'][0],
                       feature.qualifiers['translation'][0],
                       int(feature.location.start),
                       int(feature.location.end),
                       cds_seq[feature.qualifiers['protein_id'][0]])
                all_cds.append(cds)
            except BaseException:
                # filter out pseudogenes
                index += 1
                continue
    print("pseudo: ", index)
    return all_cds
