import os
from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import Document

class TelecomDocumentParser:
    """
    Handles reading multiple formats of SOPs and returning a consistent format
    for downstream chunking.
    """
    
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        
    def load_documents(self) -> list[Document]:
        """Load Markdown, JSON, and PDFs from the data directory."""
        if not os.path.exists(self.data_dir):
            print(f"Directory {self.data_dir} not found.")
            return []
            
        print(f"Loading documents from {self.data_dir}...")
        
        # Setup advanced parser (LlamaParse) if API key is present, otherwise fallback to standard PyPDF
        file_extractor = {}
        llama_api_key = os.environ.get("LLAMA_CLOUD_API_KEY")
        if llama_api_key:
            try:
                from llama_parse import LlamaParse
                print("LlamaParse API Key found. Using LlamaParse for complex PDFs.")
                file_extractor[".pdf"] = LlamaParse(result_type="markdown")
            except ImportError:
                print("llama_parse not installed. Falling back to default PyPDF.")
        else:
            print("No LLAMA_CLOUD_API_KEY found. Using standard PyPDF for PDF parsing.")

        reader = SimpleDirectoryReader(
            input_dir=self.data_dir,
            recursive=True,
            required_exts=['.md', '.pdf', '.json'],
            file_extractor=file_extractor if file_extractor else None
        )
        documents = reader.load_data()
        print(f"Successfully loaded {len(documents)} document pages/files.")
        return documents
