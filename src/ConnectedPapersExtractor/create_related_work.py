from typing import Union, Optional, Callable

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from openai.types import Embedding

from . import summarize_documents
from .PdfSummary import PdfSummaries


def create_related_work(
    summaries: PdfSummaries,
    llm: Union[
        Runnable[LanguageModelInput, str],
        Optional[Runnable[LanguageModelInput, BaseMessage]],
    ] = None,
    embeddings: Optional[Embeddings] = None,
    embeddings_function: Optional[Callable[[list[str]], list[Embedding]]] = None,
    load_embeddings: bool = True,
) -> str:
    if llm is None:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    concat_summaries = summarize_documents(
        summaries, llm, embeddings, embeddings_function, load_embeddings
    )
    prompt = ChatPromptTemplate.from_template(
        """
    You will be given different concatenated summaries of parts of scientific papers. 
    Your task is to convert these into a coherent related work.
    Passage:
    ```{text}```
    RELATED WORK:
    """
    )
    chain = prompt | llm | StrOutputParser()
    related_work = chain.invoke({"text": concat_summaries})
    return related_work
