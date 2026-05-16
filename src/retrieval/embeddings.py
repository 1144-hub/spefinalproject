from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def get_embedding_model():
    """
    Initializes and returns the BAAI/bge-m3 embedding model.
    This model runs locally and is open-source.
    """
    # Using a deeply optimized local embedding model to prevent RAM OOM crashes.
    # all-MiniLM-L6-v2 fits comfortably in < 200MB memory and prevents the freezing issue.
    embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")
    
    return embed_model
