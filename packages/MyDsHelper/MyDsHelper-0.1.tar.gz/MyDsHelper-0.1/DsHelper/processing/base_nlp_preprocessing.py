import re
from functools import lru_cache
from typing import Optional, Callable, Set, List

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.snowball import PorterStemmer

from DsHelper.processing.base_preprocessor import BasePreProcessor


class BaseNlpPreProcessor(BasePreProcessor):
    def __init__(self, stemmer: Optional[Callable], stopwords: Optional[Set[str]],
                 punctuation: Optional[str], features_to_keep: List[str] = None):
        self.stemmer = PorterStemmer(ignore_stopwords=False) or stemmer
        self.stopwords = set(nltk.corpus.stopwords.words('english')) or stopwords
        self.punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@' or punctuation
        self.url_pattern = r'https?://\S+|www\.\S+'
        nltk.download('stopwords')
        nltk.download('punkt')
        super().__init__(features_to_keep)

    # Using caching for faster performance
    @lru_cache(maxsize=None)
    def _word_stemming(self, word: str) -> str:
        return self.stemmer.stem(word)

    def _remove_urls(self, word: str) -> str:
        url_pattern = re.compile(self.url_pattern)
        return url_pattern.sub(r'', word)

    def clean_text_col(self, txt: str, bigrams: False) -> str:
        txt = str(txt)
        txt = txt.lower()  # lower case
        txt = re.sub('[' + self.punctuation + ']+', ' ', txt)  # strip punctuation
        txt = re.sub(' +', ' ', txt)  # remove double spacing
        txt = re.sub('([0-9]+)', '', txt)  # remove numbers
        body_token_list = [word for word in txt.split(' ')
                           if word not in stopwords]  # remove stopwords

        body_token_list = [word.replace('"', '').replace('\'', '').strip() for word in
                           body_token_list]  # removing single/double quotes
        body_token_list = [self._remove_urls(word) for word in body_token_list]  # removing urls
        body_token_list = [self._word_stemming(word) for word in body_token_list]  # apply stemming

        if bigrams:
            body_token_list = body_token_list + [body_token_list[i] + '_' + body_token_list[i + 1]
                                                 for i in range(len(body_token_list) - 1)]
        txt = ' '.join(body_token_list)
        return txt

    def pre_process(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
