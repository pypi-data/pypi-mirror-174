import json
from pathlib import Path
from typing import List, Optional, Union, Dict, Any, Tuple

import pandas as pd
import spacy
from spacy import Language
from spacy.tokens import Doc, DocBin
from spacy.training import iob_to_biluo
from spacy.symbols import ORTH
from tqdm import tqdm
from collections import Counter

from presidio_evaluator import span_to_tag, tokenize
from presidio_evaluator.data_generator.faker_extensions import (
    FakerSpansResult,
    FakerSpan,
)

PRIVY_ENTITIES = {
    "person": "PERSON",
    "name_male": "PERSON",
    "name_female": "PERSON",
    "first_name": "PERSON",
    "first_name_male": "PERSON",
    "first_name_female": "PERSON",
    "first_name_nonbinary": "PERSON",
    "last_name": "PERSON",
    "last_name_male": "PERSON",
    "last_name_female": "PERSON",

    "address": "LOCATION",
    "street_address": "LOCATION",
    "secondary_address": "LOCATION",
    "zipcode": "LOCATION",
    "building_number": "LOCATION",
    "street_name": "LOCATION",
    "airport_name": "LOCATION",
    "airport_iata": "LOCATION",  # *
    "airport_icao": "LOCATION",  # *

    "country": "LOCATION",
    "country_code": "LOCATION",
    "state": "LOCATION",
    "state_abbr": "LOCATION",
    "city": "LOCATION",

    "coordinate": "COORDINATE",  # **
    "longitude": "COORDINATE",  # **
    "latitude": "COORDINATE",  # **

    "nationality": "NRP",
    "nation_woman": "NRP",
    "nation_man": "NRP",
    "nation_plural": "NRP",
    "religion": "NRP",

    "date": "DATE_TIME",
    "date_time": "DATE_TIME",
    "date_of_birth": "DATE_TIME",
    "day_of_week": "DATE_TIME",
    "year": "DATE_TIME",
    "month": "DATE_TIME",

    "url": "URL",
    "domain_name": "URL",

    "credit_card_number": "CREDIT_CARD",
    "credit_card_expire": "DATE_TIME",

    "iban": "IBAN_CODE",
    "bban": "US_BANK_NUMBER",  # *
    "phone_number": "PHONE_NUMBER",
    "ssn": "US_SSN",
    "passport": "US_PASSPORT",  # *
    "driver_license": "US_DRIVER_LICENSE",
    "ip_address": "IP_ADDRESS",
    "itin": "US_ITIN",
    "email": "EMAIL_ADDRESS",

    "organization": "ORGANIZATION",
    "company": "ORGANIZATION",
    "airline": "ORGANIZATION",

    "job": "TITLE",
    "prefix": "TITLE",
    "prefix_male": "TITLE",
    "prefix_female": "TITLE",
    "gender": "TITLE",

    "imei": "IMEI",
    "password": "PASSWORD",
    "license_plate": "US_LICENSE_PLATE",
    "mac_address": "MAC_ADDRESS",
    "age": "AGE",

    "currency_code": "FINANCIAL",
    "aba": "FINANCIAL",
    "swift": "FINANCIAL",

    "string": "O",
    "boolean": "O",
    "color": "O",
    "random_number": "O",
    "sha1": "O",
}

