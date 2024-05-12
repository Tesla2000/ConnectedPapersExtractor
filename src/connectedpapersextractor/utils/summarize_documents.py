from __future__ import annotations

from ..services.convert_service import CovertService
from src.connectedpapersextractor import Config
from src.connectedpapersextractor.article import Articles


def add_summaries(articles: Articles, convert_service: CovertService) -> Articles:
    metadata_path = articles[0].file_path.parent.joinpath(Config.metadate_file_name)
    for article in articles:
        convert_service.add_summary(article, metadata_path)
    return articles
