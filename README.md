# segtest
A Test Suite for Morphological Phenomena in Neural Machine Translation

# Motivation

Data-driven subword segmentation has become the default strategy for open-vocabulary machine translation and other NLP tasks, but may not be sufficiently generic for optimal learning of non-concatenative morphology. In this repository, we make our test suite covering different types of morphological phenomena available. It can be used to evaluate new segmentation strategies or sequence-to-sequence architectures in a controlled, semi-synthetic setting.

# Preparing the Data
You can find our synthetic training data as well as the test sets for the morphological phenomena in the `test_suite_data` folder. In order to train an NMT model on this data, we recommend adding a larger corpus of real translations to the training data and using a real-data dev set.

If you want to reproduce our experiments from the paper, you should add the training data from the WMT16 news translation task and use the test sets from WMT15 as the development data. You can download the data on the [official WMT website](http://www.statmt.org/wmt16/translation-task.html).

Decompress the synthetic data and concatenate the files with your own training data files:

    gunzip test_suite_data/train_synthetic.*

    cat test_suite_data/train_synthetic.src your_training_data.de > test_suite_data/train.src
    cat test_suite_data/train_synthetic.trg your_training_data.en > test_suite_data/train.trg

    mv your_dev_data.de test_suite_data/dev.src
    mv your_dev_data.en test_suite_data/dev.trg
    cp test_suite_data/dev.trg test_suite_data/dev.ref


# Training Your Models

We provide the training scripts for the models we trained in the paper. If you want to reproduce our results, you can use these scripts to train the respective models.

Our models were trained with [nematus](https://github.com/EdinburghNLP/nematus), the preprocessing for BPE models is done with [SentencePiece](https://github.com/google/sentencepiece) and we use [sacrebleu](https://github.com/mjpost/sacrebleu) to monitor translation quality throughout the training. Please follow the installation instructions in these repositories to install the necesary toolkits.  

Before training the models you need to export the relative paths to the nematus repository and to this repository:

    segtest_dir=path_to_this_repository
    nematus_home=path_to_nematus_repository

    export segtest_dir
    export nematus_home

You can then execute the `run.sh` script for the specific model you want to train, e.g. for the BPE model with 32k subword merges and BPE-dropout:

    bash models/bpe-d32k/run.sh

`bpe-32k` is the BPE model with 32k merges without BPE-dropout. `bpe-d32k` is the BPE model with 32k merges with BPE-dropout. `bpe-d500` is the BPE model with 500 merges and BPE-dropout which we used as a parent model to finetune the character-based model `char`. If you want to follow our setup to train `char`, you first have to train `bpe-d500` (for at least 400k updates).

`run.sh` includes the preprocessing and training of the model as well as translating the test sets. If you want to test your own segmentation strategies or another architecture / train with another framework on this data, you can easily replace the necessary scripts with your own, i.e. `preprocess.sh` or `train.sh` and `translate.sh` respectively.


# Evaluating Your Models

For evaluation, you can call the `evaluate.sh` script in the respective model folder, e.g.:

    bash models/bpe-d32k/evaluate.sh

This will evaluate all translated test sets.

If you did not train models yourself but simply want to reproduce the evaluation of the model outputs in our paper, you can also do this. We provide the test set translations of our models in the `paper_results` folder. The main results in the paper (Table 4) can be reproduced as follows:

    python scripts/evaluate.py -t paper_results/$model/$type.postprocessed -i test_suite_data/$type.meta -s test_suite_data/$type.scores -m $type -r surface

where `$model` is either `bpe-32k`, `bpe-d32k`, `bpe-d500` or `char` and `$type` is either `compound`, `circumfix`, `infix`, `vowelharmony` or `reduplication`. For example, if you want to evaluate how well the BPE model with 32k merges without BPE-dropout can translate reduplication, call the script like this:

    python scripts/evaluate.py -t paper_results/bpe-32k/reduplication.postprocessed -i test_suite_data/reduplication.meta -s test_suite_data/reduplication.scores -m reduplication -r surface

    #1: 0.942
    #2: 0.0
    #3: 0.72

The ids correspond to the ids used in the paper. See Table 5 in the Appendix for an overview of which id corresponds to which pattern.

To evaluate the abstract representation, change the value for `-r`:

    python scripts/evaluate.py -t paper_results/bpe-32k/reduplication.postprocessed -i test_suite_data/reduplication.meta -s test_suite_data/reduplication.scores -m reduplication -r abstract

To include the data augmentation examples (see Appendix C), use `--include_augmented_examples`:

    python scripts/evaluate.py -t paper_results/bpe-32k/reduplication.postprocessed -i test_suite_data/reduplication.meta -s test_suite_data/reduplication.scores -m reduplication -r surface --include_augmented_examples

To evaluate based on the frequency with which a source word base is seen with the specific morphological phenomena in the training data (used for Figure 2), use the `--evaluate_by_freq_buckets` option:

    python scripts/evaluate.py -t paper_results/bpe-32k/reduplication.postprocessed -i test_suite_data/reduplication.meta -s test_suite_data/reduplication.scores -m reduplication -r surface --evaluate_by_freq_buckets




# Citation

If you use this test suite, please cite the following paper:

    @inproceedings{amrhein2021,
    title = "How Suitable Are Subword Segmentation Strategies for Translating Non-Concatenative Morphology?",
    author = "Amrhein, Chantal  and
      Sennrich, Rico",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2021",
    month = nov,
    year = "2021",
    publisher = "Association for Computational Linguistics",
    }
