#!/bin/bash
set -e

echo "--- Setting up NetRestore Locally ---"

# Create and activate virtual environment
if [ -d "venv" ]; then
    echo "Removing broken python3.13 venv..."
    rm -rf venv
fi

echo "Creating virtual environment with python3.11..."
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null
# Install PyTorch first
pip install torch torchvision
pip install -r requirements.txt

export PYTHONPATH=$(pwd)

# Inject GROQ API Key from .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

DB_PATH="./chroma_db/chroma.sqlite3"
if [ ! -f "$DB_PATH" ]; then
    echo "⚠️  Vector Database not found."
    echo "🛠️  Starting automatic data ingestion pipeline..."

    python3.11 -c "
import sys
sys.path.insert(0, '.')
from src.data_engineering.pipeline import DataPipeline
from src.retrieval.vector_store import TelecomVectorStore

print('Loading and chunking SOP documents...')
pipeline = DataPipeline(data_dir='./data')
nodes = pipeline.run()

if not nodes:
    print('ERROR: No nodes produced. Check that ./data contains SOP documents.')
    sys.exit(1)

print(f'Indexing {len(nodes)} chunks into ChromaDB...')
vs = TelecomVectorStore(db_path='./chroma_db')
vs.insert_nodes(nodes)
print('✅ Ingestion complete.')
"
    echo "✅ Data ingestion complete."
else
    echo "🚀 Vector Database found. Skipping ingestion."
fi

echo "🎯 Launching Streamlit Application..."
export STREAMLIT_GATHER_USAGE_STATS=false
streamlit run src/app/main.py
