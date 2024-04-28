import re
from typing import Union, Optional, Callable

from langchain.chains.llm import LLMChain
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import Runnable
from openai.types import Embedding
from tqdm import tqdm

from .conv2docs import conv2docs
from .PdfSummary import PdfSummaries
from .extract_main_parts import extract_main_parts


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
    map_template = """You will be passes parts of a scientific document one by one. 
    {docs}
    Based on this list of docs, please identify the main themes 
    Helpful Answer:"""
    map_prompt = PromptTemplate.from_template(map_template)
    map_chain = LLMChain(llm=llm, prompt=map_prompt)
