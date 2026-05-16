"""
RAG Evaluation Script with Ground Truth Metrics.

Evaluates the NetRestore RAG pipeline against ground truth Q&A pairs
using both retrieval metrics and generation quality metrics.

Metrics computed:
  RETRIEVAL:
    - Hit Rate:    % of queries where the correct vendor doc was retrieved
    - Keyword Hit: % of expected keywords found in retrieved context
    - MRR:         Mean Reciprocal Rank of the first relevant result

  GENERATION (requires GROQ_API_KEY):
    - Answer Completeness:  Does the answer contain expected keywords?
    - Faithfulness Proxy:   Is the answer grounded in retrieved context?

Usage:
    python src/evaluation/evaluate.py
    python src/evaluation/evaluate.py --skip-llm   # retrieval metrics only
"""

import os
import sys
import json
import argparse
import time

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.retrieval.vector_store import TelecomVectorStore
from src.retrieval.hybrid_search import TelecomHybridRetriever
from src.llm.qa_engine import ProceduralQAEngine


def load_ground_truth(path: str) -> list[dict]:
    """Load evaluation Q&A pairs from JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def evaluate_retrieval(retriever: TelecomHybridRetriever, qa_pairs: list[dict]) -> dict:
    """
    Evaluate retrieval quality against ground truth.

    Returns:
        Dict with retrieval metrics.
    """
    total = len(qa_pairs)
    vendor_hits = 0
    keyword_hits = 0
    total_keywords = 0
    reciprocal_ranks = []

    print("\n" + "=" * 70)
    print("RETRIEVAL EVALUATION")
    print("=" * 70)

    for i, qa in enumerate(qa_pairs):
        query = qa["query"]
        expected_vendor = qa.get("expected_vendor")
        expected_keywords = qa.get("expected_keywords", [])

        # Build filters from expected values
        filters = {}
        if expected_vendor:
            filters["equipment_vendor"] = expected_vendor
        alarm_code = qa.get("expected_alarm_code")
        if alarm_code:
            filters["alarm_code"] = alarm_code

        # Retrieve
        results = retriever.search(query=query, filters=filters if filters else None)

        # --- Vendor Hit Rate ---
        vendor_found = False
        first_relevant_rank = None
        for rank, r in enumerate(results):
            doc_vendor = r.node.metadata.get("equipment_vendor", "")
            if expected_vendor and doc_vendor == expected_vendor:
                vendor_found = True
                if first_relevant_rank is None:
                    first_relevant_rank = rank + 1
                break

        if vendor_found or not expected_vendor:
            vendor_hits += 1

        # --- MRR ---
        if first_relevant_rank:
            reciprocal_ranks.append(1.0 / first_relevant_rank)
        else:
            reciprocal_ranks.append(0.0)

        # --- Keyword Hit Rate ---
        all_context = " ".join([r.node.get_content().lower() for r in results])
        for kw in expected_keywords:
            total_keywords += 1
            if kw.lower() in all_context:
                keyword_hits += 1

        # Print per-query result
        status = "✅" if vendor_found or not expected_vendor else "❌"
        kw_found = sum(1 for kw in expected_keywords if kw.lower() in all_context)
        print(f"  {status} Q{i+1}: '{query[:60]}...' "
              f"| Vendor: {'MATCH' if vendor_found else 'MISS'} "
              f"| Keywords: {kw_found}/{len(expected_keywords)} "
              f"| Results: {len(results)}")

    metrics = {
        "vendor_hit_rate": vendor_hits / total if total > 0 else 0,
        "keyword_hit_rate": keyword_hits / total_keywords if total_keywords > 0 else 0,
        "mrr": sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0,
        "total_queries": total,
    }

    print(f"\n{'─' * 50}")
    print(f"  Vendor Hit Rate:   {metrics['vendor_hit_rate']:.1%} ({vendor_hits}/{total})")
    print(f"  Keyword Hit Rate:  {metrics['keyword_hit_rate']:.1%} ({keyword_hits}/{total_keywords})")
    print(f"  MRR:               {metrics['mrr']:.3f}")
    print(f"{'─' * 50}")

    return metrics


def evaluate_generation(qa_engine: ProceduralQAEngine, qa_pairs: list[dict]) -> dict:
    """
    Evaluate generation quality using stateless queries.
    Checks answer completeness (keyword presence) and basic faithfulness.

    Returns:
        Dict with generation metrics.
    """
    total = len(qa_pairs)
    complete_answers = 0
    faithful_answers = 0
    total_latency = 0

    print("\n" + "=" * 70)
    print("GENERATION EVALUATION (using Groq LLM)")
    print("=" * 70)

    for i, qa in enumerate(qa_pairs):
        query = qa["query"]
        expected_keywords = qa.get("expected_keywords", [])
        expected_vendor = qa.get("expected_vendor")

        filters = {}
        if expected_vendor:
            filters["equipment_vendor"] = expected_vendor
        alarm_code = qa.get("expected_alarm_code")
        if alarm_code:
            filters["alarm_code"] = alarm_code

        try:
            start = time.time()
            response = qa_engine.query_stateless(query, filters=filters if filters else None)
            latency = time.time() - start
            total_latency += latency

            answer = str(response).lower()

            # --- Answer Completeness: does the answer contain expected keywords? ---
            kw_found = sum(1 for kw in expected_keywords if kw.lower() in answer)
            is_complete = kw_found >= len(expected_keywords) * 0.5  # at least 50% of keywords
            if is_complete:
                complete_answers += 1

            # --- Faithfulness Proxy: does the answer NOT contain "I cannot find" ---
            is_faithful = "i cannot find" not in answer and len(answer.strip()) > 50
            if is_faithful:
                faithful_answers += 1

            status = "✅" if is_complete and is_faithful else "⚠️"
            print(f"  {status} Q{i+1}: '{query[:50]}...' "
                  f"| Complete: {'Y' if is_complete else 'N'} "
                  f"| Faithful: {'Y' if is_faithful else 'N'} "
                  f"| Latency: {latency:.1f}s "
                  f"| Keywords: {kw_found}/{len(expected_keywords)}")

        except Exception as e:
            print(f"  ❌ Q{i+1}: '{query[:50]}...' | ERROR: {str(e)[:80]}")
            total_latency += 0

    metrics = {
        "answer_completeness": complete_answers / total if total > 0 else 0,
        "faithfulness_rate": faithful_answers / total if total > 0 else 0,
        "avg_latency_seconds": total_latency / total if total > 0 else 0,
        "total_queries": total,
    }

    print(f"\n{'─' * 50}")
    print(f"  Answer Completeness: {metrics['answer_completeness']:.1%} ({complete_answers}/{total})")
    print(f"  Faithfulness Rate:   {metrics['faithfulness_rate']:.1%} ({faithful_answers}/{total})")
    print(f"  Avg Latency:         {metrics['avg_latency_seconds']:.2f}s")
    print(f"{'─' * 50}")

    return metrics


def main():
    parser = argparse.ArgumentParser(description="Evaluate NetRestore RAG Pipeline")
    parser.add_argument("--skip-llm", action="store_true",
                        help="Skip LLM generation evaluation (retrieval metrics only)")
    args = parser.parse_args()

    # Paths
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    db_path = os.path.join(project_root, "chroma_db")
    qa_path = os.path.join(project_root, "data", "evaluation_qa.json")

    # Load ground truth
    if not os.path.exists(qa_path):
        print(f"❌ Ground truth file not found: {qa_path}")
        sys.exit(1)

    qa_pairs = load_ground_truth(qa_path)
    print(f"📋 Loaded {len(qa_pairs)} evaluation Q&A pairs")

    # Initialize retriever
    if not os.path.exists(db_path):
        print(f"❌ ChromaDB not found at {db_path}. Run test_retrieval.py first to ingest data.")
        sys.exit(1)

    vs_manager = TelecomVectorStore(db_path=db_path)
    retriever = TelecomHybridRetriever(vector_store_manager=vs_manager, similarity_top_k=10)

    # ── Retrieval Evaluation ──
    retrieval_metrics = evaluate_retrieval(retriever, qa_pairs)

    # ── Generation Evaluation ──
    generation_metrics = {}
    if not args.skip_llm:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("\n⚠️  GROQ_API_KEY not set. Skipping generation evaluation.")
            print("   Set it with: export GROQ_API_KEY=gsk_...")
        else:
            qa_engine = ProceduralQAEngine(retriever_pipeline=retriever)
            generation_metrics = evaluate_generation(qa_engine, qa_pairs)
    else:
        print("\n⏭️  Skipping LLM generation evaluation (--skip-llm flag)")

    # ── Summary ──
    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)
    print(f"\n  Retrieval Metrics:")
    print(f"    Vendor Hit Rate:   {retrieval_metrics['vendor_hit_rate']:.1%}")
    print(f"    Keyword Hit Rate:  {retrieval_metrics['keyword_hit_rate']:.1%}")
    print(f"    MRR:               {retrieval_metrics['mrr']:.3f}")

    if generation_metrics:
        print(f"\n  Generation Metrics:")
        print(f"    Answer Completeness: {generation_metrics['answer_completeness']:.1%}")
        print(f"    Faithfulness Rate:   {generation_metrics['faithfulness_rate']:.1%}")
        print(f"    Avg Latency:         {generation_metrics['avg_latency_seconds']:.2f}s")

    # Save results to JSON
    results_path = os.path.join(project_root, "evaluation_results.json")
    results = {
        "retrieval": retrieval_metrics,
        "generation": generation_metrics,
        "num_qa_pairs": len(qa_pairs),
    }
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Results saved to {results_path}")


if __name__ == "__main__":
    main()
