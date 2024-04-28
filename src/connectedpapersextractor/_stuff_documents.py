from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate


def _stuff_documents(llm: BaseLanguageModel, docs: list[Document]
                     ) -> str:
    prompt = ChatPromptTemplate.from_template(
        """
    Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:
    """
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )
    return stuff_chain.invoke({"input_documents": docs})["text"]
