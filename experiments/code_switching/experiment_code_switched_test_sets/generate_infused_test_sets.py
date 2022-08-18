import pickle as pkl
import json
from tqdm import tqdm
import argparse
from collections import defaultdict
import jieba
import pickle
import random

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('--output_dir', type=str)
  parser.add_argument('--lang', type=str)
  parser.add_argument('--path_to_marvl_annotations', type=str)
  parser.add_argument('--path_to_marvl_dict', type=str)

  args = parser.parse_args()

  lang = args.lang

  with open(args.path_to_marvl_dict, 'rb') as handle:
    marvl_dict = pickle.load(handle)

  with open(args.path_to_marvl_annotations, 'r', encoding="utf-8") as json_file:
    json_list = list(json_file)

  marvl_lang = [json.loads(jline) for jline in json_list]

  def get_infused_dataset(probability = 1, only_concept = False):
    marvl_en_infused = []

    words_modified = 0
    total_words = 0

    for entry in marvl_lang:
        
        if only_concept:
          # get concept 
          concept_original = entry["concept"]
          concept_clean = concept_original.split("-")[-1].replace("_", " ").lower()
          if " " in concept_clean:
            concepts = concept_clean.split(" ")
          else:
            concepts = [concept_clean]


        caption = entry["caption"]
        copied_caption = str(caption)

        if lang == "zh":
          caption_split = jieba.lcut(caption, cut_all=False)
          for word in caption_split:
            if word != "," and word != "." and word != "。":
              total_words += 1
        else:
          caption_split = caption.split(" ")
          total_words += len(caption_split)


        if only_concept:
          for concept in concepts:
            for i, word in enumerate(caption_split):
              if word.endswith(".") or word.endswith(","):
                word = word[:-1]
              word = word.lower()
              if concept in word:
                if word in marvl_dict:
                  caption_split[i] = marvl_dict[word]
                  words_modified += 1
        else:
          for i, word in enumerate(caption_split):
              if word == "," or word == "." or word == "。":
                continue
              if word.endswith(",") or word.endswith("."):
                  word = word[:-1]
              word = word.lower()
              if random.random() < probability:
                  caption_split[i] = marvl_dict[word]
                  words_modified += 1

        copied_entry = entry.copy()
        copied_caption = ' '.join(caption_split)
        copied_entry["caption"] = copied_caption

        marvl_en_infused.append(copied_entry)
    
    print("Probability to translate word = {p}".format(p = probability))
    print("# words modified: {m}".format(m = words_modified))
    print("Proportion: {p}%\n".format(p = words_modified / total_words * 100))

    return marvl_en_infused

  marvl_en_infused_concept = get_infused_dataset(only_concept = True)
  with open(args.output_dir + '/marvl-{l}-en-infused_concept.jsonl'.format(l = lang), 'w', encoding='utf-8') as f:
    for entry in marvl_en_infused_concept:
        json.dump(entry, f, ensure_ascii=False)
        f.write('\n')

  for prob in [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]:
    marvl_en_infused_prob = get_infused_dataset(prob)
    with open(args.output_dir + '/marvl-{l}-en-infused_{p}.jsonl'.format(l = lang, p = str(prob).replace(".", "")), 'w', encoding='utf-8') as f:
      for entry in marvl_en_infused_prob:
          json.dump(entry, f, ensure_ascii=False)
          f.write('\n')