from operator import attrgetter
from typing import Union, Optional

from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langchain_text_splitters import TextSplitter

from . import MainPartsExtractor
from .MainPartsExtractor import _DefaultExtractor
from .PdfSummary import PdfSummaries
from src.connectedpapersextractor.utils.combine_summaries import combine_summaries
from src.connectedpapersextractor.utils.summarize_documents import summarize_documents


def create_related_work(
    summaries: PdfSummaries,
    llm: Union[
        Runnable[LanguageModelInput, str],
        Optional[Runnable[LanguageModelInput, BaseMessage]],
    ] = None,
    text_splitter: Optional[TextSplitter] = None,
    main_parts_extractor: Optional[MainPartsExtractor] = None,
    refine: bool = True,
    custom_stuff_prompt_template: Optional[str] = None,
) -> str:
    if not summaries:
        raise ValueError("Summaries must be provided")
    if main_parts_extractor is None:
        main_parts_extractor = _DefaultExtractor()
    if llm is None:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    summaries_with_text = summarize_documents(
        summaries, main_parts_extractor, llm, text_splitter, custom_stuff_prompt_template
    )
    combined_summaries = "\n\n".join(
        map(": ".join, map(attrgetter("title", "text_summary"), summaries_with_text))
    )
    if refine and len(summaries) != 1:
        return combine_summaries(combined_summaries, llm)
    return combined_summaries
