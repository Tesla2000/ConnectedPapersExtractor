import json
import shutil
from pathlib import Path
from typing import Union

from . import ArticleFilter, PdfSummaries
from . import PdfSummary
from ._get_pdf_summaries import _get_pdf_summaries
from .Config import Config


class _NoFilter(ArticleFilter):
    def filter(self, summaries: PdfSummaries) -> PdfSummaries:
        return summaries


def get_summaries(
    connected_papers_url: str,
    pdf_output: Union[Path, str, None] = None,
    article_filter: ArticleFilter = _NoFilter(),
) -> PdfSummaries:
    temp_pdf = pdf_output or Path(__file__).parent.joinpath(Config.temp_pdf_path)
    temp_pdf.mkdir(exist_ok=True, parents=True)
    summaries: list[PdfSummary] = list(
        filter(
            PdfSummary.is_valid,
            (PdfSummary(pdf_file) for pdf_file in temp_pdf.glob("*.pdf")),
        )
    )
    if not summaries:
        summaries = _get_pdf_summaries(
            connected_papers_url,
            temp_pdf,
        )
    else:
        metadata = json.loads(temp_pdf.joinpath(Config.metadate_file_name).read_text())
        for summary in summaries:
            for key, value in metadata[str(summary.file_path)].items():
                setattr(summary, key, value)
    if temp_pdf != pdf_output:
        shutil.rmtree(temp_pdf)
    return article_filter.filter(summaries)
