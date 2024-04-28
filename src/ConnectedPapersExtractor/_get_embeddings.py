from pathlib import Path
from typing import Optional, Callable

import numpy as np
import openai
from langchain_core.documents import Document
from openai.types import Embedding

from . import Config, PdfSummary


def _openai_embed(pages: list[str]) -> list[Embedding]:
    response = openai.embeddings.create(model="text-embedding-3-small", input=pages)
    return response.data


def _generate_embeddings(
    embeddings_path: Path,
    embeddings_shape_path: Path,
    docs: list[Document],
    embeddings_function: Optional[Callable[[list[str]], list[Embedding]]] = None,
):
    if embeddings_function is None:
        embeddings_function = _openai_embed
    embeddings = embeddings_function([doc.page_content for doc in docs])
    vectors = [embedding.embedding for embedding in embeddings]
    array = np.array(vectors)
    array = array.astype("float32")
    embeddings_path.write_bytes(array.tobytes())
    embeddings_shape_path.write_text(str(array.shape))
    return array


def _get_embeddings(
    summary: PdfSummary,
    embeddings_function: Optional[Callable[[list[str]], list[Embedding]]] = None,
    load_embeddings: bool = True,
) -> np.ndarray:
    embeddings_path = summary.file_path.with_suffix(Config.embedding_extension)
    embeddings_shape_path = summary.file_path.with_suffix(
        Config.embedding_shape_extension
    )
    if (
        not embeddings_path.exists()
        or not embeddings_shape_path.exists()
        or not load_embeddings
    ):
        array = _generate_embeddings(
            embeddings_path, embeddings_shape_path, summary.docs, embeddings_function
        )
    else:
        array = np.frombuffer(embeddings_path.read_bytes(), dtype=np.float32)
        array = array.reshape(eval(embeddings_shape_path.read_text()))
    return array
