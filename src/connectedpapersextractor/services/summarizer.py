from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI

from src.connectedpapersextractor.article import Documents


class SummarizerService(ABC):
    @abstractmethod
    def summarize(self, docs: Documents) -> str:
        pass


class DefaultSummarizerService(SummarizerService):
    def summarize(self, docs: Documents) -> str:
        llm = ChatOpenAI(temperature=0.5, model_name="gpt-4-turbo")
        chain = load_summarize_chain(llm)
        result = chain.run(docs)
        if isinstance(result, str):
            return result
        raise ValueError


default_text_splitter = DefaultSummarizerService()
