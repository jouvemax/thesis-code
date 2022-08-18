import pickle as pkl
import json
from tqdm import tqdm
import argparse
import pandas as pd
from collections import defaultdict
import pyiwn
import zeyrek
import logging

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str)
    parser.add_argument('--lang', type=str)
    parser.add_argument('--path_to_captions', type=str, default=None)
    args = parser.parse_args()

    lang = args.lang

    lang_to_iso3 = {"sw": "swh", "ta": "tam", "tr": "tur", "id": "ind", "zh": "cmn"}

    wordnet_alignments = pd.read_csv("./wordnetwiktionaryalignments-2013-02-19.tsv", sep='\t',)

    print("There are {n} unique entries in WordNet.".format(n = len(wordnet_alignments)))

    pos_mapping = {"j": "ADJ", "r":"ADV", "n":"NOUN", "v": "VERB"}
    en_word_to_pos = defaultdict(lambda: set())

    for i, row in wordnet_alignments.iterrows():
        word = row.wtword
        pos = pos_mapping[row.pos]
        en_word_to_pos[word].add(pos)

    print("There are {n} unique words in WordNet.".format(n = len(en_word_to_pos)))

    en_lang = pd.read_csv("./eng2{l}.txt".format(l = lang_to_iso3[lang]), sep="\t", header=None)
    en_lang.rename(columns={0: "en", 1: lang}, inplace=True)
    en_lang = en_lang[en_lang.en != en_lang[lang]]

    en_lang_dict = {}
    lang_en_dict = {}

    for row in en_lang.iterrows():
        lang_word = row[1][lang]

        if lang == "sw":
            if lang_word.startswith("-"):
                lang_word = lang_word.replace("-", "")

        en_word = row[1].en

        if pd.isna(en_word):
            en_word = "nan"
        if pd.isna(lang_word):
            lang_word = "nan"

        pos_tags = en_word_to_pos[en_word]

        for tag in pos_tags:
            en_lang_dict[(en_word, tag)] = lang_word
            lang_en_dict[(lang_word, tag)] = en_word

    print("en -> {l} dict contains {n} (en_word, pos tag) -> {l}_word mappings.".format(l = lang, n = len(en_lang_dict)))
    non_composite_word_en = 0
    for key in en_lang_dict.keys():
        if " " not in key[0]:
           non_composite_word_en += 1
    print("    -> {n} non-composite en words. It excludes expression made of two or more words. \n".format(n = non_composite_word_en))

    print("{l} -> en dict contains {n} ({l}_word, pos tag) -> en_word mappings.".format(l = lang, n = len(lang_en_dict)))
    non_composite_word_lang = 0
    for key in lang_en_dict.keys():
        if " " not in key[0]:
           non_composite_word_lang += 1
    print("    -> {n} non-composite {l} words. It excludes expression made of two or more words. \n".format(l = lang, n = non_composite_word_lang))


    with open(args.output_dir + '/en_to_{l}_dict.pickle'.format(l = lang), 'wb') as handle:
        pkl.dump(en_lang_dict, handle, protocol=pkl.HIGHEST_PROTOCOL)

    with open(args.output_dir + '/{l}_to_en_dict.pickle'.format(l = lang), 'wb') as handle:
        pkl.dump(lang_en_dict, handle, protocol=pkl.HIGHEST_PROTOCOL)

    if lang == "tr" or lang == "ta":

        print("Computing reduced version of words for {l}.".format(l = lang))
        word_to_reduced_version = {}

        with open(args.path_to_captions) as f:
            lang_captions = json.load(f)

        unique_words = set()
        for key, caption in lang_captions.items():
            if "\n" in caption:
                caption = caption.replace("\n", " ")
            words = caption.split(" ")
            for word in words:
                unique_words.add(word.lower())

        lang_word_to_pos = defaultdict(lambda: set())
        for word, pos in lang_en_dict.keys():
            lang_word_to_pos[word].add(pos)
        
        print("There are {n} unique words in the {l} captions.".format(n = len(unique_words), l = lang))

        if lang == "ta":

            # Using the Tamil WordNet from IndoWordNet
            iwn_ta = pyiwn.IndoWordNet(lang=pyiwn.Language.TAMIL)

            for word in tqdm(unique_words):
                try:
                    synsets = iwn_ta.synsets(word)
                    if len(synsets) > 0:
                        longest_lemmatized_word = ""
                        for synset in synsets:
                            synset_word = synset.head_word()
                            if synset_word.lower() in lang_word_to_pos:
                                if len(synset_word) > len(longest_lemmatized_word):
                                    longest_lemmatized_word = synset_word.lower()  
                        if longest_lemmatized_word != "":
                            word_to_reduced_version[word] = longest_lemmatized_word
                except:
                    continue

        if lang == "tr":
            # For Zeyrek package
            logger = logging.getLogger()
            logger.setLevel(logging.CRITICAL)
            analyzer = zeyrek.MorphAnalyzer()

            for word in tqdm(unique_words):
                lemmatized = analyzer.lemmatize(word)
                if len(lemmatized) > 0:
                    lemmatized_words = lemmatized[0][1]

                    longest_lemmatized_word = ""
                    for word_l in lemmatized_words:
                        if word_l.lower() in lang_word_to_pos:
                            if len(word_l) > len(longest_lemmatized_word):
                                longest_lemmatized_word = word_l.lower()  
                    if longest_lemmatized_word != "":
                        word_to_reduced_version[word] = longest_lemmatized_word
        
        print("Added {n} mappings from {l} word to another word in the {l} -> en dict.".format(n = len(word_to_reduced_version), l = lang))

        with open(args.output_dir + '/{l}_word_to_reduced_version.pickle'.format(l = lang), 'wb') as handle:
            pkl.dump(word_to_reduced_version, handle, protocol=pkl.HIGHEST_PROTOCOL)