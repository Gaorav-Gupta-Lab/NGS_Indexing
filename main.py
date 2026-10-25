"""

"""
import random

def rcomp(seq):
    """
    Reverse complement our sequence.  This is code copied and modified from BioPython.
    :param seq:
    :return:
    """

    ambiguous_dna_complement = {
        "A": "T",
        "C": "G",
        "G": "C",
        "T": "A",
        "M": "K",
        "R": "Y",
        "W": "W",
        "S": "S",
        "Y": "R",
        "K": "M",
        "V": "B",
        "H": "D",
        "D": "H",
        "B": "V",
        "X": "X",
        "N": "N",
    }
    complement_mapping = ambiguous_dna_complement
    before = ''.join(complement_mapping.keys())
    after = ''.join(complement_mapping.values())
    before += before.lower()
    after += after.lower()
    ttable = str.maketrans(before, after)
    comp_seq = ''.join(reversed(seq.translate(ttable)))

    return comp_seq

def build_index(index_name):
    """
    Returns dictionary of index names and sequences required for index selection.
    :param index_name:
    :return:
    """
    i5_keys = []
    i7_keys = []
    sample_index_dict = {}

    if index_name == "trueseq":
        tmp_dict = {
            'D501': 'AGGCTATA',
            'D502': 'GCCTCTAT',
            'D503': 'AGGATAGG',
            'D504': 'TCAGAGCC',
            'D505': 'CTTCGCCT',
            'D506': 'TAAGATTA',
            'D507': 'ACGTCCTG',
            'D508': 'GTCAGTAC',
            'D701': 'CGAGTAAT',
            'D702': 'TCTCCGGA',
            'D703': 'AATGAGCG',
            'D704': 'GGAATCTC',
            'D705': 'TTCTGAAT',
            'D706': 'ACGAATTC',
            'D707': 'AGCTTCAG',
            'D708': 'GCGCATTA',
            'D709': 'CATAGCCG',
            'D710a': 'GTCATCGA',
            'D711': 'GCGCGAGA',
            'D712': 'CTATCGCT'
        }

        for key, value in tmp_dict.items():
            if "D7" in key:
                value = rcomp(value)
                i7_keys.append(key)
            else:
                i5_keys.append(key)
            sample_index_dict[key] = value

    else:
        tmp_udp_dict = {
            'UDP5_0105': 'TGTGATGTAT',
            'UDP5_0289V2': 'GGCACGCCAT',
            'UDP5_0336': 'TCGAATGGAA',
            'UDP5_0296': 'CTTATACCTG',
            'UDP5_0124': 'TATGGCTCGA',
            'UDP5_0118': 'TAACCGCCGA',
            'UDP5_0329': 'AGGTTGCAGG',
            'UDP5_0112': 'CCAACAACAT',
            'UDP5_0332': 'ATTGACACAT',
            'UDP5_0115': 'CGGCTAACGT',
            'UDP7_0105': 'ACGATTGCTG',
            'UDP7_0289V2': 'GCTACTATCT',
            'UDP7_0336': 'TTGAGCCTAA',
            'UDP7_0296': 'TCCTTCATAG',
            'UDP7_0124': 'GGTAACGCAG',
            'UDP7_0118': 'GAACAAGTAT',
            'UDP7_0329': 'CGGCAAGCTC',
            'UDP7_0112': 'GTAGCCATCA',
            'UDP7_0332': 'GCAACAGGTG',
            'UDP7_0115': 'AGAGCTGCCT'
        }

        for key, value in tmp_udp_dict.items():
            if "UDP7" in key:
                i7_keys.append(key)
                value = rcomp(value)
            else:
                i5_keys.append(key)
            sample_index_dict[key] = value

    return sample_index_dict, i5_keys, i7_keys

def main():
    num_libraries = 5
    input_folder = output_folder = "output"
    project_name = ""
    previous_output_file = ""
    index_name = "trueseq"

    sample_index_dict, i5_keys, i7_keys = build_index(index_name)
    all_indices = []

    for i5_key in i5_keys:
        i5_seq = sample_index_dict[i5_key]
        for i7_key in i7_keys:
            i7_seq = sample_index_dict[i7_key]
            index_id = "{}+{}".format(i5_key, i7_key)
            index_seq = "{}+{}".format(i5_seq, i7_seq)
            all_indices.append(tuple([index_id, index_seq]))

    used_indices = random.sample(all_indices, num_libraries)

    output_string = "Index ID\tManifest Sequence\n"
    for index_tuples in used_indices:
        output_string += "{}\t{}\n".format(index_tuples[0], index_tuples[1])
    print(output_string)


if __name__ == '__main__':
    main()

