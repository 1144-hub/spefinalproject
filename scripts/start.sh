#!/bin/bash
set -e

echo "--- Starting Telecom RAG Startup Sequence ---"

# Check if ChromaDB exists and has data.
# 'chroma.sqlite3' is created by ChromaDB PersistentClient on first write.
DB_PATH="/app/chroma_db/chroma.sqlite3"

if [ ! -f "$DB_PATH" ] || [ "$FORCE_DB_REBUILD" = "true" ]; then
    if [ "$FORCE_DB_REBUILD" = "true" ]; then
        echo "🔄  FORCE_DB_REBUILD is set. Clearing existing database contents..."
        # Use find -mindepth 1 to safely delete only children, never '.' or '..'
        find /app/chroma_db -mindepth 1 -delete 2>/dev/null || true
    fi
    echo "⚠️  Vector Database not found or rebuild requested."
    echo "🛠️  Starting automatic data ingestion pipeline..."

    # Set PYTHONPATH so all src.* imports resolve correctly inside the container.
    export PYTHONPATH=/app

    # Run the real ingestion pipeline (DataPipeline → TelecomVectorStore).
    # This is NOT the test script — it builds the production ChromaDB.
    python3 -c "
import sys
sys.path.insert(0, '/app')
from src.data_engineering.pipeline import DataPipeline
from src.retrieval.vector_store import TelecomVectorStore

print('Loading and chunking SOP documents...')
pipeline = DataPipeline(data_dir='/app/data')
nodes = pipeline.run()

if not nodes:
    print('ERROR: No nodes produced. Check that /app/data contains SOP documents.')
    sys.exit(1)

print(f'Indexing {len(nodes)} chunks into ChromaDB...')
vs = TelecomVectorStore(db_path='/app/chroma_db')
vs.insert_nodes(nodes)
print('✅ Ingestion complete.')
"

    echo "✅ Data ingestion complete."
else
    echo "🚀 Vector Database found. Skipping ingestion."
fi

echo "🎯 Launching Streamlit Application..."

# Execute the streamlit app, replacing this shell process (exec = no zombie parent)
exec streamlit run src/app/main.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true
