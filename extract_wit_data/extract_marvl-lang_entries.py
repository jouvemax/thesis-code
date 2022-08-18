import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wit_tsv_path', type=str)
    parser.add_argument('--output_path', type=str)
    args = parser.parse_args()

    wit_tsv_path = args.wit_tsv_path
    output_path = args.output_path

    raw_entries_1 = pd.read_csv(wit_tsv_path + '/wit_v1.train.all-00000-of-00010.tsv', sep='\t')

    raw_entries_2 = pd.read_csv(wit_path + '/wit_v1.train.all-00001-of-00010.tsv', sep='\t')
    raw_entries_2.index += len(raw_entries_1)

    raw_entries_3 = pd.read_csv(wit_path + '/wit_v1.train.all-00002-of-00010.tsv', sep='\t')
    raw_entries_3.index += len(raw_entries_1) + len(raw_entries_2)

    raw_entries_4 = pd.read_csv(wit_path + '/wit_v1.train.all-00003-of-00010.tsv', sep='\t')
    raw_entries_4.index += len(raw_entries_1) + len(raw_entries_2) + len(raw_entries_3)

    raw_entries_5 = pd.read_csv(wit_path + '/wit_v1.train.all-00004-of-00010.tsv', sep='\t')
    raw_entries_5.index += len(raw_entries_1) + len(raw_entries_2) + len(raw_entries_3) + len(raw_entries_4)

    half_length = len(raw_entries_1) + len(raw_entries_2) + len(raw_entries_3) + len(raw_entries_4) + len(raw_entries_5)

    raw_entries_6 = pd.read_csv(wit_path + '/wit_v1.train.all-00005-of-00010.tsv', sep='\t')
    raw_entries_6.index += half_length

    raw_entries_7 = pd.read_csv(wit_path + '/wit_v1.train.all-00006-of-00010.tsv', sep='\t')
    raw_entries_7.index += half_length + len(raw_entries_6)

    raw_entries_8 = pd.read_csv(wit_path + '/wit_v1.train.all-00007-of-00010.tsv', sep='\t')
    raw_entries_8.index += half_length + len(raw_entries_6) + len(raw_entries_7)

    raw_entries_9 = pd.read_csv(wit_path + '/wit_v1.train.all-00008-of-00010.tsv', sep='\t')
    raw_entries_9.index += half_length + len(raw_entries_6) + len(raw_entries_7) + len(raw_entries_8)

    raw_entries_10 = pd.read_csv(wit_path + '/wit_v1.train.all-00009-of-00010.tsv', sep='\t')
    raw_entries_10.index += half_length + len(raw_entries_6) + len(raw_entries_7) + len(raw_entries_8) + len(raw_entries_9)


    def get_lang_entries(lang):
        lang_entries_1 = raw_entries_1[raw_entries_1.language == lang]
        lang_entries_2 = raw_entries_2[raw_entries_2.language == lang]
        lang_entries_3 = raw_entries_3[raw_entries_3.language == lang]
        lang_entries_4 = raw_entries_4[raw_entries_4.language == lang]
        lang_entries_5 = raw_entries_5[raw_entries_5.language == lang]
        lang_entries_6 = raw_entries_6[raw_entries_6.language == lang]
        lang_entries_7 = raw_entries_7[raw_entries_7.language == lang]
        lang_entries_8 = raw_entries_8[raw_entries_8.language == lang]
        lang_entries_9 = raw_entries_9[raw_entries_9.language == lang]
        lang_entries_10 = raw_entries_10[raw_entries_10.language == lang]

        lang_entries_concat = pd.concat([lang_entries_1,
                                        lang_entries_2,
                                        lang_entries_3,
                                        lang_entries_4,
                                        lang_entries_5,
                                        lang_entries_6,
                                        lang_entries_7,
                                        lang_entries_8,
                                        lang_entries_9,
                                        lang_entries_10], 
                                        axis=0)

        lang_entries_concat.to_pickle("{l}_entries.pkl".format(l = lang))

    get_lang_entries("sw")
    get_lang_entries("ta")
    get_lang_entries("tr")
    get_lang_entries("id")
    get_lang_entries("zh")