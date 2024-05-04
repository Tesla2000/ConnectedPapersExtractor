from typing import Optional

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate

stuff_prompt_template = """
    Write a concise summary of the following:
    ```{text}```
    CONCISE SUMMARY:
    """


def _stuff_documents(llm: BaseLanguageModel, docs: list[Document], custom_stuff_prompt_template: Optional[str] = None) -> str:
    if custom_stuff_prompt_template is None:
        custom_stuff_prompt_template = stuff_prompt_template
    prompt = ChatPromptTemplate.from_template(custom_stuff_prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )
    return stuff_chain.invoke({"input_documents": docs})['output_text']
