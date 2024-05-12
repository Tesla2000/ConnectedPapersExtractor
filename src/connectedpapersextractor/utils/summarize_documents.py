import json
import warnings
from dataclasses import asdict
from typing import Optional

from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.language_models import BaseLanguageModel
from langchain_text_splitters import TextSplitter

from src.connectedpapersextractor import Config
from src.connectedpapersextractor.MainPartsExtractor import MainPartsExtractor
from src.connectedpapersextractor.PdfSummary import PdfSummaries
from .add_docs import _add_docs
from .huggingface_reduce import _huggingface_reduce
from .refine_documents import _refine_documents
from .stuff_documents import _stuff_documents


def summarize_documents(
    summaries: PdfSummaries,
    main_parts_extractor: MainPartsExtractor,
    llm: Optional[BaseLanguageModel] = None,
    text_splitter: Optional[TextSplitter] = None,
    custom_stuff_prompt_template: Optional[str] = None,
) -> PdfSummaries:
    metadata_path = summaries[0].file_path.parent.joinpath(Config.metadate_file_name)
    for summary in summaries:
        if summary.text_summary is not None:
            continue
        _add_docs(summary, text_splitter)
        docs = main_parts_extractor.extract(summary)
        if isinstance(llm, HuggingFacePipeline):
            text_summary = _huggingface_reduce(llm, docs)
        else:
            try:
                text_summary = _stuff_documents(llm, docs, custom_stuff_prompt_template)
            except Exception as e:
                warnings.warn(str(e))
                text_summary = _refine_documents(llm, docs, custom_stuff_prompt_template)
        summary.text_summary = text_summary
        summary_as_dict = asdict(summary)
        summary_as_dict.pop("docs")
        metadata = json.loads(metadata_path.read_text())
        metadata[str(summary_as_dict.pop("file_path"))] = summary_as_dict
        metadata_path.write_text(json.dumps(metadata, indent=2))
    return summaries
