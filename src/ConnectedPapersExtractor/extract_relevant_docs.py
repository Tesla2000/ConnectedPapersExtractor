from typing import Optional, Callable

import faiss
import numpy as np
from chromadb import Embeddings
from langchain_core.documents import Document
from openai.types import Embedding

from . import PdfSummaries
from .conv2docs import conv2docs
from ._get_embeddings import _get_embeddings


def extract_relevant_docs(summaries: PdfSummaries, docs: list[Document], embeddings_function: Optional[Callable[[list[str]], list[Embedding]]] = None, load_embeddings: bool = True) -> list[Document]:
    if not summaries:
        raise ValueError("No summaries provided")
    array = _get_embeddings(summaries, docs, embeddings_function, load_embeddings)
    num_clusters = 50
    dimension = array.shape[1]
    kmeans = faiss.Kmeans(dimension, num_clusters, niter=20, verbose=True)
    kmeans.train(array)
    centroids = kmeans.centroids
    index = faiss.IndexFlatL2(dimension)
    index.add(array)
    D, I = index.search(centroids, 1)
    sorted_array = np.sort(I, axis=0)
    sorted_array = sorted_array.flatten()
    return [docs[i] for i in sorted_array]
