from itertools import chain
from operator import attrgetter
from typing import Optional

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

from src.ConnectedPapersExtractor import PdfSummary, PdfSummaries


def conv2docs(
    summaries: PdfSummaries, embeddings: Optional[Embeddings] = None
) -> PdfSummaries:
    if embeddings is None:
        embeddings = OpenAIEmbeddings()
    for summary in summaries:
        raw_documents = summary.extract_documents()
        raw_text = "\n\n\n".join(map(attrgetter("page_content"), raw_documents))
        text_splitter = SemanticChunker(
            embeddings, breakpoint_threshold_type="interquartile"
        )
        summary.docs = text_splitter.create_documents([raw_text])
    return summaries
