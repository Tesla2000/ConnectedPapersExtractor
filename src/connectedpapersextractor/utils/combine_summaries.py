from typing import Union, Optional

from langchain.chains.llm import LLMChain
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable


def combine_summaries(
    combined_summaries: str,
    llm: Union[
        Runnable[LanguageModelInput, str],
        Optional[Runnable[LanguageModelInput, BaseMessage]],
    ],
) -> str:
    reduce_template = """The following is set of summaries of scientific article:\n
    {docs}
    Take these and distill it into a related work. 
    Helpful Answer:"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)
    related_work = reduce_chain.invoke({"docs": combined_summaries})
    return related_work["text"]
