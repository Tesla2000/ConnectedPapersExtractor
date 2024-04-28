from operator import attrgetter
from typing import Optional

from langchain_core.embeddings import Embeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

from . import PdfSummary


def _add_docs(
    summary: PdfSummary, embeddings: Optional[Embeddings] = None
) -> PdfSummary:
    if embeddings is None:
        embeddings = OpenAIEmbeddings()
    raw_documents = summary.extract_documents()
    raw_text = "\n\n\n".join(map(attrgetter("page_content"), raw_documents))
    text_splitter = SemanticChunker(
        embeddings, breakpoint_threshold_type="interquartile"
    )
    summary.docs = text_splitter.create_documents([raw_text])
    return summary