PRIVY_PRESIDIO_MODEL = {
    "person": "PER",
    "name_male": "PER",
    "name_female": "PER",
    "first_name": "PER",
    "first_name_male": "PER",
    "first_name_female": "PER",
    "first_name_nonbinary": "PER",
    "last_name": "PER",
    "last_name_male": "PER",
    "last_name_female": "PER",

    "address": "LOC",
    "street_address": "LOC",
    "secondary_address": "LOC",
    "zipcode": "LOC",
    "building_number": "LOC",
    "street_name": "LOC",
    "airport_name": "LOC",
    "airport_iata": "LOC",  # *
    "airport_icao": "LOC",  # *

    "country": "LOC",
    "country_code": "LOC",
    "state": "LOC",
    "state_abbr": "LOC",
    "city": "LOC",

    "coordinate": "LOC",  # **
    "longitude": "LOC",  # **
    "latitude": "LOC",  # **

    "nationality": "NRP",
    "nation_woman": "NRP",
    "nation_man": "NRP",
    "nation_plural": "NRP",
    "religion": "NRP",

    "date": "DATE_TIME",
    "date_time": "DATE_TIME",
    "date_of_birth": "DATE_TIME",
    "day_of_week": "DATE_TIME",
    "year": "DATE_TIME",
    "month": "DATE_TIME",

    "url": "O",
    "domain_name": "O",

    "credit_card_number": "CREDIT_CARD",
    "credit_card_expire": "DATE_TIME",

    "iban": "O",
    "bban": "US_BANK_NUMBER",  # *
    "phone_number": "O",
    "ssn": "O",
    "passport": "US_PASSPORT",  # *
    "driver_license": "US_DRIVER_LICENSE",
    "ip_address": "O",
    "itin": "US_ITIN",
    "email": "O",

    "organization": "ORG",
    "company": "ORG",
    "airline": "ORG",

    "job": "TITLE",
    "prefix": "TITLE",
    "prefix_male": "TITLE",
    "prefix_female": "TITLE",
    "gender": "TITLE",

    "imei": "IMEI",
    "password": "PASSWORD",
    "license_plate": "US_LICENSE_PLATE",
    "mac_address": "MAC_ADDRESS",
    "age": "AGE",

    "currency_code": "FINANCIAL",
    "aba": "FINANCIAL",
    "swift": "FINANCIAL",

    "string": "O",
    "boolean": "O",
    "color": "O",
    "random_number": "O",
    "sha1": "O",
}

# # mapping to match CONLL and custom entities.
# PRIVY_PRESIDIO_MODEL = {
#     # entities presidio performs poorly on
#     "DATE_TIME": "DATE_TIME",
#     "US_DRIVER_LICENSE": "US_DRIVER_LICENSE",
#     "PERSON": "PER",
#     "US_PASSPORT": "US_PASSPORT",
#     "NRP": "NRP",
#     "LOCATION": "LOC",

#     # entities not supported by presidio
#     "COORDINATE": "LOC",
#     "TITLE": "TITLE",
#     "IMEI": "IMEI",
#     "PASSWORD": "PASSWORD",
#     "US_LICENSE_PLATE": "US_LICENSE_PLATE",
#     "MAC_ADDRESS": "MAC_ADDRESS",
#     "AGE": "AGE",
#     "FINANCIAL": "FINANCIAL",
# }

PRIVY_CONLL_TRANSLATOR = {
    "PERSON": "PERSON",
    "LOCATION": "LOC",
    "ORGANIZATION": "ORG",
    # "NRP": "MISC",
    # "GPE": "LOC",
}

PRIVY_ONTONOTES_TRANSLATOR = {
    "PERSON": "PERSON",
    "NRP": "NORP",
    # "STREET_ADDRESS": "FAC",
    # "LOCATION": "FAC",
    "GPE": "GPE",
    "DATE_TIME": "DATE",
    "ORGANIZATION": "ORG",
}

PRIVY_PRESIDIO_TRANSLATOR = {
    "PERSON": "PERSON",
    "NRP": "NRP",
    "STREET_ADDRESS": "LOCATION",
    "LOCATION": "LOCATION",
    "GPE": "LOCATION",
    "DATE_TIME": "DATE_TIME",
    "CREDIT_CARD": "CREDIT_CARD",
    "URL": "URL",
    "DOMAIN_NAME": "URL",
    "IBAN_CODE": "IBAN_CODE",
    # "US_BANK_NUMBER": "US_BANK_NUMBER", # not supported somehow
    "PHONE_NUMBER": "PHONE_NUMBER",
    "US_SSN": "US_SSN",
    "US_PASSPORT": "US_PASSPORT",
    "US_DRIVER_LICENSE": "US_DRIVER_LICENSE",
    "IP_ADDRESS": "IP_ADDRESS",
    "EMAIL_ADDRESS": "EMAIL_ADDRESS",
    "ORGANIZATION": "ORGANIZATION",
}

