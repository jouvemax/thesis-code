import pickle as pkl
import json
from tqdm import tqdm
import argparse
from googletrans import Translator
from collections import defaultdict
import jieba

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str)
    parser.add_argument('--lang', type=str)
    parser.add_argument('--path_to_marvl_annotations', type=str)
    args = parser.parse_args()

    lang = args.lang

    with open(args.path_to_marvl_annotations, 'r', encoding="utf-8") as json_file:
        json_list = list(json_file)

    marvl_lang = [json.loads(jline) for jline in json_list]

    unique_words = set()
    total_words = 0

    for entry in marvl_lang:
        caption = entry["caption"]

        if lang == "zh":
            caption_words = jieba.lcut(caption, cut_all=False)
        else:
            caption_words = caption.split(" ")
        for word in caption_words:
            if word.endswith(".") or word.endswith(",") or word.endswith("。"):
                word = word[:-1]
            word = word.lower()
            unique_words.add(word)
        total_words += len(caption_words)
    
    print("There are {n} unique words in the {l} MaRVL test set.".format(n = len(unique_words), l = lang))
    print("There are {n} total words in the {l} MaRVL test set.".format(n = total_words, l = lang))

    lang_words_to_en = {}
    nb_errors = 0

    translator = Translator(service_urls=['translate.google.co.uk'])

    for word in tqdm(unique_words):
        try:
            if lang == "zh":
                translation = translator.translate(word, dest='en').text.lower()
            else:
                translation = translator.translate(word, src=lang, dest='en').text.lower()
            lang_words_to_en[word] = translation
        except:
            lang_words_to_en[word] = word
            nb_errors += 1
    
    print("There were {n} errors while translating.".format(n = nb_errors))

    with open(args.output_dir + '/{l}_to_en_marvl_dict.pickle'.format(l = lang), 'wb') as handle:
        pkl.dump(lang_words_to_en, handle, protocol=pkl.HIGHEST_PROTOCOL)