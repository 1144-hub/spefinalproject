"""
Cross-Encoder Reranker for NetRestore RAG Pipeline.

Uses a lightweight cross-encoder model (ms-marco-MiniLM-L-6-v2, ~80MB) to
rerank candidate documents after initial retrieval.  Cross-encoders process
(query, document) pairs jointly through a full transformer forward pass,
producing much more accurate relevance scores than bi-encoder cosine
similarity alone.

This reranker sits between the fusion retriever and the LLM generation step:
    Retrieve top-10 (vector + BM25) → Rerank → Take top-3 → Send to LLM
"""

from llama_index.core.schema import NodeWithScore


class TelecomReranker:
    """
    Wraps a sentence-transformers CrossEncoder for reranking retrieved nodes.
    Falls back gracefully to score-based ranking if the model fails to load
    (e.g., no internet on first run and no cached model).
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        try:
            from sentence_transformers import CrossEncoder
            self.model = CrossEncoder(model_name)
            self.available = True
            print(f"✅ Reranker loaded: {model_name}")
        except Exception as e:
            print(f"⚠️  Reranker model failed to load: {e}. Falling back to score-based ranking.")
            self.model = None
            self.available = False

    def rerank(
        self,
        query: str,
        nodes_with_scores: list[NodeWithScore],
        top_n: int = 3,
    ) -> list[NodeWithScore]:
        """
        Rerank a list of NodeWithScore using the cross-encoder.

        Args:
            query:              The user's search query.
            nodes_with_scores:  Candidate nodes from the fusion retriever.
            top_n:              Number of top results to return after reranking.

        Returns:
            Reranked list of NodeWithScore (length <= top_n).
        """
        if not self.available or not nodes_with_scores:
            return nodes_with_scores[:top_n]

        # Build (query, passage) pairs for the cross-encoder
        pairs = [(query, node.node.get_content()) for node in nodes_with_scores]
        scores = self.model.predict(pairs)

        # Pair each node with its reranker score, sort descending
        scored = list(zip(nodes_with_scores, scores))
        scored.sort(key=lambda x: x[1], reverse=True)

        result = []
        for node_with_score, rerank_score in scored[:top_n]:
            # Replace the original retrieval score with the reranker score
            node_with_score.score = float(rerank_score)
            result.append(node_with_score)

        return result
