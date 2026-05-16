"""
ChromaDB Inspection Script for NetRestore

This utility script provides a quick inspection of the ChromaDB vector store
to verify document ingestion, examine metadata, and preview content samples.

Usage:
    python scratch/inspect_db.py

Note: This is a development/debugging tool and should not be used in production.
"""

import chromadb
import os

# Database path configuration
db_path = "/Users/swarnendusekhardas/SSD_Files/Workspace/SPE Major Project/chroma_db"

# Check if the database exists
if not os.path.exists(db_path):
    print("❌ ChromaDB not found at the specified path.")
    print(f"   Path: {db_path}")
    print("   Please run the data ingestion pipeline first.")
else:
    # Initialize ChromaDB persistent client
    client = chromadb.PersistentClient(path=db_path)
    
    # Access the telecom SOPs collection
    collection = client.get_collection("telecom_sops")
    
    # Retrieve a sample of documents with their metadata
    results = collection.get(limit=10)
    
    print(f"📊 NetRestore ChromaDB Inspection Results")
    print(f"   Collection: telecom_sops")
    print(f"   Sample Size: {len(results['ids'])} documents")
    print(f"{'=' * 60}")
    
    # Display document information
    for i in range(len(results['ids'])):
        print(f"\n📄 Document {i + 1}:")
        print(f"   ID: {results['ids'][i]}")
        print(f"   Metadata: {results['metadatas'][i]}")
        print(f"   Content Preview: {results['documents'][i][:100]}...")
        print(f"{'─' * 60}")
