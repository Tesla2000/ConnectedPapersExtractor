from dataclasses import dataclass
from pathlib import Path

from langchain.chains.base import Chain
from langchain_community.document_loaders.pdf import PyPDFLoader


@dataclass
class PdfSummary:
    path: Path
    year: int
    citations: int
    text: str = None

    def extract_text(self, chain: Chain) -> "PdfSummary":
        loader = PyPDFLoader(str(self.path))
        docs = loader.load()
        self.text = chain.run(docs)
        return self
