import json
from dataclasses import asdict
from typing import Optional

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLanguageModel

from . import Config
from .MainPartsExtractor import MainPartsExtractor
from .PdfSummary import PdfSummaries
from ._add_docs import _add_docs
from ._refine_documents import _refine_documents
from ._stuff_documents import _stuff_documents, stuff_prompt


def _summarize_documents(
    summaries: PdfSummaries,
    main_parts_extractor: MainPartsExtractor,
    llm: Optional[BaseLanguageModel] = None,
    embeddings: Optional[Embeddings] = None,
) -> PdfSummaries:
    metadata_path = summaries[0].file_path.parent.joinpath(Config.metadate_file_name)
    for summary in summaries:
        if summary.text_summary is not None:
            continue
        _add_docs(summary, embeddings)
        docs = main_parts_extractor.extract(summary)
        if llm.max_tokens is None:
            raise ValueError(f"{llm=} max_tokens argument is None.\nAssign integer value to llm.max_tokens=value")
        if llm.get_num_tokens(" ".join(doc.page_content for doc in docs) + stuff_prompt) < llm.max_tokens:
            max_tokens, llm.max_tokens = llm.max_tokens, None
            text_summary = _stuff_documents(llm, docs)
            llm.max_tokens = max_tokens
        else:
            text_summary = _refine_documents(llm, docs)
        summary.text_summary = text_summary
        summary_as_dict = asdict(summary)
        summary_as_dict.pop("docs")
        metadata = json.loads(metadata_path.read_text())
        metadata[str(summary_as_dict.pop("file_path"))] = summary_as_dict
        metadata_path.write_text(json.dumps(metadata, indent=2))
    return summaries
