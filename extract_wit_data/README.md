# Extract WIT data

### Use the `marvl_env` environment for the following steps.

**1. Download WIT training entries from the official WIT [repository](https://github.com/google-research-datasets/wit/blob/main/DATA.md).**

**2. Extract entries for the languages of interest (Indonesian, Swahili, Tamil, Turkish and Mandarin Chinese)**

Use the `extract_marvl-lang_entries.sh` script.

It will create one pickle file per language and assign a unique id to all entries.

**3. Download images**

Use the `download_images.sh` for each language.

This script will download all the images for a given langague (given as input). Each image filename will be its unique id.
It will also create a `.json` containing all captions. It maps all image id to its caption.

It is possible to download only a portion of the images using the `SAMPLE_FACTOR` parameter.

For every 10,000 images downloaded, a dictionary will be saved. It can be use to retrieve the download status of each entry, and to restart the download from the latest checkpoint if something wrong happen.

**4. Extract features**

Once all images for a language are downloaded, use the `wit_pretraining_proposal.sh` script in [../marvl-code/feature_extraction/](marvl-code/feature_extraction) to extract the features.

For this step, please use the environment provided in [../marvl-code/feature_extraction/](marvl-code/feature_extraction)

**5. Get the valid ids**

As we will later construct datasets with exactly 18,500 entries, we save as pickle files all the ids whose entries were correctly extracted. It can be done using the `get_valid_ids.sh` script.
