import os
import re
from typing import List, Dict, Any, Optional

from llama_index.core.schema import TextNode, BaseNode
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.extractors import BaseExtractor

class TelecomMetadataExtractor(BaseExtractor):
    """
    Custom metadata extractor that uses Regex to identify Alarm Codes 
    and Equipment Vendors from the document text.
    In a real-world scenario, this might use an LLM for complex extraction.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    async def aextract(self, nodes: List[BaseNode]) -> List[Dict[str, Any]]:
        """Extract metadata from nodes."""
        metadata_list = []
        for node in nodes:
            metadata = self._extract_metadata(node.get_content())
            metadata_list.append(metadata)
        return metadata_list
        
    def _extract_metadata(self, text: str) -> Dict[str, Any]:
        """Apply regex patterns to find specific telecom entities."""
        metadata = {}
        
        # Extract Alarm Code (e.g. ALARM_CODE_404, ALARM_501)
        alarm_match = re.search(r'ALARM(?:_CODE)?_(\d+)', text, re.IGNORECASE)
        if alarm_match:
            metadata["alarm_code"] = alarm_match.group(1)
            
        # Extract Vendor
        vendors = ["Cisco", "Nokia", "Juniper", "Ericsson", "Huawei"]
        vendor_found = False
        for vendor in vendors:
            if vendor.lower() in text.lower():
                metadata["equipment_vendor"] = vendor
                vendor_found = True
                break
        
        # If no vendor found in chunk, we don't set it (pipeline will propagate)
                
        # Extract Severity
        severity_match = re.search(r'Severity:\s*(Critical|Major|Minor|Warning)', text, re.IGNORECASE)
        if severity_match:
            metadata["severity"] = severity_match.group(1).title()
            
        return metadata


def get_procedural_chunker():
    """
    Returns a configured MarkdownNodeParser alongside the metadata extractor.
    The MarkdownNodeParser is excellent for Procedural QA because it chunks
    text by Header (e.g. ## Procedure X) rather than arbitrary strict token counts.
    This guarantees that Steps 1 to N under a procedure stay in the same node.
    """
    # Using LlamaIndex's built-in Markdown splitters for high-level structure
    parser = MarkdownNodeParser()
    return parser
