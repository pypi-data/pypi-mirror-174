from typing import List

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter


def draw_word_cloud(words_list: List[str], min_times: int = 10):
    stopwords = set(STOPWORDS)
    stopwords_parts = {"'s", " ' s'", " `s"}
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10)

    def skip_entity(e):
        if e in stopwords:
            return True
        for p in stopwords_parts:
            if p in e:
                return True
        return False

    c = Counter(words_list)
    # using the subject frquencies
    d = {k: v for k, v in dict(c).items() if v > min_times and not skip_entity(k)}
    wordcloud.generate_from_frequencies(d)
    plt.figure(figsize=(10, 20), facecolor=None)
    plt.imshow(wordcloud)
