from pathlib import Path
from typing import Union

import arxiv

from src.connectedpapersextractor import PdfSummaries, PdfSummary
from src.connectedpapersextractor.utils.download_summaries import _download_summaries


def download_summaries_from_arxiv(
    search: arxiv.Search,
    dir_path: Union[str, Path] = Path("/"),
) -> PdfSummaries:
    client = arxiv.Client()
    results = client.results(search)
    summaries = list(PdfSummary(
            file_path=dir_path.joinpath(article.entry_id.rpartition('/')[-1]).with_suffix('.pdf'),
            download_link=article.pdf_url,
            year=article.published.year,
            title=article.title,
        ) for article in results)
    _download_summaries(summaries, dir_path)
    return summaries
