# ConnectedPapersExtractor
A package for creating summaries based on https://www.connectedpapers.com/.

Installation:

`

    pip install ConnectedPapersExtractor
`

Code example:
`

    import os
    from pathlib import Path
    
    from src.ConnectedPapersExtractor import get_summaries, ArticleFilter, PdfSummaries
    from src.ConnectedPapersExtractor.create_related_work import create_related_work
    
    if __name__ == "__main__":
        class Filter(ArticleFilter):
            def filter(self, summaries: PdfSummaries) -> PdfSummaries:
                return list(summary for summary in summaries if summary.n_words < 10000)
    
    
        connected_papers_url = "https://www.connectedpapers.com/main/d1bb97ac84e81b10f3a60d7c634c6c0c26437072/Can-LLMs-be-Good-Financial-Advisors%3F%3A-An-Initial-Study-in-Personal-Decision-Making-for-Optimized-Outcomes/graph"
        summaries = get_summaries(
            connected_papers_url,
            pdf_output=Path("pdf_files"),
            article_filter=Filter(),
        )
    
        related_work = create_related_work(summaries, refine=False)
        print(related_work)
`