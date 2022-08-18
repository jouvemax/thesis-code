# WIT Pretraining

1. Generate the ids for our training datasets

Provide as input the list of entries whose features were correctly extracted.

Use the `build_random_train_val_sets.sh` script for random data.

Use the `build_selected_train_val_sets.sh` script for smart selection of data using fastText. You need to provide as input the path the the fastText model. They can be downloaded [here](https://fasttext.cc/docs/en/crawl-vectors.html).

2. Once you have obtained the pretraining dataset ids, extract their corresponding captions using the `get_captions_from_ids.sh` script.

3. Pretraining

Scripts for pretraining are in [marvl-code/experiments/ctrl_muniter/pretrain/experiment_1](../../../marvl-code/experiments/ctrl_muniter/pretrain/experiment_1).

**Use the `marvl_env`environment.**

4. Finetuning

Scripts for finetuning are in [iglue/experiments/zero_shot/ctrl_muniter/marvl/experiment_1](../../../iglue/experiments/zero_shot/ctrl_muniter/marvl/experiment_1).

**Use the `iglue_env`environment.**

5. Results can be observed in the `results.ipynb` notebook.
