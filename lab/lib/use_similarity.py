#!/usr/bin/env python

from absl import logging
import tensorflow_hub as hub
import tensorflow as tf
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

logging.set_verbosity(logging.ERROR)

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


def top_pairs(keyToDoc: dict, topN):
    names, documents = [list(x) for x in zip(*keyToDoc.items())]

    embeddings = np.array(embed(documents)).tolist()

    global_top_scores = []
    for first_idx, _ in enumerate(embeddings):
        offset = first_idx + 1
        # Do not record flipped duplicates. Must include self match for some reason?
        cosine_similarities = linear_kernel(
            embeddings[offset - 1 : offset], embeddings[offset - 1 :]
        ).flatten()

        # convert back to native Python dtypes.
        document_scores = [item.item() for item in cosine_similarities[1:]]

        # Top scores for this subset.
        sorted_top_scores = sorted(
            enumerate(document_scores), reverse=True, key=lambda x: x[1]
        )[:topN]

        matches = [
            (first_idx, other_idx + offset, score)
            for other_idx, score in sorted_top_scores
        ]
        global_top_scores = global_top_scores + matches

    # Return highest scoring matches globally.
    top_index_matches = sorted(global_top_scores, reverse=True, key=lambda x: x[2])[
        :topN
    ]

    # Return the OG keys.
    return [
        (names[first_idx], names[other_idx], score)
        for first_idx, other_idx, score in top_index_matches
    ]
