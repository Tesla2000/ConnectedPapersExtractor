from dataclasses import dataclass

from arxiv import Result
from langchain.chains.base import Chain
from langchain_community.document_loaders.pdf import PyPDFLoader


@dataclass
class PdfSummary:
    year: int
    citations: int
    download_args: tuple[Result, str]
    text: str = None

    def extract_text(self, chain: Chain) -> "PdfSummary":
        arxiv_results, dir_path = self.download_args
        print(f"Downloading {arxiv_results.entry_id}...")
        pdf_file = arxiv_results.download_pdf(dirpath=dir_path)
        print("Downloaded")
        loader = PyPDFLoader(pdf_file)
        docs = loader.load()
        self.text = chain.run(docs)
        return self
