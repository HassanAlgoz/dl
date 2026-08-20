"""Helpers for the chunking lesson — expansion metadata, context expansion, and eval metrics."""

from __future__ import annotations

from collections import defaultdict

from langchain_core.documents import Document

# Keys populated by MarkdownHeaderTextSplitter (see LangChain docs).
HEADER_KEYS = ("h1", "h2", "h3")


def section_id(meta: dict) -> str:
    """Stable id for all chunks under the same markdown section."""
    parts = [meta["source"], *(meta[k] for k in HEADER_KEYS if meta.get(k))]
    return "::".join(parts)


def assign_expansion_metadata(chunks: list[Document]) -> list[Document]:
    """Add section_id, chunk_index, and chunk_count for context expansion."""
    counts: dict[str, int] = defaultdict(int)
    for chunk in chunks:
        sid = section_id(chunk.metadata)
        chunk.metadata["section_id"] = sid
        counts[sid] += 1

    index_in_section: dict[str, int] = defaultdict(int)
    section_index_in_file: dict[str, dict[str, int]] = defaultdict(dict)

    for chunk in chunks:
        sid = chunk.metadata["section_id"]
        source = chunk.metadata["source"]

        if sid not in section_index_in_file[source]:
            section_index_in_file[source][sid] = len(section_index_in_file[source])

        chunk.metadata["section_index"] = section_index_in_file[source][sid]
        chunk.metadata["chunk_index"] = index_in_section[sid]
        chunk.metadata["chunk_count"] = counts[sid]
        index_in_section[sid] += 1

    return chunks


def contextualize(chunk: Document) -> str:
    """Prepend header breadcrumb so embeddings retain document location.
    For example, if we end up with a chunk that is under an `h3` header,
    we can append at the top the path from the document's `h1` to this chunk.
    """
    path = " > ".join(chunk.metadata[k] for k in HEADER_KEYS if chunk.metadata.get(k))
    text = chunk.page_content
    return f"[{path}]\n\n{text}" if path else text


def to_chroma_records(chunks: list[Document]) -> tuple[list[str], list[str], list[dict]]:
    """Convert LangChain Documents to Chroma ids, texts, and metadata lists."""
    ids, documents, metadatas = [], [], []
    for chunk in chunks:
        source = chunk.metadata["source"]
        sec = chunk.metadata["section_index"]
        idx = chunk.metadata["chunk_index"]
        ids.append(f"{source}::s{sec:02d}::c{idx:02d}")
        documents.append(contextualize(chunk))
        metadatas.append(chunk.metadata)
    return ids, documents, metadatas


def expand_context(collection, meta: dict, window: int = 1):
    """Return neighboring chunks from the same section, ordered by chunk_index."""
    hits = collection.get(
        where={"section_id": meta["section_id"]},
        include=["documents", "metadatas"],
    )
    rows = sorted(
        zip(hits["ids"], hits["documents"], hits["metadatas"]),
        key=lambda row: row[2]["chunk_index"],
    )
    center = meta["chunk_index"]
    return rows[max(0, center - window) : center + window + 1]


def recall_at_k(results: list[str], expected: list[str], k: int) -> float:
    """Of your test queries, what percentage have the correct chunk in the top `k` results?"""
    return len(set(results[:k]) & set(expected)) / len(expected)


def mrr(results: list[str], expected: list[str]) -> float:
    """Where does the first correct chunk appear? (Higher is better)"""
    expected_set = set(expected)
    for rank, chunk_id in enumerate(results, start=1):
        if chunk_id in expected_set:
            return 1 / rank
    return 0.0
