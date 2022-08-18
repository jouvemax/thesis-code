# Concepts coverage

1. Generate the ids for our training datasets

Provide as input the list of entries whose features were correctly extracted.

Use the `build_concept_coverage_train_val_sets.sh` script. You can provide the coverage settup by changing the `COVERAGE` parameter ("full" or "zero").

2. Once you have obtained the pretraining dataset ids, extract their corresponding captions using the `get_captions_from_ids.sh` script from [experiment_pretraining](../experiment_pretraining).

3. Pretraining

Scripts for pretraining are in [marvl-code/experiments/ctrl_muniter/pretrain/experiment_2](../../../marvl-code/experiments/ctrl_muniter/pretrain/experiment_2).

**Use the `marvl_env` environment.**

4. Finetuning

Scripts for finetuning are in [iglue/experiments/zero_shot/ctrl_muniter/marvl/experiment_2](../../../iglue/experiments/zero_shot/ctrl_muniter/marvl/experiment_2).

**Use the `iglue_env` environment.**

5. Results can be observed in the `results.ipynb` notebook.