# old
SPACY_PRESIDIO_ENTITIES = {
    "ORG": "ORGANIZATION",
    "NORP": "NRP",
    "GPE": "LOCATION",
    "LOC": "LOCATION",
    "FAC": "LOCATION",
    "PERSON": "PERSON",
    "LOCATION": "LOCATION",
    "ORGANIZATION": "ORGANIZATION",
    "DATE": "DATE_TIME",
    "TIME": "DATE_TIME",
}

PRESIDIO_SPACY_ENTITIES = {
    "PERSON": "PERSON",
    "LOCATION": "LOC",
    "GPE": "GPE",
    "ORGANIZATION": "ORG",
    "DATE_TIME": "DATE",
    "NRP": "NORP",
}


class Span:
    """
    Holds information about the start, end, type and value
    of an entity in a text
    """

    def __init__(self, entity_type, entity_value, start_position, end_position):
        self.entity_type = entity_type
        self.entity_value = entity_value
        self.start_position = start_position
        self.end_position = end_position

    def intersect(self, other, ignore_entity_type: bool):
        """
        Checks if self intersects with a different Span
        :return: If intersecting, returns the number of
        intersecting characters.
        If not, returns 0
        """

        # if they do not overlap the intersection is 0
        if (
            self.end_position < other.start_position
            or other.end_position < self.start_position
        ):
            return 0

        # if we are accounting for entity type a diff type means intersection 0
        if not ignore_entity_type and (self.entity_type != other.entity_type):
            return 0

        # otherwise the intersection is min(end) - max(start)
        return min(self.end_position, other.end_position) - max(
            self.start_position, other.start_position
        )

    @classmethod
    def from_faker_span(cls, faker_span: FakerSpan) -> "Span":
        return cls(
            entity_type=faker_span.type,
            entity_value=faker_span.value,
            start_position=faker_span.start,
            end_position=faker_span.end,
        )

    def __repr__(self):
        return (
            f"Type: {self.entity_type}, "
            f"value: {self.entity_value}, "
            f"start: {self.start_position}, "
            f"end: {self.end_position}"
        )

    def __eq__(self, other):
        return (
            self.entity_type == other.entity_type
            and self.entity_value == other.entity_value
            and self.start_position == other.start_position
            and self.end_position == other.end_position
        )

    def __hash__(self):
        return hash(
            (
                "entity_type",
                self.entity_type,
                "entity_value",
                self.entity_value,
                "start_position",
                self.start_position,
                "end_position",
                self.end_position,
            )
        )

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class InputSample(object):
    def __init__(
        self,
        full_text: str,
        spans: Optional[List[Span]] = None,
        masked: Optional[str] = None,
        tokens: Optional[Doc] = None,
        tags: Optional[List[str]] = None,
        create_tags_from_span=False,
        token_model_version="en_core_web_sm",
        scheme="IO",
        metadata=None,
        template_id=None,
    ):
        """
        Hold all the information needed for evaluation in the
        presidio-evaluator framework.

        :param full_text: The raw text of this sample
        :param masked: Masked/Templated version of the raw text
        :param spans: List of spans for entities
        :param create_tags_from_span: True if tags (tokens+tags) should be added
        :param scheme: IO, BIO or BILUO. Only applicable if span_to_tag=True
        :param tokens: spaCy Doc object
        :param tags: list of strings representing the label for each token,
        given the scheme
        :param token_model_version: The name of the model to use for tokenization if no tokens provided
        :param metadata: A dictionary of additional metadata on the sample,
        in the English (or other language) vocabulary
        :param template_id: Original template (utterance) of sample, in case it was generated  # noqa
        """
        if tags is None:
            tags = []
        if tokens is None:
            tokens = []
        self.full_text = full_text
        self.masked = masked
        self.spans = spans if spans else []
        self.metadata = metadata

        # generated samples have a template from which they were generated
        if not template_id and self.metadata:
            self.template_id = self.metadata.get("template_id")
        else:
            self.template_id = template_id

        if create_tags_from_span:
            tokens, tags = self.get_tags(scheme, token_model_version)
            self.tokens = tokens
            self.tags = tags
        else:
            self.tokens = tokens
            self.tags = tags

    @classmethod
    def from_faker_spans_result(
        cls,
        faker_spans_result: FakerSpansResult,
        scheme: str = "BILUO",
        create_tags_from_span: bool = True,
        **kwargs,
    ) -> "InputSample":
        """
        Translate the FakerSpansResult object to InputSample for backward compatibility
        :param faker_spans_result: A FakerSpansResult object
        :param create_tags_from_span: True if text should be tokenized according to spans
        :param scheme: Annotation scheme for tokens (BILUO, BIO, IO). Only relevant if create_tags_from_span=True
        :param kwargs: Additional kwargs for InputSample creation
        :return: InputSample
        """
        spans = [
            Span.from_faker_span(new_span) for new_span in faker_spans_result.spans
        ]
        return cls(
            full_text=faker_spans_result.fake,
            spans=spans,
            masked=faker_spans_result.template,
            create_tags_from_span=create_tags_from_span,
            scheme=scheme,
            template_id=faker_spans_result.template_id,
            **kwargs,
        )

    def __repr__(self):
        return (
            f"Full text: {self.full_text}\n"
            f"Spans: {self.spans}\n"
            f"Tokens: {self.tokens}\n"
            f"Tags: {self.tags}\n"
        )

    def to_dict(self):

        return {
            "full_text": self.full_text,
            "masked": self.masked,
            "spans": [span.__dict__ for span in self.spans],
            "tags": self.tags,
            "tokens": [t.text for t in self.tokens],
            "template_id": self.template_id,
            "metadata": self.metadata,
        }

    @classmethod
    def from_json(cls, data, **kwargs):
        if "spans" in data:
            data["spans"] = [Span.from_json(span) for span in data["spans"]]
        return cls(**data, create_tags_from_span=True, **kwargs)

    def get_tags(self, scheme="IOB", model_version="en_core_web_sm"):
        start_indices = [span.start_position for span in self.spans]
        end_indices = [span.end_position for span in self.spans]
        tags = [span.entity_type for span in self.spans]
        tokens = tokenize(self.full_text, model_version)

        labels = span_to_tag(
            scheme=scheme,
            text=self.full_text,
            tags=tags,
            starts=start_indices,
            ends=end_indices,
            tokens=tokens,
        )

        return tokens, labels

    def to_conll(self, translate_tags: bool) -> List[Dict[str, Any]]:
        """
        Turns a list of InputSample objects to a dictionary
        containing text, pos, tag, template_id and label.
        :param translate_tags: Whether to translate tags using the PRESIDIO_SPACY_ENTITIES dictionary
        :return: Dict
        """

        conll = []
        for i, token in enumerate(self.tokens):
            if translate_tags:
                label = self.translate_tag(
                    self.tags[i], PRIVY_ENTITIES, ignore_unknown=True
                )
            else:
                label = self.tags[i]
            conll.append(
                {
                    "text": token.text,
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "template_id": self.template_id,
                    "label": label,
                },
            )

        return conll

    def get_template_id(self):
        if not self.template_id:
            return self.metadata.get("template_id")

    @staticmethod
    def create_conll_dataset(
        dataset: Union[List["InputSample"], List[FakerSpansResult]],
        translate_tags=False,
        # translator=PRIVY_ENTITIES,
        to_bio=True,
        token_model_version="en_core_web_sm"
    ) -> pd.DataFrame:

        if len(dataset) <= 1:
            raise ValueError("Dataset should contain multiple records")

        if isinstance(dataset[0], FakerSpansResult):
            dataset = [
                InputSample.from_faker_spans_result(
                    record, create_tags_from_span=True, scheme="BILUO", token_model_version=token_model_version
                )
                for record in tqdm(dataset, desc="Translating spans into tokens")
            ]

        conlls = []
        i = 0
        for sample in tqdm(dataset):
            if to_bio:
                sample.biluo_to_bio()
            conll = sample.to_conll(translate_tags=translate_tags)
            for token in conll:
                token["sentence"] = i
                conlls.append(token)
            i += 1

        return pd.DataFrame(conlls)

    def to_spacy(
        self, entities=None, translate_tags=True
    ) -> Tuple[str, Dict[str, List]]:
        """
        Translates an input sample into a format which can be consumed by spaCy during training.
        :param entities: Specific entities to focus on.
        :param translate_tags: Whether to translate the existing tags into spaCy tags (PERSON, LOC, GPE, ORG)
        :return: text and a dictionary containing a list of entities, e.g.
        "Bob is my name", {"entities": [(0, 3, "PERSON")]}
        """
        entities = [
            (span.start_position, span.end_position, span.entity_type)
            for span in self.spans
            if (entities is None) or (span.entity_type in entities)
        ]
        new_entities = []
        if translate_tags:
            for entity in entities:
                new_tag = self.translate_tag(
                    entity[2], PRESIDIO_SPACY_ENTITIES, ignore_unknown=True
                )
                new_entities.append((entity[0], entity[1], new_tag))
        else:
            new_entities = entities
        return self.full_text, {"entities": new_entities}

    @classmethod
    def from_spacy_doc(
        cls, doc: Doc, translate_tags: bool = True, scheme: str = "BILUO"
    ) -> "InputSample":
        if scheme not in ("BILUO", "BILOU", "BIO", "IOB"):
            raise ValueError('scheme should be one of "BILUO","BILOU","BIO","IOB"')

        spans = []
        for ent in doc.ents:
            entity_type = (
                cls.rename_from_spacy_tag(ent.label_) if translate_tags else ent.label_
            )
            span = Span(
                entity_type=entity_type,
                entity_value=ent.text,
                start_position=ent.start_char,
                end_position=ent.end_char,
            )
            spans.append(span)

        tags = [
            f"{token.ent_iob_}-{token.ent_type_}" if token.ent_iob_ != "O" else "O"
            for token in doc
        ]
        if scheme in ("BILUO", "BILOU"):
            tags = iob_to_biluo(tags)

        return cls(
            full_text=doc.text,
            masked=None,
            spans=spans,
            tokens=doc,
            tags=tags,
            create_tags_from_span=False,
            scheme=scheme,
        )

    @staticmethod
    def get_spacy(model_version="en_core_web_sm"):
        # add custom rules to spacy tokenizer to break down html, xml, sql into single tokens
        print("loading model {}".format(model_version))
        nlp = spacy.load(model_version)
        # split on these additional characters =' is for sql queries, < and > for html, xml)
        infixes = nlp.Defaults.infixes + [r'([><(=\'),"])']
        nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer

        for tagName in "html body i br p".split():
            nlp.tokenizer.add_special_case(f"<{tagName}>", [{ORTH: f"<{tagName}>"}])
            nlp.tokenizer.add_special_case(f"</{tagName}>", [{ORTH: f"</{tagName}>"}])

        for tagName in "br p".split():
            nlp.tokenizer.add_special_case(f"<{tagName}/>", [{ORTH: f"<{tagName}/>"}])

        for tagName in "html body i br p".split():
            nlp.tokenizer.add_special_case(f"<{tagName}>", [{ORTH: f"<{tagName}>"}])
            nlp.tokenizer.add_special_case(f"</{tagName}>", [{ORTH: f"</{tagName}>"}])
        return nlp

    @staticmethod
    def create_spacy_dataset(
        dataset: List["InputSample"],
        output_path: Optional[str] = None,
        entities: List[str] = None,
        sort_by_template_id: bool = False,
        translate_tags: bool = True,
        spacy_pipeline: Optional[Language] = None,
        alignment_mode: str = "expand",
    ) -> List[Tuple[str, Dict]]:
        """
        Creates a dataset which can be used to train spaCy models.
        If output_path is provided, it also saves the dataset in a spacy format.
        See https://spacy.io/usage/training#training-data

        :param dataset: List[InputSample] to create the dataset from
        :param output_path: Location for the created spacy dataset
        :param entities: List of entities to use
        :param sort_by_template_id: Whether to sort by template id (assuming the data is generated using templates)
        :param translate_tags: Whether to translate tags to spacy tags (PERSON, LOC, GPE, ORG)
        :param spacy_pipeline: The spaCy pipeline to use when creating the spaCy dataset. Default is en_core_web_sm
        :param alignment_mode: See `Doc.char_span`
        :return: a list of input samples translated to the spacy annotation structure
        [("Bob is my name, {"entities": [(0, 3, "PERSON")]})]
        """

        def template_sort(x):
            return x.metadata["template_id"]

        if sort_by_template_id:
            dataset.sort(key=template_sort)

        if not spacy_pipeline:
            spacy_pipeline = InputSample.get_spacy()

        spacy_dataset = [
            sample.to_spacy(entities=entities, translate_tags=translate_tags)
            for sample in dataset
        ]

        # Remove 'O' spans (if certain entities were ignored)
        for sample in spacy_dataset:
            if sample[1]["entities"]:
                new_entities = [
                    span for span in sample[1]["entities"] if span[2] != "O"
                ]
                sample[1]["entities"] = new_entities

        if output_path:
            db = DocBin()
            for text, annotations in spacy_dataset:
                doc = spacy_pipeline(text)
                ents = []
                for start, end, label in annotations["entities"]:
                    if start >= end:
                        print(
                            f"Span has zero or negative size, skipping. {(start, end, label)} in text={text}"
                        )
                        continue
                    if label == "O" or not label:
                        print("Skipping missing or non-entity ('O') spans")
                        continue
                    span = doc.char_span(
                        start, end, label=label, alignment_mode=alignment_mode
                    )
                    if not span:
                        print(
                            f"Skipping illegal span {(start, end, label)}, text={text[start:end]}, full text={text}"
                        )
                        continue
                    ents.append(span)
                doc.ents = ents
                db.add(doc)
            db.to_disk(output_path)

        return spacy_dataset

    @staticmethod
    def to_json(dataset: List["InputSample"], output_file: Union[str, Path]):
        """
        Save the InputSample dataset to json.
        :param dataset: list of InputSample objects
        :param output_file: path to file
        """

        examples_json = [example.to_dict() for example in dataset]

        with open("{}".format(output_file), "w+", encoding="utf-8") as f:
            json.dump(examples_json, f, ensure_ascii=False, indent=4)

    def to_spacy_doc(self):
        doc = self.tokens
        spacy_spans = []
        for span in self.spans:
            start_token = [
                token.i for token in self.tokens if token.idx == span.start_position
            ][0]
            end_token = [
                token.i
                for token in self.tokens
                if token.idx + len(token.text) == span.end_position
            ][0] + 1
            spacy_span = spacy.tokens.span.Span(
                doc, start=start_token, end=end_token, label=span.entity_type
            )
            spacy_spans.append(spacy_span)
        doc.ents = spacy_spans
        return doc

    @staticmethod
    def translate_tag(tag: str, dictionary: Dict[str, str], ignore_unknown: bool):
        has_prefix = len(tag) > 2 and tag[1] == "-"
        no_prefix = tag[2:] if has_prefix else tag
        if no_prefix in dictionary.keys():
            return (
                tag[:2] + dictionary[no_prefix] if has_prefix else dictionary[no_prefix]
            )
        else:
            if ignore_unknown:
                return "O"
            else:
                return tag

    def biluo_to_bio(self):
        new_tags = []
        for tag in self.tags:
            new_tag = tag
            has_prefix = len(tag) > 2 and tag[1] == "-"
            if has_prefix:
                if tag[0] == "U":
                    new_tag = "B" + tag[1:]
                elif tag[0] == "L":
                    new_tag = "I" + tag[1:]
            new_tags.append(new_tag)

        self.tags = new_tags

    @staticmethod
    def rename_from_spacy_tag(spacy_tag, ignore_unknown=False):
        return InputSample.translate_tag(
            spacy_tag, SPACY_PRESIDIO_ENTITIES, ignore_unknown=ignore_unknown
        )

    @staticmethod
    def rename_to_spacy_tags(tag, ignore_unknown=True):
        return InputSample.translate_tag(
            tag, PRESIDIO_SPACY_ENTITIES, ignore_unknown=ignore_unknown
        )

    def to_flair(self):
        for i, token in enumerate(self.tokens):
            return f"{token} {token.pos_} {self.tags[i]}"

    def translate_input_sample_tags(self, dictionary=None, ignore_unknown=True):
        if dictionary is None:
            dictionary = PRESIDIO_SPACY_ENTITIES

        # Translate tags
        self.tags = [
            InputSample.translate_tag(tag, dictionary, ignore_unknown=ignore_unknown)
            for tag in self.tags
        ]

        # Translate spans
        for span in self.spans:
            if span.entity_type in dictionary:
                span.entity_type = dictionary[span.entity_type]
            elif ignore_unknown:
                span.entity_value = "O"

        # Remove spans if they were changed to "O"
        self.spans = [span for span in self.spans if span.entity_type != "O"]

    @staticmethod
    def create_flair_dataset(dataset: List["InputSample"]) -> List[str]:
        flair_samples = []
        for sample in dataset:
            flair_samples.append(sample.to_flair())

        return flair_samples

    @staticmethod
    def read_dataset_json(
        filepath: Union[Path, str] = None, length: Optional[int] = None, **kwargs
    ) -> List["InputSample"]:
        """
        Reads an existing dataset, stored in json into a list of InputSample objects
        :param filepath: Path to json file
        :param length: Number of records to return (would return 0-length)
        :return: List[InputSample]
        """
        with open(filepath, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        if length:
            dataset = dataset[:length]

        input_samples = [
            InputSample.from_json(row, **kwargs) for row in tqdm(dataset, desc="tokenizing input")
        ]

        return input_samples

    @classmethod
    def convert_faker_spans(cls, fake_records: List[FakerSpansResult]) -> List["InputSample"]:
        """tokenize and transform fake samples to list of InputSample objects (data structure in presidio)"""
        input_samples = [
            # InputSample.from_faker_spans_result(faker_spans_result=fake_record)
            InputSample.from_faker_spans_result(
                fake_record, create_tags_from_span=True, scheme="BILUO", token_model_version="en_core_web_sm"
            )
            for fake_record in tqdm(fake_records)
        ]
        return input_samples

    @classmethod
    def count_entities(cls, input_samples: List["InputSample"]) -> Counter:
        count_per_entity_new = Counter()
        for record in input_samples:
            for span in record.spans:
                count_per_entity_new[span.entity_type] += 1
        return count_per_entity_new.most_common()

    @classmethod
    def remove_unsupported_entities(cls, dataset: List["InputSample"], entity_mapping: Dict[str, str]) -> None:
        """Remove records with unsupported entities using passed in entity mapping translator."""
        filtered_records = []
        excluded_entities = set()

        for sample in dataset:
            supported = True
            for span in sample.spans:
                if not span.entity_type in entity_mapping.keys():
                    supported = False
                    if span.entity_type not in excluded_entities:
                        print(f"Filtering out unsupported entity {span.entity_type}")
                    excluded_entities.add(span.entity_type)
            if supported:
                filtered_records.append(sample)
        return filtered_records
