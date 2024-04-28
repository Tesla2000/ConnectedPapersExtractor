from operator import attrgetter
from typing import Union, Optional, Callable

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from openai.types import Embedding

from . import summarize_documents_piecemeal
from .PdfSummary import PdfSummaries
from ._combine_summaries import _combine_summaries


def create_related_work(
    summaries: PdfSummaries,
    llm: Union[
        Runnable[LanguageModelInput, str],
        Optional[Runnable[LanguageModelInput, BaseMessage]],
    ] = None,
    embeddings: Optional[Embeddings] = None,
    embeddings_function: Optional[Callable[[list[str]], list[Embedding]]] = None,
    load_embeddings: bool = True,
    refine: bool = True,
) -> str:
    if not summaries:
        raise ValueError("Summaries must be provided")
    if llm is None:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    summaries_with_text = summarize_documents_piecemeal(
        summaries, llm, embeddings, embeddings_function, load_embeddings
    )
    combined_summaries = "\n\n".join(map(": ".join, map(attrgetter("title", "text_summary"), summaries_with_text)))
    if refine and len(summaries) != 1:
        return _combine_summaries(summaries_with_text, llm)
    return combined_summaries
