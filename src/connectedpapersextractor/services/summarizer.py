from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from injector import inject
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI

from src.connectedpapersextractor.article import Documents


@inject
class SummarizerService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def summarize(self, docs: Documents) -> str:
        pass


class DefaultSummarizerService(SummarizerService):
    def summarize(self, docs: Documents) -> str:
        llm = ChatOpenAI(temperature=0.4, model_name="gpt-4-turbo")
        chain = load_summarize_chain(llm)
        result = chain.run(docs)
        if isinstance(result, str):
            return result
        raise ValueError


default_text_splitter = DefaultSummarizerService()
