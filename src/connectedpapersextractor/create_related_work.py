from operator import attrgetter
from typing import Union, Optional

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable

from . import MainPartsExtractor
from .MainPartsExtractor import _DefaultExtractor
from .PdfSummary import PdfSummaries
from ._combine_summaries import _combine_summaries
from ._summarize_documents import _summarize_documents


def create_related_work(
    summaries: PdfSummaries,
    llm: Union[
        Runnable[LanguageModelInput, str],
        Optional[Runnable[LanguageModelInput, BaseMessage]],
    ] = None,
    embeddings: Optional[Embeddings] = None,
    main_parts_extractor: Optional[MainPartsExtractor] = None,
    refine: bool = True,
) -> str:
    if not summaries:
        raise ValueError("Summaries must be provided")
    if main_parts_extractor is None:
        main_parts_extractor = _DefaultExtractor()
    if llm is None:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
        llm.max_tokens = 16385
    summaries_with_text = _summarize_documents(
        summaries, main_parts_extractor, llm, embeddings
    )
    combined_summaries = "\n\n".join(
        map(": ".join, map(attrgetter("title", "text_summary"), summaries_with_text))
    )
    if refine and len(summaries) != 1:
        return _combine_summaries(combined_summaries, llm)
    return combined_summaries
