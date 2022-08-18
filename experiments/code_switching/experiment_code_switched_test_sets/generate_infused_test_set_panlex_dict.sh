OUTPUT_DIR=./ta
LANG=ta
PATH_TO_MARVL_ANNOTATIONS=/mnt/nas_home/mrgj4/marvl-code/data/ta/annotations/marvl-ta.jsonl
PATH_TO_PANLEX_DICT=../panlex_dictionaries/ta_to_en_dict.pickle
PATH_TO_CAPTION_TO_POS_TAG=/mnt/nas_home/mrgj4/wit_dataset/infusion_exp/ta_caption_to_pos_marvl_test_set.pickle
PATH_TO_WORD_TO_REDUCED_VERSION=../panlex_dictionaries/ta_word_to_reduced_version.pickle


python generate_infused_test_set_panlex_dict.py \
  --output_dir $OUTPUT_DIR \
  --lang $LANG \
  --path_to_marvl_annotations $PATH_TO_MARVL_ANNOTATIONS \
  --path_to_panlex_dict $PATH_TO_PANLEX_DICT \
  --path_to_caption_to_pos_tag $PATH_TO_CAPTION_TO_POS_TAG \
  --path_to_word_to_reduced_version $PATH_TO_WORD_TO_REDUCED_VERSION