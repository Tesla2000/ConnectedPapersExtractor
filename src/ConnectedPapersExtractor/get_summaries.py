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
    connectedpapers_url: str,
    chain: Chain,
    pdf_output: Union[Path, str] = None,
    article_filter: ArticleFilter = _NoFilter(),
) -> list[PdfSummary]:
    temp_pdf = pdf_output or Path(__file__).parent.joinpath("_temp_pfd_files")
    temp_pdf.mkdir(exist_ok=True, parents=True)
    summaries = _get_pdf_summaries(connectedpapers_url, temp_pdf)
    filtered_summaries = article_filter.filter(summaries)
    output_summaries = list(
        summary.extract_text(chain) for summary in filtered_summaries
    )
    if temp_pdf != pdf_output:
        shutil.rmtree(temp_pdf)
    return output_summaries
