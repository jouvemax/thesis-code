# thesis-code

This repository contains the code for my [thesis](Master_Thesis.pdf).

### Setup

1. Clone this repository with:
`git@github.com:jouvemax/thesis-code.git`

2. Create the three conda environments with:

`conda env create -f marvl_env.yml`

`conda env create -f iglue_env.yml`

`conda env create -f multicombo_env.yml`

3. Download the pretrained mUNITER and xUNITER baseline models [here](https://sid.erda.dk/sharelink/HfTaLDBWJi).

### WIT dataset

All information for downloading and extracting features from WIT are in [extract_wit_data/](extract_wit_data).

### Experiments

The scripts to reproduce all experiments can be found in [experiments/](experiments).

### Pretraining

Scripts for pretraining mUNITER and xUNITER can be found in [marvl-code/experiments/](marvl-code/experiments).

### Finetuning

For finetuning I relied on the IGLUE repository, as the NLVR2 features were smaller (~50GB) than the ones compatible with the MaRVL repository (~1TB).

NLVR2 images features (36 regions per image) can be downloaded [here](https://sid.erda.dk/cgi-sid/ls.py?share_id=FjJUsFbRWO).

Scripts for finetuning mUNITER and xUNITER can be found in [iglue/experiments/zero_shot/](iglue/experiments/zero_shot).

### Testing

Scripts for testing mUNITER and xUNITER can be found in [marvl-code/experiments/](marvl-code/experiments).

MaRVL features can be downloaded [here](https://sid.erda.dk/cgi-sid/ls.py?share_id=hmoEs4a3oG).
