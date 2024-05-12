from operator import attrgetter
from typing import Optional

from langchain_text_splitters import TextSplitter

from src.connectedpapersextractor import PdfSummary


def add_docs(
    summary: PdfSummary, text_splitter: Optional[TextSplitter] = None
) -> PdfSummary:
    raw_documents = summary.extract_documents()
    raw_text = "\n\n\n".join(map(attrgetter("page_content"), raw_documents))
    if text_splitter is not None:
        summary.docs = text_splitter.create_documents([raw_text])
    else:
        summary.extract_documents()
    return summary
