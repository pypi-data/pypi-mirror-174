import warnings

import lemminflect
import spacy
from spacy.tokens import Token, Doc

from replacy.db import get_forms_lookup


class Inflector:
    def __init__(self, nlp=None, forms_lookup=None):

        self.nlp = nlp
        if not self.nlp:
            self.nlp = spacy.load("en_core_web_sm")

        self.forms_lookup = forms_lookup
        if not self.forms_lookup:
            self.forms_lookup = get_forms_lookup()

    def get_dict_form(self, word, tag):
        for k in self.forms_lookup:
            if (
                word in self.forms_lookup[k].values()
                and tag in self.forms_lookup[k].keys()
            ):
                return self.forms_lookup[k][tag]
        return None

    def auto_inflect(
        self,
        doc: Doc,
        suggest_text: str,
        suggest_index: int,
        generated_suggestions_obj: list,
        match_inflect_index: int,
        match_start: int,
        match_end: int,
    ):
        """
        Inflect the suggestion using token at position 'index' as template.
        ex. (washed, eat) => ate
        Returns inflected suggestion as text.
        If the inflection is not supported, check verb_forms.json
        if not found - returns None.
        """
        suggestions_separator = " "
        suggestion_items = []
        corrected_suggest_index = suggest_index
        for idx, generated_suggestion in enumerate(generated_suggestions_obj):
            if len(generated_suggestion["generated"]):
                if idx == suggest_index:
                    suggestion_items.append(suggest_text)
                else:
                    suggestion_items.append(generated_suggestion["generated"][0])
                    if idx < suggest_index:
                        # I should split this by suggestion_separator instead of spaces
                        # in case of an empty string as suggestion_separator,
                        # we need to do the mapping before calling SuggestionGenerator.get_options
                        # I went with spaces now, as it covers most of the cases
                        # usually when we use inflection, we deal with suggestion of single
                        # or multiple words separated by a space
                        generated_suggestion_length = len(
                            generated_suggestion["generated"][0].split(" ")
                        )
                        if generated_suggestion_length > 1:
                            corrected_suggest_index += generated_suggestion_length - 1
            else:  # if suggestion item has empty suggestion options, then move the index 1 item before
                if idx < suggest_index:
                    corrected_suggest_index -= 1

        suggestion = suggestions_separator.join(suggestion_items)

        match_inflect_token = doc[match_inflect_index]

        space_before_suggestion = (
            doc[match_start].whitespace_ if match_start > 0 else ""
        )
        space_after_suggestion = (
            doc[match_end - 1].whitespace_ if match_end < len(doc) else ""
        )
        changed_sentence = "".join(
            [
                doc[:match_start].text,
                space_before_suggestion,
                suggestion,
                space_after_suggestion,
                doc[match_end:].text,
            ]
        )
        changed_doc = self.nlp(changed_sentence)
        changed_token = changed_doc[match_start + corrected_suggest_index]

        return self.inflect_or_lookup(changed_token, match_inflect_token.tag_)

    @staticmethod
    def tag_to_pos(tag):
        if tag in ["JJ", "JJR", "JJS"]:
            return "ADJ"
        elif tag in ["RB", "RBR", "RBS"]:
            return "ADV"
        elif tag in ["NN", "NNS"]:
            return "NOUN"
        elif tag in ["NNP", "NNPS"]:
            return "PROPN"
        elif tag in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]:
            return "VERB"  # AUX
        else:
            return tag

    def get_inflection_type(self, value: str):
        pos_values = ["ADJ", "ADV", "NOUN", "PROPN", "VERB", "AUX"]
        if value in pos_values:
            return "pos"
        elif Inflector.tag_to_pos(value) in pos_values:
            return "tag"
        elif value == "ALL":
            return "all"
        else:
            warnings.warn(
                f"Inflection <<{value}>> not supported, will fallback to <<ALL>>."
            )
            return "all"

    def get_lemmas(self, word, tag=None, pos=None):

        lemmas = []

        if tag:
            # infer pos from tag
            pos = Inflector.tag_to_pos(tag)

        if pos:
            lemma_dict = lemminflect.getLemma(word, upos=pos)
            lemmas = list(lemma_dict)
        else:
            # no pos provided, return all lemmas
            lemma_dict = lemminflect.getAllLemmas(word)
            for i in lemma_dict.values():
                lemmas += list(i)

        return lemmas

    def inflect_lemma(self, lemma, tag=None, pos=None):

        inflections = []
        # tag based
        if tag:
            inflection_tuple = lemminflect.getInflection(lemma, tag=tag)
            inflections = list(inflection_tuple)
        else:
            # pos based, can be None too
            inflection_dict = lemminflect.getAllInflections(lemma, upos=pos)
            for i in inflection_dict.values():
                inflections += list(i)

        return inflections

    def inflect_token(self, token: Token, tag=None, pos=None):

        if tag:
            # dictionary look up
            # returns None if not found
            inflection = self.get_dict_form(token.lemma_, tag=tag)

            if not inflection:
                # tag provided, spaCy inflection (has .lemma_)
                inflection = token._.inflect(tag)

            inflections = [inflection]
        else:
            # fallback to pyinflect inflection
            # get all inflections
            inflections = self.inflect_lemma(token.lemma_, tag=tag, pos=pos)

        return inflections

    def inflect_string(self, word: str, tag=None, pos=None):

        inflections = []

        # lemmatize
        lemmas = self.get_lemmas(word, tag=tag, pos=pos)
        for lemma in lemmas:
            # check dict forms first
            # those are potential corrections to lemminflect
            # returns None if not found
            lemma_i = [self.get_dict_form(lemma, tag=tag)]
            if not lemma_i[0]:
                lemma_i = self.inflect_lemma(lemma, tag=tag, pos=pos)
            inflections += lemma_i

        return inflections

    def inflect_or_lookup(self, word, tag=None, pos=None):
        if isinstance(word, Token):
            # token inflection tries spaCy ext (._.inflect)
            # with spaCy lemmatizer (.lemma_)
            return self.inflect_token(word, tag=tag, pos=pos)
        elif isinstance(word, str):
            return self.inflect_string(word, tag=tag, pos=pos)
