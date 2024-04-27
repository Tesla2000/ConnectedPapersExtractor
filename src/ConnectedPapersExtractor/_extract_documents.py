from typing import Optional, Callable

import numpy as np
from chromadb import Embeddings
from langchain_core.documents import Document
from openai.types import Embedding

from . import PdfSummaries, Config
from ._get_embeddings import _get_embeddings


def _extract_documents(summaries: PdfSummaries, embeddings: Optional[Embeddings] = None, embeddings_function: Optional[Callable[[list[str]], list[Embedding]]] = None) -> list[Document]:
    if not summaries:
        raise ValueError("No summaries provided")
    embeddings_path = summaries[0].file_path.parent.joinpath(Config.embedding_file_name)
    if not summaries[0].file_path.parent.joinpath(Config.embedding_file_name).exists():
        array = _get_embeddings(summaries, embeddings_path, embeddings, embeddings_function)
    else:
        array = np.fromfile(embeddings_path)
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
    extracted_docs = [docs[i] for i in sorted_array]
