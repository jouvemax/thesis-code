import pickle
import argparse
import os
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_ids_folder', type=str)
    parser.add_argument('--path_to_captions', type=str)
    args = parser.parse_args()

    with open(args.path_to_captions, 'r', encoding="utf-8") as json_file:
        captions = json.load(json_file)

    def save_captions(indices, split):

        captions_split = {}
        for indice in indices:
            if indice in captions:
                caption = captions[indice]
                captions_split[indice] = caption

        print("Saving {n} captions at ".format(n = len(captions_split)) + args.path_to_ids_folder + "/caption_{s}.json.".format(s = split))
        
        with open(args.path_to_ids_folder + "/caption_{s}.json".format(s = split), "w", encoding="utf-8") as outfile:
            json.dump(captions_split, outfile, ensure_ascii=False)

    for file in os.listdir(args.path_to_ids_folder):
        if file.startswith("training_indices"):
            with open(args.path_to_ids_folder + "/" + file, 'rb') as handle_1:
                training_indices = pickle.load(handle_1)

            save_captions(training_indices, "train")

        if file.startswith("validation_indices"):
            with open(args.path_to_ids_folder + "/" + file, 'rb') as handle_2:
                validation_indices = pickle.load(handle_2)
            
            save_captions(validation_indices, "valid")