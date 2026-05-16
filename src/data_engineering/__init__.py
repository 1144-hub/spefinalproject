"""
Data Engineering Module

This module handles the ingestion, parsing, chunking, and metadata extraction
of network Standard Operating Procedures (SOPs) for the NetRestore RAG system.

Components:
    - parser.py: Document loading from various formats (Markdown, PDF, JSON)
    - chunking.py: Structural chunking with header-aware splitting and metadata extraction
    - pipeline.py: End-to-end data processing pipeline orchestration
"""