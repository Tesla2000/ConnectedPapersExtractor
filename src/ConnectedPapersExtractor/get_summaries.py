import shutil
from pathlib import Path
from typing import Union

from langchain.chains.base import Chain

from .ArticleFilter import ArticleFilter
from .PdfSummary import PdfSummary
from ._get_pdf_summaries import _get_pdf_summaries


class _NoFilter(ArticleFilter):
    def filter(self, summaries: list[PdfSummary]) -> list[PdfSummary]:
        return summaries


def get_summaries(
    connected_papers_url: str,
    pdf_output: Union[Path, str, None] = None,
    article_filter: ArticleFilter = _NoFilter(),
) -> list[PdfSummary]:
    temp_pdf = pdf_output or Path(__file__).parent.joinpath("_temp_pfd_files")
    temp_pdf.mkdir(exist_ok=True, parents=True)
    summaries = tuple(PdfSummary(pdf_file) for pdf_file in temp_pdf.iterdir())
    if not summaries:
        summaries = _get_pdf_summaries(
            connected_papers_url,
            article_filter,
            temp_pdf,
        )
    if temp_pdf != pdf_output:
        shutil.rmtree(temp_pdf)
    return summaries
