# path to folder containing WIT extracted entries, should contain sw_entries.pkl, ta_entries.pkl...
WIT_ENTRIES_PATH="/mnt/nas_home/mrgj4/wit_dataset/utils"
# images will be downloaded at output_path/
OUTPUT_PATH="/mnt/nas_home/mrgj4/wit_dataset/images/zh"
LANG="zh"
# sample factor to reduce the amount of downloaded images, default = 1
SAMPLE_FACTOR=0.33
# number of processes used to download the images
NB_PROCESSES=8
# if you already started the download and want to continue later
#DOWNLOAD_DICT_PATH=
# captions will be saved at caption_path/
CAPTION_PATH="/mnt/nas_home/mrgj4/wit_dataset/captions"

python download_images.py --wit_entries_path $WIT_ENTRIES_PATH --output_path $OUTPUT_PATH \
                          --lang $LANG --sample_factor $SAMPLE_FACTOR \
                          --nb_processes $NB_PROCESSES \
                          --caption_path $CAPTION_PATH
                          #--download_dict_path $DOWNLOAD_DICT_PATH 