import json
from dataclasses import asdict
from typing import Union, Optional, Callable

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from openai.types import Embedding

from . import Config
from .PdfSummary import PdfSummaries
from .conv2docs import conv2docs


def summarize_documents_piecemeal(
    summaries: PdfSummaries,
    llm: Union[
        Runnable[LanguageModelInput, str],
        Optional[Runnable[LanguageModelInput, BaseMessage]],
    ] = None,
    embeddings: Optional[Embeddings] = None,
    embeddings_function: Optional[Callable[[list[str]], list[Embedding]]] = None,
    load_embeddings: bool = True,
) -> PdfSummaries:
    prompt = ChatPromptTemplate.from_template(
    """
    Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:
    """
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    summaries = conv2docs(summaries, embeddings)
    metadata_path = summaries[0].file_path.parent.joinpath(Config.metadate_file_name)
    for summary in summaries:
        if summary.text_summary is not None:
            continue
        # docs = extract_main_parts(summary, embeddings_function, load_embeddings)
        docs = summary.docs
        text_summary = stuff_chain.run(docs)
        summary.text_summary = text_summary
        summary_as_dict = asdict(summary)
        summary_as_dict.pop("docs")
        metadata = json.loads(metadata_path.read_text())
        metadata[str(summary_as_dict.pop("file_path"))] = summary_as_dict
        metadata_path.write_text(json.dumps(metadata, indent=2))
    return summaries
