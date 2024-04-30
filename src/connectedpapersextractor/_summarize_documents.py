import json
import warnings
from dataclasses import asdict
from typing import Optional

from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.language_models import BaseLanguageModel
from langchain_text_splitters import TextSplitter
from tqdm import tqdm

from . import Config
from .MainPartsExtractor import MainPartsExtractor
from .PdfSummary import PdfSummaries
from ._add_docs import _add_docs
from ._huggingface_reduce import _huggingface_reduce
from ._refine_documents import _refine_documents, refine_prompt_template
from ._stuff_documents import _stuff_documents, stuff_prompt_template


def _summarize_documents(
    summaries: PdfSummaries,
    main_parts_extractor: MainPartsExtractor,
    llm: Optional[BaseLanguageModel] = None,
    text_splitter: Optional[TextSplitter] = None,
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
                text_summary = _stuff_documents(llm, docs)
            except Exception as e:
                warnings.warn(str(e))
                text_summary = _refine_documents(llm, docs)
        summary.text_summary = text_summary
        summary_as_dict = asdict(summary)
        summary_as_dict.pop("docs")
        metadata = json.loads(metadata_path.read_text())
        metadata[str(summary_as_dict.pop("file_path"))] = summary_as_dict
        metadata_path.write_text(json.dumps(metadata, indent=2))
    return summaries
