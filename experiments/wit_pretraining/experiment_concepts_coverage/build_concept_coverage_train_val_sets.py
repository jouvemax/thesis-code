import pickle
import random
import argparse
import pandas as pd
import json
import re
from collections import defaultdict

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--list_indices_path', type=str)
    parser.add_argument('--marvl_entries_path', type=str)
    parser.add_argument('--lang_entries_path', type=str)
    parser.add_argument('--lang', type=str)
    parser.add_argument('--output_dir', type=str)
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--coverage', type=str)
    args = parser.parse_args()

    nb_training_entries = 18500
    nb_validation_entries = 1000
    
    with open(args.list_indices_path, 'rb') as handle:
        list_indices = pickle.load(handle)

    extracted_indices = set(list_indices)

    with open(args.lang_entries_path, 'rb') as handle:
        lang_entries = pickle.load(handle)

    filtered_df = lang_entries.drop([
                                 "hierarchical_section_title", 
                                 "caption_attribution_description",
                                 "caption_alt_text_description",
                                 "is_main_image",
                                 "attribution_passes_lang_id",
                                 "page_changed_recently",
                                 "context_page_description",
                                 "context_section_description"], 
                                 axis = 1)
    
    lang_entries_dict = filtered_df.to_dict("index")
    lang_entries_list = list(lang_entries_dict.items())

    lang_data = [pair for pair in lang_entries_list if str(pair[0]) in extracted_indices]
    
    with open(args.marvl_entries_path, 'r', encoding="utf-8") as json_file:
        marvl_list = list(json_file)

    marvl_concepts = set()

    for json_str in marvl_list:
        entry = json.loads(json_str)
        concept = entry["concept"]
        concept_clean = concept.split("-")[-1].replace("_", " ").lower()
        marvl_concepts.add(concept_clean)


    print("Loaded {n} MaRVL concepts from {f}.".format(n = len(marvl_concepts), f = args.marvl_entries_path)) 

    coverage = args.coverage
    seed = args.seed
    lang = args.lang
    random.seed(seed)

    def findWholeWord(w, caption):
        if lang == "ta" or lang == "zh":
            return w in caption
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search(caption)

    def check_list_coverage(list, concept):
        for entry in list:
            if findWholeWord(concept, entry):
                return True
        return False

    def check_overall_coverage(lang_data, marvl_concepts):
        concepts_title = set(pair[1]["page_title"].lower() for pair in lang_data)
        concepts_section_title = set(pair[1]["section_title"].lower() for pair in lang_data if not pd.isna(pair[1]["section_title"]))
        captions = set(pair[1]["caption_reference_description"].lower() for pair in lang_data if not pd.isna(pair[1]["caption_reference_description"]))

        concept_present = set()
        concept_not_present = set()
        for marvl_concept in marvl_concepts:
            if (check_list_coverage(concepts_title, marvl_concept)):
                concept_present.add(marvl_concept)
            elif (check_list_coverage(concepts_section_title, marvl_concept)):
                concept_present.add(marvl_concept)
            elif check_list_coverage(captions, marvl_concept):
                concept_present.add(marvl_concept)
            else:
                concept_not_present.add(marvl_concept)

        return concept_present, concept_not_present

    def check_title_coverage(lang_data, marvl_concepts):
        concepts_title = set(pair[1]["page_title"].lower() for pair in lang_data)

        concept_present = set()
        concept_not_present = set()
        for marvl_concept in marvl_concepts:
            if check_list_coverage(concepts_title, marvl_concept):
                concept_present.add(marvl_concept)
            else:
                concept_not_present.add(marvl_concept)

        return concept_present, concept_not_present

    concept_present_all, concept_not_present_all = check_overall_coverage(lang_data, marvl_concepts)
    print("There are {n} concepts covered in the WIT dataset.".format(n = len(concept_present_all)))
    print("There are {n} concepts missing in the WIT dataset.".format(n = len(concept_not_present_all)))

    concept_present_title, concept_not_present_title = check_title_coverage(lang_data, marvl_concepts)
    print("There are {n} concepts covered in the WIT dataset pages title.".format(n = len(concept_present_title)))
    print("There are {n} concepts missing in the WIT dataset pages title.".format(n = len(concept_not_present_title)))

    concept_to_entry_id = defaultdict(lambda: set())
    concept_to_title_id = defaultdict(lambda: set())

    for entry in lang_data:
        for concept in marvl_concepts:

            entry_id = entry[0]
            entry_data = entry[1]

            title = entry_data["page_title"]
            section_title = entry_data["section_title"]
            caption = entry_data["caption_reference_description"]

            if findWholeWord(concept, title.lower()):
                concept_to_entry_id[concept].add(entry_id)
                concept_to_title_id[concept].add(entry_id)
                continue
            if not pd.isna(section_title):
                if findWholeWord(concept, section_title.lower()):
                    concept_to_entry_id[concept].add(entry_id)
                    continue
            if not pd.isna(caption):
                if findWholeWord(concept, caption.lower()):
                    concept_to_entry_id[concept].add(entry_id)

    entries_marvl_concepts = set()
    for ids in concept_to_entry_id.values():
        entries_marvl_concepts.update(ids)

    print("There are {n} entries containing a MaRVL concept in either their title, their section title, or their caption.".format(n = len(entries_marvl_concepts)))

    entries_title_marvl_concepts = set()
    for ids in concept_to_title_id.values():
        entries_title_marvl_concepts.update(ids)

    print("There are {n} entries containing a MaRVL concept in their title.".format(n = len(entries_title_marvl_concepts)))

    if coverage == "full":

        title_matching_indices = []
        for ind in entries_title_marvl_concepts:
            title_matching_indices.append(ind)

        other_entries_ind = [pair[0] for pair in lang_data if pair[0] not in set(title_matching_indices)]

        random.seed(seed)
        random_selected_entries = random.sample(other_entries_ind, nb_training_entries - len(title_matching_indices))
        training_indices = title_matching_indices + random_selected_entries
        training_indices.sort()

        non_training_indices = [pair[0] for pair in lang_data if pair[0] not in set(training_indices)]

        random.seed(seed)
        validation_indices = random.sample(non_training_indices, nb_validation_entries)
        validation_indices.sort() 

        # Sanity check
        selected_entries = [pair for pair in lang_data if pair[0] in set(training_indices)]

        concept_present_all, concept_not_present_all = check_overall_coverage(selected_entries, marvl_concepts)
        print("There are {n} concepts covered in the training set.".format(n = len(concept_present_all)))
        print("There are {n} concepts missing in the training set.".format(n = len(concept_not_present_all)))

    if coverage == "zero":
        pruned_lang_data = [pair for pair in lang_data if pair[0] not in entries_marvl_concepts]

        random.seed(seed)
        training_data = random.sample(pruned_lang_data, nb_training_entries)

        training_indices = [pair[0] for pair in training_data]
        training_indices.sort()

        concept_present_all, concept_not_present_all = check_overall_coverage(training_data, marvl_concepts)
        print("There are {n} concepts covered in the training set.".format(n = len(concept_present_all)))
        print("There are {n} concepts missing in the training set.".format(n = len(concept_not_present_all)))

        non_training_indices = [pair[0] for pair in lang_data if pair[0] not in set(training_indices)]

        validation_indices = random.sample(non_training_indices, nb_validation_entries)
        validation_indices.sort()

    training_indices_str = set(str(ind) for ind in training_indices)
    validation_indices_str = set(str(ind) for ind in validation_indices)

    output_dir = args.output_dir

    print("Saving {p}/training_indices_seed{s}.pickle ({n} indices).".format(p = output_dir, s = seed, n = len(training_indices_str)))
    with open(output_dir + '/training_indices_seed{s}.pickle'.format(s = seed), 'wb') as handle_1:
        pickle.dump(training_indices_str, handle_1, protocol=pickle.HIGHEST_PROTOCOL)

    print("Saving {p}/validation_indices_seed{s}.pickle ({n} indices).".format(p = output_dir, s = seed, n = len(validation_indices_str)))    
    with open(output_dir + '/validation_indices_seed{s}.pickle'.format(s = seed), 'wb') as handle_2:
        pickle.dump(validation_indices_str, handle_2, protocol=pickle.HIGHEST_PROTOCOL)
