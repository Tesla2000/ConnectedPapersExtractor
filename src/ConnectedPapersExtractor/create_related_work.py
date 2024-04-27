from typing import Union

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

from .PdfSummary import PdfSummaries
from ._extract_documents import _extract_documents


def create_related_work(summaries: PdfSummaries, llm: Union[
    Runnable[LanguageModelInput, str], Runnable[LanguageModelInput, BaseMessage]
]) -> str:
    documents = _extract_documents(summaries)
    # prompt_template = """Write a summary of the following pdfs:
    # "{text}"
    # SUMMARY:"""
    # prompt = PromptTemplate.from_template(prompt_template)
    # llm_chain = LLMChain(llm=llm, prompt=prompt)
    # chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    # result = chain.run(documents)
    # return result
    pass
