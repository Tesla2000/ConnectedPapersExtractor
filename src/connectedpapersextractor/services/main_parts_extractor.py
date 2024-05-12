from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import numpy as np
import openai
from injector import inject

from src.connectedpapersextractor.article import Documents


@inject
class MainPartsExtractorService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def extract(self, docs: Documents) -> Documents:
        pass


class DefaultMainPartsExtractorService(MainPartsExtractorService):
    def extract(self, docs: Documents) -> Documents:
        return docs
    # array = _get_embeddings(docs)
    # num_clusters = 5
    # dimension = array.shape[1]
    # kmeans = faiss.Kmeans(dimension, num_clusters, niter=20, verbose=True)
    # kmeans.train(array)
    # centroids = kmeans.centroids
    # index = faiss.IndexFlatL2(dimension)
    # index.add(array)
    # D, I = index.search(centroids, 1)
    # sorted_array = np.sort(I, axis=0)
    # sorted_array = sorted_array.flatten()
    # return [summary.docs[i] for i in sorted_array]


default_extractor_service = DefaultMainPartsExtractorService()


def _get_embeddings(
    docs: Documents,
) -> np.ndarray:
    pages = [doc.page_content for doc in docs]
    embeddings = openai.embeddings.create(
        model="text-embedding-3-small", input=pages).data
    vectors = [embedding.embedding for embedding in embeddings]
    return np.array(vectors)
