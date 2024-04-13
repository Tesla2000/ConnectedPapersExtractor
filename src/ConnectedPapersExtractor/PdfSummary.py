from dataclasses import dataclass
from typing import Callable

from langchain.chains.base import Chain
from langchain_community.document_loaders.pdf import PyPDFLoader


@dataclass
class PdfSummary:
    year: int
    citations: int
    download_function: Callable[[], str]
    text: str = None

    def extract_text(self, chain: Chain) -> "PdfSummary":
        loader = PyPDFLoader(self.download_function())
        docs = loader.load()
        self.text = chain.run(docs)
        return self
