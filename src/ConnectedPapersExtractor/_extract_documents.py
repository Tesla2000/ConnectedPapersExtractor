from itertools import chain
from operator import attrgetter
from typing import Sequence, Optional

import numpy as np
import openai
from langchain_core.documents import Document
from chromadb import Embeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

from src.ConnectedPapersExtractor import PdfSummary


def _get_embeddings(pages: list[str]):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=pages
    )
    return response.data


def _extract_documents(summaries: Sequence[PdfSummary], embeddings: Optional[Embeddings] = None) -> list[Document]:
    if embeddings is None:
        embeddings = OpenAIEmbeddings()
    raw_documents = list(chain.from_iterable(map(PdfSummary.extract_documents, summaries)))
    raw_text = '\n\n\n'.join(map(attrgetter("page_content"), raw_documents))
    text_splitter = SemanticChunker(
        embeddings, breakpoint_threshold_type="interquartile"
    )
    docs = text_splitter.create_documents([raw_text])
    embeddings = _get_embeddings([doc.page_content for doc in docs])
    content_list = [doc.page_content for doc in docs]
    df = pd.DataFrame(content_list, columns=['page_content'])
    vectors = [embedding.embedding for embedding in embeddings]
    array = np.array(vectors)
    embeddings_series = pd.Series(list(array))
    df['embeddings'] = embeddings_series
