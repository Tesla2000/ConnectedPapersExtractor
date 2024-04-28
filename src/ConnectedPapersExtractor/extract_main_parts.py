from typing import Optional, Callable

import faiss
import numpy as np
from langchain_core.documents import Document
from openai.types import Embedding

from . import PdfSummary
from ._get_embeddings import _get_embeddings


def extract_main_parts(
    summary: PdfSummary,
    embeddings_function: Optional[Callable[[list[str]], list[Embedding]]] = None,
    load_embeddings: bool = True,
) -> list[Document]:
    array = _get_embeddings(summary, embeddings_function, load_embeddings)
    num_clusters = 5
    dimension = array.shape[1]
    kmeans = faiss.Kmeans(dimension, num_clusters, niter=20, verbose=True)
    kmeans.train(array)
    centroids = kmeans.centroids
    index = faiss.IndexFlatL2(dimension)
    index.add(array)
    D, I = index.search(centroids, 1)
    sorted_array = np.sort(I, axis=0)
    sorted_array = sorted_array.flatten()
    return [summary.docs[i] for i in sorted_array]
