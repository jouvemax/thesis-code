# either input captions file or nlvr2 annotations
PATH_TO_TEXT=/mnt/nas_home/mrgj4/marvl-code/data/en/annotations/train.jsonl
OUTPUT_DIR=/mnt/nas_home/mrgj4/wit_dataset/infusion_exp

# en for NLVR2 sentences
LANG=en


python extract_lang_pos.py \
  --path_to_text $PATH_TO_TEXT \
  --output_dir $OUTPUT_DIR \
  --lang $LANG