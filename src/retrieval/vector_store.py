import chromadb
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from src.retrieval.embeddings import get_embedding_model
import os

class TelecomVectorStore:
    """
    Manages the local ChromaDB vector store and index for processed network documents.
    """
    
    def __init__(self, db_path: str = "./chroma_db", collection_name: str = "telecom_sops"):
        self.db_path = db_path
        self.collection_name = collection_name
        self.embed_model = get_embedding_model()
        
        # Initialize ChromaDB client (local persistent directory)
        self.db = chromadb.PersistentClient(path=self.db_path)
        self.chroma_collection = self.db.get_or_create_collection(self.collection_name)
        
        # Setup LlamaIndex Vector Store
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        
        # Keep track if we have an active index loaded
        self.index = None

    def insert_nodes(self, nodes):
        """
        Takes LlamaIndex nodes (structural chunks) and indexes them into ChromaDB
        using the BAAI embedding model.
        """
        print(f"Indexing {len(nodes)} chunks into ChromaDB at {self.db_path}...")
        self.index = VectorStoreIndex(
            nodes, 
            storage_context=self.storage_context, 
            embed_model=self.embed_model
        )
        print("Indexing Complete.")
        
    def get_index(self):
        """
        Loads the existing index from the ChromaDB storage context if it wasn't
        just created via `insert_nodes`.
        """
        if not self.index:
            self.index = VectorStoreIndex.from_vector_store(
                self.vector_store,
                embed_model=self.embed_model
            )
        return self.index
