# Code-switched MaRVL test sets

### Setup

1. Build the bilingual dictionary for each MaRVL language using the `build_marvl_dictionary.sh` script. It translates each word in the test sets to English using Google translate.

2. Extract the part-of-speech tags of each MaRVL test set using the `extract_lang_pos_marvl.sh`.

Please use the `multicombo_env` for this step.

3. Generate the code-switched test sets using the `generate_infused_test_sets.sh` and the `generate_infused_test_set_panlex_dict.sh` scripts. 

The `generate_infused_test_set_panlex_dict.sh` code-switches the words using the Panlex dictionaries and the exact same pipeline as the one we will use for training later.


### Code-switched MaRVL test sets

Code-switched test sets are available for each language in its corresponding folder ("id", "sw", "ta", "tr", or "zh").

### Results

The results can be observed in the `results.ipynb` notebook.
