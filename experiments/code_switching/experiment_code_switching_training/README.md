# Code-switching training

1. We will use the same features and captions as the ones used in [experiment_pretraining](../../experiments/wit_pretraining/experiment_pretraining)

However, this time, we will apply the code-switching framework during pretraining and/or finetuning.

3. Pretraining

Scripts for pretraining are in [marvl-code/experiments/ctrl_muniter/pretrain/experiment_3](../../../marvl-code/experiments/ctrl_muniter/pretrain/experiment_3) for mUNITER, and in [marvl-code/experiments/ctrl_xuniter/pretrain/experiment_3](../../../marvl-code/experiments/ctrl_xuniter/pretrain/experiment_3) for xUNITER.

**Use the `marvl_env`environment.**

4. Finetuning

Scripts for finetuning are in [iglue/experiments/zero_shot/ctrl_muniter/marvl/experiment_3](../../../iglue/experiments/zero_shot/ctrl_muniter/marvl/experiment_3) for mUNITER, and in [iglue/experiments/zero_shot/ctrl_xuniter/marvl/experiment_3](../../../iglue/experiments/zero_shot/ctrl_xuniter/marvl/experiment_3) for xUNITER.

**Use the `iglue_env`environment.**

5. Results can be observed in the `results.ipynb` notebook.
