"""ChromaDB retrieval module compatible with DSPy's Retrieve API."""

from __future__ import annotations

import dspy
from dspy.primitives.prediction import Prediction

try:
    import chromadb
except ImportError as err:
    raise ImportError(
        "chromadb is required to use ChromadbRM. Install it with `pip install chromadb`.",
    ) from err


class ChromadbRM(dspy.Retrieve):
    """Retrieve top passages from a ChromaDB collection.

    Assumes the collection already exists and has been populated with document text.
    ChromadbRM does not perform ingestion — load documents in the notebook first.

    Args:
        collection_name: Name of the Chroma collection (must be a string, not a
            Collection object — see https://github.com/stanfordnlp/dspy/issues/469).
        persist_directory: Path for ``chromadb.PersistentClient``. Omit for in-memory.
        chromadb_client: Optional pre-built client. If omitted, one is created from
            ``persist_directory``.
        embedding_function: Chroma embedding function. ``None`` uses Chroma's default
            (local ``all-MiniLM-L6-v2``).
        k: Default number of passages to retrieve.

    Examples:
        ```python
        retriever = ChromadbRM(
            collection_name="ragqa_tech",
            persist_directory="./chroma_data",
            k=5,
        )
        dspy.configure(lm=lm, rm=retriever)

        passages = dspy.Retrieve(k=5)("what is high memory on linux?").passages
        ```

        ```python
        class RAG(dspy.Module):
            def __init__(self):
                self.retrieve = ChromadbRM("ragqa_tech", "./chroma_data", k=5)
        ```
    """

    def __init__(
        self,
        collection_name: str,
        persist_directory: str | None = None,
        chromadb_client: chromadb.ClientAPI | None = None,
        embedding_function=None,
        k: int = 3,
    ):
        if not isinstance(collection_name, str):
            raise TypeError(
                "collection_name must be a string (the collection name), "
                "not a chromadb Collection object. "
                "See https://github.com/stanfordnlp/dspy/issues/469"
            )

        self._collection_name = collection_name

        if chromadb_client is not None:
            self._client = chromadb_client
        elif persist_directory is not None:
            self._client = chromadb.PersistentClient(path=persist_directory)
        else:
            self._client = chromadb.Client()

        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function,
        )

        super().__init__(k=k)

    @property
    def collection(self):
        """Underlying Chroma collection (useful for ingestion in notebooks)."""
        return self._collection

    @property
    def client(self):
        return self._client

    def forward(
        self,
        query_or_queries: str | list[str],
        k: int | None = None,
        **kwargs,
    ) -> Prediction:
        """Search ChromaDB for the top-k passages matching the query."""
        k = k if k is not None else self.k
        queries = [query_or_queries] if isinstance(query_or_queries, str) else query_or_queries
        queries = [q for q in queries if q]

        passages: list[str] = []
        for query in queries:
            results = self._collection.query(
                query_texts=[query],
                n_results=k,
                **kwargs,
            )
            docs = results["documents"][0]

            for doc in docs:
                passages.append(doc)

        return Prediction(passages=passages)
