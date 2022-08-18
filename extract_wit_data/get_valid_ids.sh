# Path to extracted features
PATH_TO_FEATURES=/mnt/nas_home/mrgj4/wit_dataset/features/tr_features.h5
# Path 
OUTPUT_PATH=/mnt/nas_home/mrgj4/final_repo/experiment_1/tr
# file name
FILE_NAME=tr_valid_ids

python get_valid_ids.py --path_to_features $PATH_TO_FEATURES --output_path $OUTPUT_PATH --file_name $FILE_NAME