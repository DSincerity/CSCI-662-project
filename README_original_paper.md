### This is the README.md of KEMI paper.

# KEMI

The model and analysis implementation of _Knowledge-enhanced Mixed-initiative Dialogue System for Emotional Support Conversations_ (ACL 2023), which can be downloaded via this [url](https://drive.google.com/drive/folders/1gFlgKxda5O-RSbb3lhaj6oXiopgAsJKg?usp=sharing).

The code is built upon this [repo](https://github.com/thu-coai/Emotional-Support-Conversation/tree/main/codes_zcj).

## Run the code
Under the 'blenderbot' directory,
1. Run 'bash RUN/prepare_strat.sh' to prepare the data.
2. Run 'bash RUN/train_strat.sh' to train the model.
3. Run 'bash RUN/infer_strat.sh' to evaluate the model.

## Analysis of Mixed Initiative
Under the 'eafr' directory, you can find the fingerprint data of the analysis results on ESConv and EmpatheticDialogues.


## Citation
If the code or data is used in your research, please star this repo and cite our paper as follows:
```
@article{DBLP:journals/corr/abs-2305-10172,
  author       = {Yang Deng and
                  Wenxuan Zhang and
                  Yifei Yuan and
                  Wai Lam},
  title        = {Knowledge-enhanced Mixed-initiative Dialogue System for Emotional
                  Support Conversations},
  journal      = {CoRR},
  volume       = {abs/2305.10172},
  year         = {2023},
  url          = {https://doi.org/10.48550/arXiv.2305.10172},
}
```


===================================================================================
### KEMI is based on this code base. Here is README.md of the base code repo.

# Running Scripts for *ESC*

Siyang Liu*, **Chujie Zheng***, Orianna Demasi, Sahand Sabour, Yu Li, Zhou Yu, Yong Jiang and Minlie Huang. **Towards Emotional Support Dialog Systems**. *In ACL 2021*. [[paper]](https://arxiv.org/abs/2106.01144) [[repo]](https://github.com/thu-coai/Emotional-Support-Conversation)

```bib
@inproceedings{liu-etal-2021-towards,
  title={Towards Emotional Support Dialog Systems},
  author={Liu, Siyang  and
    Zheng, Chujie  and
    Demasi, Orianna  and
    Sabour, Sahand  and
    Li, Yu  and
    Yu, Zhou  and
    Jiang, Yong  and
    Huang, Minlie},
  booktitle={Proceedings of the 59th annual meeting of the Association for Computational Linguistics},
  year={2021}
}
```

## Preparing Enviroment

```bash
conda env create -f env.yml -n cuda
conda activate cuda
```

## Downloading Model

You should first download the [BlenderBot-small](https://huggingface.co/facebook/blenderbot_small-90M) model and replace the fake `pytorch_model.bin` file in `Blenderbot_small-90M` with the true one.

If you would like to evaluate generated results with Embedding-based similarity, you can download my prepared embedding files from [here](https://drive.google.com/drive/folders/11TwzwDtQoFHynlG0b1uT1MPQz9Jctb66?usp=sharing).

## About Postfix

- `_vanilla` denotes the variant directly fine-tuned on ESConv without using strategies
- `_strat` denotes the one that additionally uses the strategy information and supervision

## Preprocessing Training Data

First, enter `_reformat` and run `python process.py`.

Then, run `bash RUN/prepare_vanilla.sh` to preprocess the training data.

## Training Your Model

Run `bash RUN/train_vanilla.sh` to train your model.

## Inference with Your Model

Every time of model training will create a new folder in `DATA/{inputter_name}.{config_name}`, which is named after the time when the training starts. You should select a checkpoint (it may be based on the PPL of validation), and replace the checkpoint path in `RUN/infer_vanilla.sh --load_checkpoint` with the path of your selected checkpoint.

Then, run `bash RUN/infer_vanilla.sh` to do the inference.

**Note**: When you run `infer_strat.sh`, you can change `GOLDEN_TRUTH` in  `inputters/PARAMS.py` to control whether use the golden strategy during inference.

## Interacting with Your Model

Similar to inference, after designating the checkpoint in `RUN/interact_vanilla.sh --load_checkpoint`, run `bash RUN/interact_vanilla.sh`.
