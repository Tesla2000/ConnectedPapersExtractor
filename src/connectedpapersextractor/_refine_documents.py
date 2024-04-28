from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import PromptTemplate


def _refine_documents(llm: BaseLanguageModel, docs: list[Document]) -> str:
    question_prompt_template = """
    Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:
    """

    question_prompt = PromptTemplate(
        template=question_prompt_template, input_variables=["text"]
    )

    refine_prompt_template = """
                  Write a concise summary of the following summaries from scientific article. 
                  The summary should resemble a paragraph of related work.
                  ```{text}```
                  RELATED WORK SUMMARY:
                  """

    refine_prompt = PromptTemplate(
        template=refine_prompt_template, input_variables=["text"]
    )
    refine_chain = load_summarize_chain(
        llm,
        chain_type="refine",
        question_prompt=question_prompt,
        refine_prompt=refine_prompt,
    )
    return refine_chain({"input_documents": docs})['output_text']
