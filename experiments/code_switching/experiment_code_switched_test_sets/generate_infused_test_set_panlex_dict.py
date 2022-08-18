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
  parser.add_argument('--path_to_panlex_dict', type=str)
  parser.add_argument('--path_to_caption_to_pos_tag', type=str)
  parser.add_argument('--path_to_word_to_reduced_version', type=str, default=None)

  args = parser.parse_args()

  lang = args.lang

  with open(args.path_to_panlex_dict, 'rb') as handle:
    panlex_dict_with_pos_tags = pickle.load(handle)

  # panlex_dict = {}
  # for word_pos, translation in panlex_dict_with_pos_tags.items():
  #   panlex_dict[word_pos[0]] = translation

  with open(args.path_to_marvl_annotations, 'r', encoding="utf-8") as json_file:
    json_list = list(json_file)

  marvl_lang = [json.loads(jline) for jline in json_list]

  with open(args.path_to_caption_to_pos_tag, 'rb') as handle:
    caption_to_pos_tag = pickle.load(handle)

  if args.path_to_word_to_reduced_version:
    with open(args.path_to_word_to_reduced_version, 'rb') as handle:
      word_to_reduced_version = pickle.load(handle)

  def code_switch_caption(caption):
      """
      Given a caption, will perform code-switching and translate some of the words to English.
      """
      words_modified_caption = 0

      def perform_dictionary_switch(init_word, dict_pair, caption):
          modified = False

          if dict_pair in panlex_dict_with_pos_tags:
                  modified = True
                  new_word = panlex_dict_with_pos_tags[dict_pair]
                  if init_word[0].isupper():
                      new_word = new_word.capitalize()
                  if lang == "zh":
                      caption = caption.replace(init_word, " " + new_word + " ")
                  else:
                      caption = caption.replace(init_word, new_word)
          return caption, modified

      if "\n" in caption:
          caption = caption.replace("\n", " ")
      if caption in caption_to_pos_tag:
          pos_tokens = caption_to_pos_tag[caption]
          for init_word, pos in pos_tokens:
              if pos in set(["NOUN", "VERB", "ADJ", "ADV"]):
                  word = init_word.lower()
                  dict_pair = (word, pos)
                  caption, modified = perform_dictionary_switch(init_word, dict_pair, caption)
                  if modified:
                    words_modified_caption += 1
                  if args.path_to_word_to_reduced_version:
                      if word in word_to_reduced_version:
                          reduced_word = word_to_reduced_version[word]
                          dict_pair = (reduced_word, pos)
                          caption, modified = perform_dictionary_switch(init_word, dict_pair, caption)
                          if modified:
                            words_modified_caption += 1
      return caption, words_modified_caption 

  def get_infused_dataset(panlex_dict):
    marvl_en_infused = []

    words_modified = 0
    total_words = 0

    for entry in marvl_lang:

        caption = entry["caption"]

        if lang == "zh":
          caption_split = jieba.lcut(caption, cut_all=False)
          for word in caption_split:
            if word != "," and word != "." and word != "。":
              total_words += 1
        else:
          caption_split = caption.split(" ")
          total_words += len(caption_split)

        
        # for i, word in enumerate(caption_split):
        #     if word == "," or word == "." or word == "。":
        #       continue
        #     if word.endswith(",") or word.endswith("."):
        #         word = word[:-1]
        #     word = word.lower()
        #     if word in panlex_dict:
        #         caption_split[i] = panlex_dict[word]
        #         words_modified += 1

        copied_entry = entry.copy()
        new_caption, words_modified_caption = code_switch_caption(caption)

        words_modified += words_modified_caption

        copied_entry["caption"] = new_caption

        marvl_en_infused.append(copied_entry)
    
    print("# words modified: {m}".format(m = words_modified))
    print("Proportion: {p}%\n".format(p = words_modified / total_words * 100))

    return marvl_en_infused

  marvl_en_infused_panlex_dict = get_infused_dataset(panlex_dict_with_pos_tags)
  with open(args.output_dir + '/marvl-{l}-en-infused_panlex_dict.jsonl'.format(l = lang), 'w', encoding='utf-8') as f:
    for entry in marvl_en_infused_panlex_dict:
        json.dump(entry, f, ensure_ascii=False)
        f.write('\n')