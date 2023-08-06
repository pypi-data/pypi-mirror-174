from typing import List

import pandas as pd

from presidio_evaluator.data_generator.faker_extensions.data_objects import FakerSpansResult

try:
    from flair.data import Corpus, Sentence
    from flair.datasets import ColumnCorpus
    from flair.embeddings import (
        TokenEmbeddings,
        WordEmbeddings,
        StackedEmbeddings,
        FlairEmbeddings,
        TransformerWordEmbeddings,
    )
    from flair.models import SequenceTagger
    from flair.trainers import ModelTrainer

except ImportError:
    print("Flair is not installed")

from presidio_evaluator import InputSample
from flair.optim import LinearSchedulerWithWarmup
import torch

from os import path


class FlairTrainer:
    """
    Helper class for training Flair models
    """

    @staticmethod
    def to_flair_row(text: str, pos: str, label: str) -> str:
        """
        Turn text, part of speech and label into one row.
        :return: str
        """
        #  note: removed part of speech tag (pos) from the row because nonsensical for protocol trace data?
        # return "{} {} {}".format(text, pos, label)
        return "{} {}".format(text, label)

    def to_flair(self, df: pd.DataFrame, outfile: str = "flair_train.txt") -> None:
        """Translate a pd.DataFrame to a flair dataset."""
        sentence = 0
        flair = []
        for row in df.itertuples():
            if row.sentence != sentence:
                sentence += 1
                flair.append("")
            else:
                flair.append(self.to_flair_row(row.text, row.pos, row.label))

        if outfile:
            with open(outfile, "w", encoding="utf-8") as f:
                for item in flair:
                    f.write("{}\n".format(item))

    def create_flair_corpus(
        self, train_samples_path, test_samples_path, val_samples_path, to_bio=False
    ):
        """
        Create a flair Corpus object and saive it to train, test, validation files.
        :param train_samples_path: Path to train samples
        :param test_samples_path: Path to test samples
        :param val_samples_path: Path to validation samples
        :return:
        """
        train_samples = train_samples_path
        # train_samples = InputSample.read_dataset_json(train_samples_path)
        # train_samples = FakerSpansResult.load_privy_dataset(train_samples_path)
        train_tagged = [sample for sample in train_samples if len(sample.spans) > 0]
        print(
            f"Kept {len(train_tagged)} train samples after removal of non-tagged samples"
        )
        train_data = InputSample.create_conll_dataset(
            train_tagged, to_bio=to_bio)
        self.to_flair(train_data, outfile="flair_train.txt")

        test_samples = test_samples_path
        # test_samples = InputSample.read_dataset_json(test_samples_path)
        # test_samples = FakerSpansResult.load_privy_dataset(test_samples_path)
        test_data = InputSample.create_conll_dataset(
            test_samples, to_bio=to_bio)
        self.to_flair(test_data, outfile="flair_test.txt")

        # val_samples = FakerSpansResult.load_privy_dataset(val_samples_path)
        # val_samples = InputSample.read_dataset_json(val_samples_path)
        val_samples = val_samples_path
        val_data = InputSample.create_conll_dataset(
            val_samples, to_bio=to_bio)
        self.to_flair(val_data, outfile="flair_val.txt")

    @staticmethod
    def read_corpus(data_folder: str):
        """
        Read Flair Corpus object.
        :param data_folder: Path with files
        :return: Corpus object
        """
        # columns = {0: "text", 1: "pos", 2: "ner"}
        columns = {0: "text", 1: "ner"}
        corpus = ColumnCorpus(
            data_folder,
            columns,
            train_file="flair_train.txt",
            test_file="flair_val.txt",
            dev_file="flair_test.txt",
            in_memory=False,
        )
        return corpus

    @staticmethod
    def train_with_flair_embeddings(corpus, add_unk=False, checkpoint="", fast=False):
        """
        Train a Flair model
        :param corpus: Corpus object
        :return:
        """
        print("Corpus: ", corpus)

        # 2. what tag do we want to predict?
        tag_type = "ner"

        # 3. make the tag dictionary from the corpus
        # tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
        if add_unk:
            tag_dictionary = corpus.make_label_dictionary(label_type=tag_type)
        else:
            tag_dictionary = corpus.make_label_dictionary(
                label_type=tag_type, add_unk=False)
        print("Tag dictionary: ", tag_dictionary)

        # 4. initialize embeddings
        if fast:
            embedding_types: List[TokenEmbeddings] = [
                WordEmbeddings("glove"),
                FlairEmbeddings("news-forward-fast"),
                FlairEmbeddings("news-backward-fast"),
            ]
        else:
            embedding_types: List[TokenEmbeddings] = [
                WordEmbeddings("glove"),
                FlairEmbeddings("news-forward"),
                FlairEmbeddings("news-backward"),
            ]

        embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

        # 5. initialize sequence tagger
        tagger = SequenceTagger(
            hidden_size=256,
            embeddings=embeddings,
            tag_dictionary=tag_dictionary,
            tag_type=tag_type,
            use_crf=True,
        )

        # 6. initialize trainer
        trainer = ModelTrainer(tagger, corpus)
        if checkpoint:
            if fast:
                path = "resources/taggers/privy-flert-ner-fast/checkpoint.pt"
            else:
                path = "resources/taggers/privy-flert-ner/checkpoint.pt"
            trained_model = SequenceTagger.load(path)
            trainer.resume(
                model=trained_model,
            )
        else:
            if fast:
                path = "resources/taggers/privy-flert-ner-fast"
            else:
                path = "resources/taggers/privy-flert-ner"
            trainer.train(
                path,
                learning_rate=0.1,
                mini_batch_size=32,
                max_epochs=150,
                checkpoint=True,
            )

        sentence = Sentence("I am from Jerusalem")
        # run NER over sentence
        tagger.predict(sentence)

        print(sentence)
        print("The following NER tags are found:")

        # iterate over entities and print
        for entity in sentence.get_spans("ner"):
            print(entity)

    @staticmethod
    def train_with_transformers(corpus, add_unk=False, mini_batch_size=1, embeddings="roberta-base", checkpoint="", max_epochs=20):
        # xlm-roberta-base is the multilingual version of roberta-base
        # roberta-large is the large version of roberta-base
        """
        Train a Flair model
        :param corpus: Corpus object
        :return:
        """
        print(corpus)

        # 2. what tag do we want to predict?
        tag_type = "ner"

        # 3. make the tag dictionary from the corpus
        if add_unk:
            tag_dictionary = corpus.make_label_dictionary(label_type=tag_type)
        else:
            tag_dictionary = corpus.make_label_dictionary(
                label_type=tag_type, add_unk=False)
        print(tag_dictionary)

        # 4. initialize fine-tuneable transformer embeddings WITH document context
        # previously xlm-roberta-large
        embedding_types: List[TokenEmbeddings] = [TransformerWordEmbeddings(model=embeddings,
                                                                            layers="-1",
                                                                            subtoken_pooling="first",
                                                                            fine_tune=True,
                                                                            use_context=True,
                                                                            )]

        embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

        # 5. initialize bare-bones sequence tagger (no CRF, no RNN, no reprojection)
        tagger = SequenceTagger(hidden_size=256,
                                embeddings=embeddings,
                                tag_dictionary=tag_dictionary,
                                tag_type='ner',
                                use_crf=False,
                                use_rnn=False,
                                reproject_embeddings=False,
                                )

        # 6. initialize trainer
        trainer: ModelTrainer = ModelTrainer(tagger, corpus)

        if checkpoint:
            trained_model = SequenceTagger.load(
                "resources/taggers/privy-flair-transformers/checkpoint.pt")
            trainer.resume(
                model=trained_model,
                # learning_rate=5.0e-6,
                # mini_batch_size=mini_batch_size,
                # max_epochs=20,
                # optimizer=torch.optim.AdamW,
                # scheduler=LinearSchedulerWithWarmup,
                # warmup_fraction=0.1,
                # use_final_model_for_eval=True,
                # decoder_lr_factor=1.0,
                # mini_batch_chunk_size=1,  # remove this parameter to speed up computation if you have a big GPU
                # checkpoint=True,
            )

        # from torch.optim.lr_scheduler import OneCycleLR

        # 7. run fine-tuning
        else:
            trainer.fine_tune('resources/taggers/privy-flair-transformers',
                              learning_rate=5.0e-6,
                              mini_batch_size=mini_batch_size,
                              max_epochs=max_epochs,
                              #   scheduler=OneCycleLR,
                              mini_batch_chunk_size=1,  # remove this parameter to speed up computation if you have a big GPU
                              #   weight_decay=0.,
                              checkpoint=True,
                              )

        sentence = Sentence("I am from Jerusalem")
        # run NER over sentence
        tagger.predict(sentence)

        print(sentence)
        print("The following NER tags are found:")

        # iterate over entities and print
        for entity in sentence.get_spans("ner"):
            print(entity)


if __name__ == "__main__":
    train_samples = "../../data/train_Dec-19-2021.json"
    test_samples = "../../data/test_Dec-19-2021.json"
    val_samples = "../../data/validation_Dec-19-2021.json"

    trainer = FlairTrainer()
    trainer.create_flair_corpus(train_samples, test_samples, val_samples)

    corpus = trainer.read_corpus("")
    trainer.train_with_flair_embeddings(corpus)
