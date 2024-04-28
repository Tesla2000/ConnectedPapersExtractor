import json
from dataclasses import asdict
from typing import Union, Optional
from warnings import warn

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from openai import BadRequestError

from . import Config
from .MainPartsExtractor import MainPartsExtractor
from .PdfSummary import PdfSummaries
from ._add_docs import _add_docs


def _summarize_documents_piecemeal(
    summaries: PdfSummaries,
    main_parts_extractor: MainPartsExtractor,
    llm: Union[
        Runnable[LanguageModelInput, str],
        Optional[Runnable[LanguageModelInput, BaseMessage]],
    ] = None,
    embeddings: Optional[Embeddings] = None,
) -> PdfSummaries:
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
    metadata_path = summaries[0].file_path.parent.joinpath(Config.metadate_file_name)
    for summary in summaries:
        if summary.text_summary is not None:
            continue
        _add_docs(summary, embeddings)
        docs = main_parts_extractor.extract(summary)
        try:
            text_summary = stuff_chain.run(docs)
        except BadRequestError as e:
            warn(e.message + "\nConsider changing  value of article_filter")
            text_summary = e.message + "\nConsider changing  value of article_filter"
        summary.text_summary = text_summary
        summary_as_dict = asdict(summary)
        summary_as_dict.pop("docs")
        metadata = json.loads(metadata_path.read_text())
        metadata[str(summary_as_dict.pop("file_path"))] = summary_as_dict
        metadata_path.write_text(json.dumps(metadata, indent=2))
    return summaries
