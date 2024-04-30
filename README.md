# ConnectedPapersExtractor
A package for creating summaries based on https://www.connectedpapers.com/.

Installation:

`

    pip install ConnectedPapersExtractor
`

Code example:
`

    from pathlib import Path
    
    from src.connectedpapersextractor import get_summaries, ArticleFilter, PdfSummaries
    from src.connectedpapersextractor.create_related_work import create_related_work
    
    if __name__ == "__main__":
        class Filter(ArticleFilter):
            def filter(self, summaries: PdfSummaries) -> PdfSummaries:
                return list(summary for summary in summaries if summary.n_words < 9500)
    
    
        connected_papers_url = "https://www.connectedpapers.com/main/9dac589a9ee616acc17b75e4cad546f94ce6777d/Evolutionary%20Based-Neural-Architecture-Search-for-an-Efficient-CAES-and-PV-Farm-Joint-Operation-Strategy-Using-Deep-Reinforcement-Learning/graph"
        summaries = get_summaries(
            connected_papers_url,
            pdf_output=Path("evolutionary_rl"),
            article_filter=Filter(),
        )
    
        related_work = create_related_work(summaries, refine=False)
        print(related_work)
`