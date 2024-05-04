from . import ArticleFilter, PdfSummaries


class _BasicFilter(ArticleFilter):
    def filter(self, summaries: PdfSummaries) -> PdfSummaries:
        return summaries
