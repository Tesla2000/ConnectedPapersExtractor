from typing import Optional

from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import PromptTemplate

from src.connectedpapersextractor.utils.stuff_documents import stuff_prompt_template

refine_prompt_template = """
              Write a concise summary of the following summaries from scientific article. 
              The summary should resemble a paragraph of related work.
              ```{text}```
              RELATED WORK SUMMARY:
              """


def refine_documents(llm: BaseLanguageModel, docs: list[Document], custom_stuff_prompt_template: Optional[str] = None) -> str:
    if custom_stuff_prompt_template is None:
        custom_stuff_prompt_template = stuff_prompt_template
    question_prompt = PromptTemplate(
        template=custom_stuff_prompt_template, input_variables=["text"]
    )

    refine_prompt = PromptTemplate(
        template=refine_prompt_template, input_variables=["text"]
    )
    refine_chain = load_summarize_chain(
        llm,
        chain_type="refine",
        question_prompt=question_prompt,
        refine_prompt=refine_prompt,
    )
    return refine_chain.invoke({"input_documents": docs})['output_text']
