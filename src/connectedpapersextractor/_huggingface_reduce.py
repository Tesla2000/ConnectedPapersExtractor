from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

from src.connectedpapersextractor._stuff_documents import stuff_prompt_template

reduce_prompt_template = """
    Write a 5-6 sentence long summary of the following:
    "{text}"
    SPECIFIC SUMMARY:
              """


def _huggingface_reduce(llm: HuggingFacePipeline, docs: list[Document]) -> str:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000 - llm.get_num_tokens(stuff_prompt_template.format(text="")),
        chunk_overlap=200,
        length_function=llm.get_num_tokens
    )
    docs = splitter.create_documents([' '.join(doc.page_content for doc in docs)])
    text_summaries = tuple(
        llm.invoke(stuff_prompt_template.format(text=doc.page_content)) for doc in tqdm(docs))
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000 - llm.get_num_tokens(reduce_prompt_template.format(text="")),
        chunk_overlap=200,
        length_function=llm.get_num_tokens
    )
    while len(text_summaries) > 1:
        text = " ".join(text_summaries)
        docs = splitter.create_documents([text])
        text_summaries = tuple(llm.invoke(reduce_prompt_template.format(text=doc.page_content)) for doc in docs)
    return text_summaries[0]
