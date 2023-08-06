from collections import Counter
from typing import List, Optional, Dict
import plotly.express as px
import plotly
from wordcloud import WordCloud
from PIL import Image
import string
import numpy as np
import pandas as pd
from tqdm import tqdm
from copy import deepcopy
from pathlib import Path

from presidio_evaluator import InputSample
from presidio_evaluator.evaluation import EvaluationResult, ModelError
from presidio_evaluator.models import BaseModel


class Evaluator:
    def __init__(
        self,
        model: BaseModel,
        verbose: bool = False,
        compare_by_io=True,
        entities_to_keep: Optional[List[str]] = None,
    ):
        """
        Evaluate a PII detection model or a Presidio analyzer / recognizer

        :param model: Instance of a fitted model (of base type BaseModel)
        :param compare_by_io: True if comparison should be done on the entity
        level and not the sub-entity level
        :param entities_to_keep: List of entity names to focus the evaluator on (and ignore the rest).
        Default is None = all entities. If the provided model has a list of entities to keep,
        this list would be used for evaluation.
        """
        self.model = model
        self.verbose = verbose
        self.compare_by_io = compare_by_io
        self.entities_to_keep = entities_to_keep
        if self.entities_to_keep is None and self.model.entities:
            self.entities_to_keep = self.model.entities

    def compare(self, input_sample: InputSample, prediction: List[str]):
        """
        Compares ground truth tags (annotation) and predicted (prediction)
        :param input_sample: input sample containing list of tags with scheme
        :param prediction: predicted value for each token
        self.labeling_scheme

        """
        annotation = input_sample.tags
        tokens = input_sample.tokens

        if len(annotation) != len(prediction):
            print(
                "Annotation and prediction do not have the"
                "same length. Sample={}".format(input_sample)
            )
            return Counter(), []

        results = Counter()
        mistakes = []

        new_annotation = annotation.copy()

        if self.compare_by_io:
            new_annotation = self._to_io(new_annotation)
            prediction = self._to_io(prediction)

        # Ignore annotations that aren't in the list of
        # requested entities.
        if self.entities_to_keep:
            prediction = self._adjust_per_entities(prediction)
            new_annotation = self._adjust_per_entities(new_annotation)
        for i in range(0, len(new_annotation)):
            # skip punctuation labeled as entity
            if tokens[i].text in string.punctuation or tokens[i].text in ["\\n", "\\t", " ", "", " \\n", "\\n "]:
                continue
            results[(new_annotation[i], prediction[i])] += 1

            if self.verbose:
                print("Annotation:", new_annotation[i])
                print("Prediction:", prediction[i])
                print(results)

            # check if there was an error
            is_error = new_annotation[i] != prediction[i]
            if is_error:
                if prediction[i] == "O":
                    mistakes.append(
                        ModelError(
                            error_type="FN",
                            annotation=new_annotation[i],
                            prediction=prediction[i],
                            token=tokens[i],
                            full_text=input_sample.full_text,
                            metadata=input_sample.metadata,
                        )
                    )
                elif new_annotation[i] == "O":
                    mistakes.append(
                        ModelError(
                            error_type="FP",
                            annotation=new_annotation[i],
                            prediction=prediction[i],
                            token=tokens[i],
                            full_text=input_sample.full_text,
                            metadata=input_sample.metadata,
                        )
                    )
                else:
                    mistakes.append(
                        ModelError(
                            error_type="Wrong entity",
                            annotation=new_annotation[i],
                            prediction=prediction[i],
                            token=tokens[i],
                            full_text=input_sample.full_text,
                            metadata=input_sample.metadata,
                        )
                    )

        return results, mistakes

    def _adjust_per_entities(self, tags):
        if self.entities_to_keep:
            return [tag if tag in self.entities_to_keep else "O" for tag in tags]
        else:
            return tags

    @staticmethod
    def _to_io(tags):
        """
        Translates BILUO/BIO/IOB to IO - only In or Out of entity.
        ['B-PERSON','I-PERSON','L-PERSON'] is translated into
        ['PERSON','PERSON','PERSON']
        :param tags: the input tags in BILUO/IOB/BIO format
        :return: a new list of IO tags
        """
        return [tag[2:] if "-" in tag else tag for tag in tags]

    def evaluate_sample(
        self, sample: InputSample, prediction: List[str]
    ) -> EvaluationResult:
        if self.verbose:
            print("Input sentence: {}".format(sample.full_text))

        results, mistakes = self.compare(input_sample=sample, prediction=prediction)
        return EvaluationResult(results, mistakes, sample.full_text)

    def evaluate_all(self, dataset: List[InputSample]) -> List[EvaluationResult]:
        evaluation_results = []
        if self.model.entity_mapping:
            print(
                f"Mapping entity values using this dictionary: {self.model.entity_mapping}"
            )
        for sample in tqdm(dataset, desc=f"Evaluating {self.model.__class__}"):

            # Align tag values to the ones expected by the model
            self.model.align_entity_types(sample)

            # Predict
            prediction = self.model.predict(sample)

            # Remove entities not requested
            prediction = self.model.filter_tags_in_supported_entities(prediction)

            # Switch to requested labeling scheme (IO/BIO/BILUO)
            prediction = self.model.to_scheme(prediction)

            evaluation_result = self.evaluate_sample(
                sample=sample, prediction=prediction
            )
            evaluation_results.append(evaluation_result)
        print(f"Entity counts after mapping: {InputSample.count_entities(dataset)}")

        return evaluation_results

    @staticmethod
    def align_entity_types(
        input_samples: List[InputSample],
        entities_mapping: Dict[str, str] = None,
        allow_missing_mappings: bool = False,
    ) -> List[InputSample]:
        """
        Change input samples to conform with Presidio's entities
        :return: new list of InputSample
        """

        new_input_samples = input_samples.copy()

        # A list that will contain updated input samples,
        new_list = []

        for input_sample in new_input_samples:
            contains_field_in_mapping = False
            new_spans = []
            # Update spans to match the entity types in the values of entities_mapping
            for span in input_sample.spans:
                if span.entity_type in entities_mapping.keys():
                    new_name = entities_mapping.get(span.entity_type)
                    span.entity_type = new_name
                    contains_field_in_mapping = True

                    new_spans.append(span)
                else:
                    if not allow_missing_mappings:
                        raise ValueError(
                            f"Key {span.entity_type} cannot be found in the provided entities_mapping"
                        )
            input_sample.spans = new_spans

            # Update tags in case this sample has relevant entities for evaluation
            if contains_field_in_mapping:
                for i, tag in enumerate(input_sample.tags):
                    has_prefix = "-" in tag
                    if has_prefix:
                        prefix = tag[:2]
                        clean = tag[2:]
                    else:
                        prefix = ""
                        clean = tag

                    if clean in entities_mapping.keys():
                        new_name = entities_mapping.get(clean)
                        input_sample.tags[i] = "{}{}".format(prefix, new_name)
                    else:
                        input_sample.tags[i] = "O"

            new_list.append(input_sample)

        return new_list
        # Iterate on all samples

    def calculate_score(
        self,
        evaluation_results: List[EvaluationResult],
        entities: Optional[List[str]] = None,
        beta: float = 2.5,
    ) -> EvaluationResult:
        """
        Returns the pii_precision, pii_recall, f_measure either and number of records for each entity
        or for all entities (ignore_entity_type = True)
        :param evaluation_results: List of EvaluationResult
        :param entities: List of entities to calculate score to. Default is None: all entities
        :param beta: F measure beta value
        between different entity types, or to treat these as misclassifications
        :return: EvaluationResult with precision, recall and f measures
        """

        # aggregate results
        all_results = sum([er.results for er in evaluation_results], Counter())

        # compute pii_recall per entity
        entity_recall = {}
        entity_precision = {}
        n = {}
        if not entities:
            entities = list(set([x[0] for x in all_results.keys() if x[0] != "O"]))

        for entity in entities:
            # all annotation of given type
            annotated = sum([all_results[x] for x in all_results if x[0] == entity])
            predicted = sum([all_results[x] for x in all_results if x[1] == entity])
            n[entity] = annotated
            tp = all_results[(entity, entity)]

            if annotated > 0:
                entity_recall[entity] = tp / annotated
            else:
                entity_recall[entity] = np.NaN

            if predicted > 0:
                per_entity_tp = all_results[(entity, entity)]
                entity_precision[entity] = per_entity_tp / predicted
            else:
                entity_precision[entity] = np.NaN

        # compute pii_precision and pii_recall
        annotated_all = sum([all_results[x] for x in all_results if x[0] != "O"])
        predicted_all = sum([all_results[x] for x in all_results if x[1] != "O"])
        if annotated_all > 0:
            pii_recall = (
                sum(
                    [
                        all_results[x]
                        for x in all_results
                        if (x[0] != "O" and x[1] != "O")
                    ]
                )
                / annotated_all
            )
        else:
            pii_recall = np.NaN
        if predicted_all > 0:
            pii_precision = (
                sum(
                    [
                        all_results[x]
                        for x in all_results
                        if (x[0] != "O" and x[1] != "O")
                    ]
                )
                / predicted_all
            )
        else:
            pii_precision = np.NaN
        # compute pii_f_beta-score
        pii_f_beta = self.f_beta(pii_precision, pii_recall, beta)

        # aggregate errors
        errors = []
        for res in evaluation_results:
            if res.model_errors:
                errors.extend(res.model_errors)

        evaluation_result = EvaluationResult(
            results=all_results,
            model_errors=errors,
            pii_precision=pii_precision,
            pii_recall=pii_recall,
            entity_recall_dict=entity_recall,
            entity_precision_dict=entity_precision,
            n_dict=n,
            pii_f=pii_f_beta,
            n=sum(n.values()),
        )

        return evaluation_result

    @staticmethod
    def precision(tp: int, fp: int) -> float:
        return tp / (tp + fp + 1e-100)

    @staticmethod
    def recall(tp: int, fn: int) -> float:
        return tp / (tp + fn + 1e-100)

    @staticmethod
    def f_beta(precision: float, recall: float, beta: float) -> float:
        """
        Returns the F score for precision, recall and a beta parameter
        :param precision: a float with the precision value
        :param recall: a float with the recall value
        :param beta: a float with the beta parameter of the F measure,
        which gives more or less weight to precision
        vs. recall
        :return: a float value of the f(beta) measure.
        """
        if np.isnan(precision) or np.isnan(recall) or (precision == 0 and recall == 0):
            return np.nan

        return ((1 + beta ** 2) * precision * recall) / (
            ((beta ** 2) * precision) + recall
        )

    class ErrorAnalyzer:
        def __init__(self, model, results, errors, output_folder, model_name, path_to_wordcloud_image):
            self.model = model
            self.results = results
            self.errors = errors
            self.output_folder = output_folder
            self.model_name = model_name.replace("/", "-")
            self.path_to_image = path_to_wordcloud_image

        def plot_recall_precision_f2(self) -> None:
            """Plot per-entity recall and precision"""
            d = {}
            d['entity'] = deepcopy(list(self.results.entity_recall_dict.keys()))
            d['recall'] = deepcopy(list(self.results.entity_recall_dict.values()))
            d['precision'] = deepcopy(
                list(self.results.entity_precision_dict.values()))
            d['count'] = deepcopy(list(self.results.n_dict.values()))
            d['f2_score'] = [Evaluator.f_beta(precision=precision, recall=recall, beta=2.5)
                             for recall, precision in zip(d['recall'], d['precision'])]
            df = pd.DataFrame(d)
            df['model'] = self.model_name
            # self._plot(df, plot_type="Recall")
            # self._plot(df, plot_type="Precision")
            self._plot(df, plot_type="F2_Score")

            scores_output = self.output_folder / \
                f"scores-dict-{self.model_name}.json"
            df.to_csv(scores_output, index=False)

        def _plot(self, df, plot_type: str) -> None:
            fig = px.bar(df, text_auto=".2", y='entity', orientation="h",
                         x=f'{plot_type.lower()}', color='count', barmode='group', title=f"Per-entity {plot_type} for {self.model_name}")
            fig.update_layout(barmode='group', yaxis={
                'categoryorder': 'total ascending'})
            fig.update_layout(yaxis_title=f"{plot_type}", xaxis_title="PII Entity")
            fig.update_traces(textfont_size=12, textangle=0,
                              textposition="outside", cliponaxis=False)
            fig.update_layout(
                plot_bgcolor="#FFF",
                xaxis=dict(
                    title="PII entity",
                    linecolor="#BCCCDC",  # Sets color of X-axis line
                    showgrid=False  # Removes X-axis grid lines
                ),
                yaxis=dict(
                    title=f"{plot_type}",
                    linecolor="#BCCCDC",  # Sets color of X-axis line
                    showgrid=False  # Removes X-axis grid lines
                ),
            )
            filename = self.output_folder / \
                f"{plot_type.lower()}_{self.model_name}.html"
            plotly.offline.plot(
                fig, filename=str(filename))
            filename = self.output_folder / \
                f"{plot_type.lower()}_{self.model_name}.png"
            fig.write_image(filename)

        def _plot_multiple_models(score_files: List[Path], model_name: str, plot_type: str) -> None:
            """Plot per-entity Recall, Precision or F2 Score for multiple models given dataframes saved to csv during evaluation"""
            df = pd.read_csv(score_files[0])
            # combine score dataframes
            for file in score_files[1:]:
                df = pd.concat([df, pd.read_csv(file)])

            fig = px.bar(df, text_auto=".2", x='entity',
                         y=f'{plot_type.lower()}', color='model', barmode='group', title=f"Per-entity {plot_type} for {model_name}")
            fig.update_layout(barmode='group', xaxis={
                'categoryorder': 'total ascending'})
            fig.update_layout(yaxis_title=f"{plot_type}", xaxis_title="PII Entity")
            fig.update_traces(textfont_size=12, textangle=0,
                              textposition="outside", cliponaxis=False)
            fig.update_layout(
                plot_bgcolor="#FFF",
                xaxis=dict(
                    title="PII entity",
                    linecolor="#BCCCDC",  # Sets color of X-axis line
                    showgrid=False  # Removes X-axis grid lines
                ),
                yaxis=dict(
                    title="Recall",
                    linecolor="#BCCCDC",  # Sets color of X-axis line
                    showgrid=False  # Removes X-axis grid lines
                ),
            )
            fig.show()

        def save_errors(self):
            ModelError.most_common_fp_tokens(self.errors)

            for entity in self.model.entity_mapping.values():
                fps_df = ModelError.get_fps_dataframe(self.errors, entity=[entity])
                if fps_df is not None:
                    fps_df.to_csv(self.output_folder /
                                  f"{self.model_name}-{entity}-fps.csv")
                    fps_df = pd.read_csv(self.output_folder /
                                         f"{self.model_name}-{entity}-fps.csv")
                    self.generate_wordcloud(
                        fps_df, entity, error_type="fps", path_to_image=self.path_to_image)
                fns_df = ModelError.get_fns_dataframe(self.errors, entity=[entity])
                if fns_df is not None:
                    fns_df.to_csv(self.output_folder /
                                  f"{self.model_name}-{entity}-fns.csv")
                    fns_df = pd.read_csv(self.output_folder /
                                         f"{self.model_name}-{entity}-fns.csv")
                    self.generate_wordcloud(
                        fns_df, entity, error_type="fns", path_to_image=self.path_to_image)

        def generate_wordcloud(self, df, entity, error_type, path_to_image):
            text = ' '.join(str(v) for v in df['token'])
            if not text:
                return
            alice_mask = np.array(Image.open(path_to_image))
            # alice_mask = np.array(Image.open(Path(__file__).with_name(path_to_image)))
            wc = WordCloud(stopwords=["testing"], background_color="black", max_font_size=100, max_words=1000, mask=alice_mask,
                           contour_width=0)
            # generate word cloud
            wc.generate(text)
            # store to file
            wc.to_file(self.output_folder /
                       f"{self.model_name}-{entity}-{error_type}-wordcloud.png")

        def graph_most_common_tokens(self):

            def group(df):
                return df.groupby(['token', 'annotation']).size().to_frame(
                ).sort_values([0], ascending=False).head(30).reset_index()

            def generate_graph(type, type_title):
                df_loc = pd.read_csv(self.output_folder /
                                     f"{self.model_name}-LOC-{type}.csv")
                df_loc = group(df_loc)

                if "presidio" in self.model_name:
                    df_org = pd.read_csv(self.output_folder /
                                         f"{self.model_name}-NRP-{type}.csv")
                    df_org = group(df_org)
                else:
                    df_org = pd.read_csv(self.output_folder /
                                         f"{self.model_name}-ORG-{type}.csv")
                    df_org = group(df_org)
                df_person = pd.read_csv(self.output_folder /
                                        f"{self.model_name}-PERSON-{type}.csv")
                df_person = group(df_person)
                dfg = pd.concat([df_loc.head(3), df_org.head(3), df_person.head(3)])

                fig = px.histogram(dfg, x=0, y="token", orientation='h', color='annotation',
                                   title=f"Most common {type_title} for {self.model_name}")

                fig.update_layout(yaxis_title=f"count", xaxis_title="PII Entity")
                fig.update_traces(textfont_size=12, textangle=0,
                                  textposition="outside", cliponaxis=False)
                fig.update_layout(
                    plot_bgcolor="#FFF",
                    xaxis=dict(
                        title="Count",
                        linecolor="#BCCCDC",  # Sets color of X-axis line
                        showgrid=False  # Removes X-axis grid lines
                    ),
                    yaxis=dict(
                        title=f"Tokens",
                        linecolor="#BCCCDC",  # Sets color of X-axis line
                        showgrid=False  # Removes X-axis grid lines
                    ),
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                fig.write_image(self.output_folder /
                                f"{self.model_name}-most-common-{type}.png")

            generate_graph(type="fns", type_title="false negatives")
            generate_graph(type="fps", type_title="false positives")
