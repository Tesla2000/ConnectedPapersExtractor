from typing import Union, Optional

from langchain.chains.llm import LLMChain
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

from src.ConnectedPapersExtractor import PdfSummaries


def combine_summaries(text_summaries: PdfSummaries, llm: Union[
        Runnable[LanguageModelInput, str],
        Optional[Runnable[LanguageModelInput, BaseMessage]],
    ]) -> str:
    if not text_summaries:
        raise ValueError("Text summaries must be provided")
    if len(text_summaries) == 1:
        return text_summaries[0].text_summary
    reduce_template = """The following is set of summaries of scientific article:
    {docs}
    Take these and distill it into a related work. 
    Helpful Answer:"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)
    related_work = reduce_chain.invoke({"docs": "\n".join(text_summaries)})
    return related_work["text"]
