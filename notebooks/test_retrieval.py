"""
Phase 2/3 Integration Test: Full Data Pipeline + Hybrid Retrieval

This script serves dual purposes:
  1. DATA INGESTION — Runs the full pipeline (load → chunk → embed → store in ChromaDB)
     Called by start.sh on first container boot.
  2. INTEGRATION TEST — Tests hybrid retrieval (BM25 + vector + reranking)
     with sample queries and vendor filters.

Usage:
    python notebooks/test_retrieval.py
"""
import sys
import os

# Add src to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_engineering.pipeline import DataPipeline
from src.retrieval.vector_store import TelecomVectorStore
from src.retrieval.hybrid_search import TelecomHybridRetriever


def main():
    print("--- Phase 2: Loading & Chunking Data ---")
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    pipeline = DataPipeline(data_dir=data_dir)
    nodes = pipeline.run()

    # Filter out empty nodes if any appeared due to formatting
    clean_nodes = [n for n in nodes if n.get_content().strip()]

    print("\n--- Phase 3: Initializing Vector Store ---")
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))

    # Clear previous testing DBs safely (avoiding mount point errors)
    if os.path.exists(db_path):
        print(f"Clearing contents of old DB at {db_path} for clean test...")
        for filename in os.listdir(db_path):
            file_path = os.path.join(db_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    vs_manager = TelecomVectorStore(db_path=db_path)

    # Embed and Insert Nodes into Chroma
    vs_manager.insert_nodes(clean_nodes)

    print("\n--- Phase 3: Testing Hybrid Search Retrieval (BM25 + Vector + Reranker) ---")
    retriever = TelecomHybridRetriever(vector_store_manager=vs_manager, similarity_top_k=10)

    queries = [
        {
            "prompt": "How do I fix optical Rx loss on my Nokia router?",
            "filters": {"equipment_vendor": "Nokia"},
        },
        {
            "prompt": "What is the procedure for BGP neighbor flapping on an Ericsson device?",
            "filters": {"equipment_vendor": "Ericsson"},
        },
        {
            "prompt": "How to resolve OSPF adjacency failure?",
            "filters": {"equipment_vendor": "Juniper"},
        },
        {
            "prompt": "Procedure to clear ALARM_CODE_404",
            "filters": {"equipment_vendor": "Nokia", "alarm_code": "404"},
        },
    ]

    for q in queries:
        print(f"\nQUERY: '{q['prompt']}' | FILTERS: {q['filters']}")
        results = retriever.search(query=q["prompt"], filters=q["filters"])

        if not results:
            print("  ⚠️  No results returned.")
            continue

        for i, node_with_score in enumerate(results):
            score = node_with_score.score
            node = node_with_score.node
            print(f"  -> Result {i+1} (Reranker Score: {score:.4f}):")
            print(f"     Title/Header: {node.metadata.get('header_path', 'No Header')}")
            preview = node.get_content()[:150].replace("\n", " ")
            print(f"     Content: {preview}...")
            print(f"     Metadata: {node.metadata}")

    print("\n✅ Phase 2/3 Integration Test Complete.")


if __name__ == "__main__":
    main()
