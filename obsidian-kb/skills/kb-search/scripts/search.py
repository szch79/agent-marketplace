#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scikit-learn"]
# ///
"""Lightweight BM25+LSA hybrid search over a directory of documents.

Usage:
  search.py <corpus_dir> <query>          # query as argument
  echo "query" | search.py <corpus_dir>   # query from stdin
  search.py <corpus_dir> -                # explicit stdin

Options:
  -k, --limit N    Number of results (default: 5)
  --json           Output as JSON

Env:
  IR_CORPUS        Default corpus directory (overridden by positional arg)
  BM25_K1          BM25 term saturation (default: 1.2)
  BM25_B           BM25 length normalization (default: 0.75)
  LSA_DIMS         LSA/SVD dimensions (default: 30)
  RRF_K            RRF fusion constant (default: 60)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── corpus loading ──────────────────────────────────────────────────

EXTENSIONS = (".md", ".txt")


def load_docs(path: Path) -> tuple[list[str], list[str]]:
    """Read files from *path* (non-recursive). Returns (doc_ids, texts)."""
    ids, texts = [], []
    for f in sorted(path.iterdir()):
        if f.is_file() and f.suffix in EXTENSIONS:
            ids.append(f.name)
            texts.append(f.read_text(encoding="utf-8"))
    return ids, texts


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


# ── scorers ─────────────────────────────────────────────────────────


def bm25_scores(
    texts: list[str], query: str, k1: float = 1.2, b: float = 0.75
) -> np.ndarray:
    vec = CountVectorizer()
    tf = vec.fit_transform(texts)
    q = vec.transform([query])

    n = tf.shape[0]
    dl = tf.sum(axis=1).A1
    avgdl = dl.mean()
    df = np.diff(tf.tocsc().indptr)

    scores = np.zeros(n)
    for t in q.indices:
        idf = np.log((n - df[t] + 0.5) / (df[t] + 0.5) + 1.0)
        col = tf[:, t].toarray().flatten()
        tf_norm = col * (k1 + 1) / (col + k1 * (1 - b + b * dl / avgdl))
        scores += idf * tf_norm
    return scores


def lsa_scores(texts: list[str], query: str, n_components: int = 30) -> np.ndarray:
    vec = TfidfVectorizer()
    tfidf = vec.fit_transform(texts)
    svd = TruncatedSVD(n_components=n_components)
    reduced = svd.fit_transform(tfidf)

    norms = np.linalg.norm(reduced, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    reduced /= norms

    q_tfidf = vec.transform([query])
    q_reduced = svd.transform(q_tfidf)
    qn = np.linalg.norm(q_reduced)
    if qn > 0:
        q_reduced /= qn

    return cosine_similarity(q_reduced, reduced).flatten()


# ── fusion ──────────────────────────────────────────────────────────


def rrf(score_arrays: list[np.ndarray], k: int = 60) -> np.ndarray:
    """Reciprocal Rank Fusion over multiple score arrays."""
    n = score_arrays[0].shape[0]
    fused = np.zeros(n)
    for scores in score_arrays:
        ranks = np.argsort(-scores)
        for rank, idx in enumerate(ranks):
            fused[idx] += 1.0 / (k + rank + 1)
    return fused


# ── main ────────────────────────────────────────────────────────────


def search(
    corpus_dir: Path, query: str, limit: int = 5,
    bm25_k1: float = 1.2, bm25_b: float = 0.75,
    lsa_dims: int = 30, rrf_k: int = 60,
):
    doc_ids, raw_texts = load_docs(corpus_dir)
    if not doc_ids:
        return []
    texts = [normalise(t) for t in raw_texts]
    q = normalise(query)

    fused = rrf([
        bm25_scores(texts, q, k1=bm25_k1, b=bm25_b),
        lsa_scores(texts, q, n_components=lsa_dims),
    ], k=rrf_k)

    top = np.argsort(-fused)[:limit]
    return [
        {"doc_id": doc_ids[i], "score": round(float(fused[i]), 4)}
        for i in top
        if fused[i] > 0
    ]


def main():
    import os

    p = argparse.ArgumentParser(description="BM25+LSA hybrid search")
    p.add_argument("corpus", nargs="?", default=os.environ.get("IR_CORPUS"),
                    help="Corpus directory (or set $IR_CORPUS)")
    p.add_argument("query", nargs="?", default="-",
                    help="Query text, or '-' for stdin")
    p.add_argument("-k", "--limit", type=int, default=5)
    p.add_argument("--json", dest="as_json", action="store_true")
    p.add_argument("--bm25-k1", type=float, default=float(os.environ.get("BM25_K1", 1.2)))
    p.add_argument("--bm25-b", type=float, default=float(os.environ.get("BM25_B", 0.75)))
    p.add_argument("--lsa-dims", type=int, default=int(os.environ.get("LSA_DIMS", 30)))
    p.add_argument("--rrf-k", type=int, default=int(os.environ.get("RRF_K", 60)))
    args = p.parse_args()

    if not args.corpus:
        p.error("corpus directory required (positional arg or $IR_CORPUS)")
    corpus = Path(args.corpus).expanduser().resolve()
    if not corpus.is_dir():
        p.error(f"not a directory: {corpus}")

    query = sys.stdin.read().strip() if args.query == "-" else args.query

    results = search(corpus, query, limit=args.limit,
                     bm25_k1=args.bm25_k1, bm25_b=args.bm25_b,
                     lsa_dims=args.lsa_dims, rrf_k=args.rrf_k)

    if args.as_json:
        print(json.dumps(results, indent=2))
    else:
        for i, r in enumerate(results, 1):
            print(f"{i:3d}. [{r['doc_id']}] ({r['score']:.4f})")


if __name__ == "__main__":
    main()
