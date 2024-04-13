# ConnectedPapersExtractor
A package for creating summaries based on https://www.connectedpapers.com/.

Installation:

`

    pip install ConnectedPapersExtractor
`

Code example:
`

    from pathlib import Path
    from langchain.chains.summarize import load_summarize_chain
    from langchain_openai import ChatOpenAI
    
    from ConnectedPapersExtractor import get_summaries, ArticleFilter, PdfSummary
    
    if __name__ == "__main__":
    
        class Filter(ArticleFilter):
            def filter(self, summaries: list[PdfSummary]) -> list[PdfSummary]:
                return list(summary for summary in summaries if summary.citations > 80)
    
        connected_papers_url = "https://www.connectedpapers.com/main/5ed5723980bd28c3626182644ca837cc3ca30b07/Adaptive-Genomic-Evolution-of-Neural-Network-Topologies-(AGENT)-for-State%20to%20Action-Mapping-in-Autonomous-Agents/graph"
        llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo-1106",
            api_key=Path("api_token").read_text().strip(),
        )
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        article_filter = Filter()
        summaries = get_summaries(
            connected_papers_url=connected_papers_url,
            chain=chain,
            article_filter=article_filter,
            pdf_output=Path("pdf_files"),
        )
        print("\n".join(summary.text for summary in summaries))
`