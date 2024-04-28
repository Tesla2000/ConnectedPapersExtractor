import re
from typing import Union, Optional, Callable

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from openai.types import Embedding
from tqdm import tqdm

from .conv2docs import conv2docs
from .PdfSummary import PdfSummaries
from .extract_relevant_docs import extract_relevant_docs


def summarize_documents(
    summaries: PdfSummaries,
    llm: Union[
        Runnable[LanguageModelInput, str],
        Optional[Runnable[LanguageModelInput, BaseMessage]],
    ] = None,
    embeddings: Optional[Embeddings] = None,
    embeddings_function: Optional[Callable[[list[str]], list[Embedding]]] = None,
    load_embeddings: bool = True,
) -> str:
    docs = conv2docs(summaries, embeddings)
    docs = extract_relevant_docs(summaries, docs, embeddings_function, load_embeddings)
    prompt = ChatPromptTemplate.from_template(
        """
    You will be given different passages from scientific articles one by one. 
    extract data that can be used to construct related work. Be specific about given output 
    if something is described provide a summary of the description. 
    If the passage don't provide useful information answer 'The passage does not provide useful information for constructing related work.'.
    Passage:
    ```{text}```
    SUMMARY:
    """
    )
    chain = prompt | llm | StrOutputParser()
    final_summary = ""

    for doc in tqdm(docs, desc="Processing documents"):
        new_summary = chain.invoke({"text": doc.page_content})
        final_summary += (
            new_summary.replace(
                "The passage does not provide useful information for constructing related work.",
                "",
            )
            + "\n"
        )
    return re.sub(r"\s+", " ", final_summary)
