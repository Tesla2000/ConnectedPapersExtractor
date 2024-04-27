from itertools import chain
from operator import attrgetter
from pathlib import Path
from typing import Optional, Callable

import numpy as np
import openai
from langchain_core.embeddings import Embeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from openai.types import Embedding

from . import PdfSummaries, PdfSummary


def _openai_embed(pages: list[str]) -> list[Embedding]:
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=pages
    )
    return response.data


def _get_embeddings(summaries: PdfSummaries, embeddings_path: Path, embeddings: Optional[Embeddings] = None,
                    embeddings_function: Optional[Callable[[list[str]], list[Embedding]]] = None):
    if embeddings is None:
        embeddings = OpenAIEmbeddings()
    raw_documents = list(chain.from_iterable(map(PdfSummary.extract_documents, summaries)))
    raw_text = '\n\n\n'.join(map(attrgetter("page_content"), raw_documents))
    text_splitter = SemanticChunker(
        embeddings, breakpoint_threshold_type="interquartile"
    )
    docs = text_splitter.create_documents([raw_text])
    if embeddings_function is None:
        embeddings_function = _openai_embed
    embeddings = embeddings_function([doc.page_content for doc in docs])
    vectors = [embedding.embedding for embedding in embeddings]
    array = np.array(vectors)
    array = array.astype('float32')
    array.tofile(embeddings_path)
    return array
