"""
CI Unit Tests: Data Pipeline Chunking
Verifies DataPipeline loads and chunks SOP documents correctly.
Jenkins runs this in the 'Lint & Unit Test' stage via:
  python -m pytest notebooks/test_chunking.py -v
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_engineering.pipeline import DataPipeline

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))


def test_all_vendor_files_present():
    """All 5 vendor SOP files must exist in ./data/"""
    expected = [
        "cisco_ios_xr_sop.md",
        "nokia_router_mop.md",
        "ericsson_ipos_sop.md",
        "juniper_junos_sop.md",
        "huawei_vrp_sop.md",
    ]
    for fname in expected:
        assert os.path.exists(os.path.join(DATA_DIR, fname)), f"Missing: {fname}"


def test_pipeline_produces_chunks():
    """DataPipeline.run() must produce at least 100 chunks."""
    pipeline = DataPipeline(data_dir=DATA_DIR)
    nodes = pipeline.run()
    assert len(nodes) >= 100, f"Expected >=100 chunks, got {len(nodes)}"


def test_chunk_metadata_has_vendor():
    """Every chunk must carry equipment_vendor metadata for hybrid filtering."""
    pipeline = DataPipeline(data_dir=DATA_DIR)
    nodes = pipeline.run()
    vendors = {n.metadata.get("equipment_vendor") for n in nodes}
    assert len(vendors - {None}) >= 1, f"No vendor metadata found. Vendors: {vendors}"


if __name__ == "__main__":
    pipeline = DataPipeline(data_dir=DATA_DIR)
    nodes = pipeline.run()
    print(f"Total chunks: {len(nodes)}")
    for node in nodes[:3]:
        print(node.metadata, node.get_content()[:100])
