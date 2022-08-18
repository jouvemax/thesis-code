import pickle as pkl
import json
import multicombo
import nltk
from conllu import parse
from tqdm import tqdm
import argparse
import jieba.posseg as pseg
from collections import defaultdict

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_text', type=str)
    parser.add_argument('--output_dir', type=str)
    parser.add_argument('--lang', type=str)
    args = parser.parse_args()

    lang = args.lang

    with open(args.path_to_text, 'r', encoding="utf-8") as json_file:
        json_list = list(json_file)
    
    lang_data = [json.loads(jline) for jline in json_list]

    sentences = set()
    for entry in lang_data:
        sentence = entry["caption"]
        if "\n" in sentence:
            sentence = sentence.replace("\n", " ")
        sentences.add(sentence)

    print("There are {n} uniques captions/sentences.".format(n = len(sentences)))

    lang_sentence_to_pos = {}

    if lang == "zh":
        mapping_ZCTC_to_UPOS = defaultdict(lambda: "IGNORE", {"a": "AJD", "ad": "ADJ", "ag":"ADJ", "an": "ADJ", "al": "ADJ", "b": "NOUN", "bg": "NOUN",
        "bl": "NOUN", "c": "CCONJ", "cc": "CCONJ", "d": "ADV", "dg": "ADV", "dl":"ADV", "e":"INTJ", "ew":"PUNCT",
        "m":"NOUN", "mg":"NOUN", "mq":"NOUN", "n":"NOUN", "ng":"NOUN", "nl":"NOUN", "nl":"NOUN", "nr":"NOUN", "nr1":"NOUN", "nr2":"NOUN",
        "nrf":"NOUN", "nrj":"NOUN", "ns":"NOUN", "nsf":"NOUN", "nt":"NOUN", "nz":"NOUN", "p":"ADP", "pba":"ADP", "pbei":"ADP", "r":"PRON", 
        "q":"NOUN", "qt":"NOUN", "qv":"NOUN", "rg":"PRON", "rr":"PRON", "ry":"PRON", "rys":"PRON", "ryt":"PRON", "ryv":"PRON", "rz":"PRON",
        "rzs":"PRON", "rzt":"PRON", "rzv":"NOUN", "u":"AUX", "s":"NOUN", "t":"NOUN", "tg":"NOUN", "v":"VERB", "vd":"VERB", "vf":"VERB",
        "vg":"VERB", "vi":"VERB", "vl":"VERB", "vn":"VERB", "vx":"VERB"})

        for sentence in tqdm(sentences):
            words = pseg.cut(sentence)
            token_pos = []
            for w in words:
                token_pos.append((w.word, mapping_ZCTC_to_UPOS[w.flag]))

            lang_sentence_to_pos[sentence] = token_pos

    else:
        nlp_lang = multicombo.load(lang)
    
        for sentence in tqdm(sentences):
        
            try:
                doc = nlp_lang(sentence)
                data = multicombo.to_conllu(doc)
                parsed_sentences = parse(data)
                token_pos = []
                for parsed_sentence in parsed_sentences:
                    for token in parsed_sentence:
                        token_pos.append((token["form"], token["upos"]))
    
                lang_sentence_to_pos[sentence] = token_pos
    
            except:
                print("Error with caption:")
                print(sentence)
                continue


    with open(args.output_dir + '/{l}_caption_to_pos_marvl_test_set.pickle'.format(l = lang), 'wb') as handle:
        pkl.dump(lang_sentence_to_pos, handle, protocol=pkl.HIGHEST_PROTOCOL)