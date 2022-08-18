import pickle
import random
import argparse
import fasttext
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--list_indices_path', type=str)
    parser.add_argument('--output_dir', type=str)
    parser.add_argument('--path_to_fasttext_model', type=str)
    parser.add_argument('--path_to_lang_entries', type=str)
    parser.add_argument('--lang', type=str)
    args = parser.parse_args()

    nb_validation_entries = 1000
    lang = args.lang

    top_k_lang = {"sw": 1500, "ta": 634, "tr": 678,"id": 460, "zh": 799}

    with open(args.list_indices_path, 'rb') as handle:
            list_indices = pickle.load(handle)

    extracted_indices = set(list_indices)

    with open(args.path_to_lang_entries, 'rb') as handle:
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

    print("Loading model at " + args.path_to_fasttext_model)
    model_lang = fasttext.load_model(args.path_to_fasttext_model)

    with open('../marvl-code/data/{l}/annotations/marvl-{l}.jsonl'.format(l = lang), 'r', encoding="utf-8") as json_file:
        marvl_list = list(json_file)

    marvl_concepts = set()

    for json_str in marvl_list:
        entry = json.loads(json_str)
        concept = entry["concept"]
        concept_clean = concept.split("-")[-1].replace("_", " ").lower()
        marvl_concepts.add(concept_clean)

    print("Loaded {n} MaRVL concepts for {l}.".format(n = len(marvl_concepts), l = lang))

    print("Computing Wikipedia Page Title embeddings using fastText.")
    embeddings_list = np.array([model_lang[entry[1]["page_title"].lower()] for entry in lang_data])

    embeddings_selected_indices = set()
    for concept in marvl_concepts:
        top_k = np.argpartition(cosine_similarity(embeddings_list, model_lang[concept].reshape(1, -1)).flatten(), -top_k_lang[lang])[-top_k_lang[lang]:]

        for ind in top_k:
            embeddings_selected_indices.add(ind)

    print("Selected the closest {k} entries (according to page title) for every concept. {n} entries selected in total.".format(k = top_k_lang[lang], n = len(embeddings_selected_indices)))        

    sorted_indices = list(embeddings_selected_indices)
    sorted_indices.sort()

    selected_entries = np.asarray(lang_data)[sorted_indices]

    selected_indices = [pair[0] for pair in selected_entries]

    # select non training indices
    non_training_indices = [indice for indice in list_indices if indice not in selected_indices]

    # select validation indices
    validation_indices = random.sample(non_training_indices, nb_validation_entries)

    training_indices_str = set(str(ind) for ind in selected_indices)
    validation_indices_str = set(str(ind) for ind in validation_indices)

    output_dir = args.output_dir

    print("\n")
    print("Saving {p}/training_indices_selected_{l}.pickle ({n} indices)".format(p = output_dir, l = lang, n = len(training_indices_str)))
    with open(output_dir + '/training_indices_selected_{l}.pickle'.format(l = lang), 'wb') as handle_1:
        pickle.dump(training_indices_str, handle_1, protocol=pickle.HIGHEST_PROTOCOL)

    print("Saving {p}/validation_indices_selected_{l}.pickle ({n} indices)".format(p = output_dir, l = lang, n = len(validation_indices_str)))    
    with open(output_dir + '/validation_indices_selected_{l}.pickle'.format(l = lang), 'wb') as handle_2:
        pickle.dump(validation_indices_str, handle_2, protocol=pickle.HIGHEST_PROTOCOL)
