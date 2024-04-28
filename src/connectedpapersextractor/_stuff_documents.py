from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate

stuff_prompt = """
    Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:
    """


def _stuff_documents(llm: BaseLanguageModel, docs: list[Document]
                     ) -> str:
    prompt = ChatPromptTemplate.from_template(stuff_prompt)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )
    return stuff_chain.invoke({"input_documents": docs})['output_text']
