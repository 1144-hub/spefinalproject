"""
Procedural QA Engine with Topology-Aware Reasoning and Query Routing.

This is the central orchestration class that ties together:
  - Hybrid retrieval (BM25 + vector + reranker)
  - Network topology injection (cascade analysis)
  - Query routing (in-scope vs out-of-scope)
  - Chat memory (conversational continuity)
  - LLM generation with chain-of-thought reasoning
"""

import os
import json
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.schema import NodeWithScore, TextNode
from src.llm.generator import get_llm_generator
from src.llm.prompts import (
    SYSTEM_PROMPT,
    TOPOLOGY_CONTEXT_TEMPLATE,
    OUT_OF_SCOPE_RESPONSE,
    procedural_qa_prompt,
    legacy_procedural_qa_prompt,
)


# ---------------------------------------------------------------------------
# Keywords for query routing (keyword-based, zero resource cost)
# ---------------------------------------------------------------------------
TELECOM_KEYWORDS = [
    # Alarm & procedure terms
    "alarm", "alarm_code", "procedure", "clear", "restore", "troubleshoot",
    "outage", "fault", "sop", "mop", "incident", "escalat",
    # Protocol terms
    "bgp", "ospf", "is-is", "isis", "mpls", "ldp", "rsvp", "bfd",
    "vrrp", "hsrp", "lacp", "stp", "vpls", "evpn", "pim", "igmp",
    "oam", "ipsec", "gre",
    # Equipment terms
    "router", "switch", "interface", "port", "sfp", "optic",
    "line card", "npu", "psu", "fan tray",
    # Vendor terms
    "nokia", "cisco", "juniper", "ericsson", "huawei",
    # Metric/status terms
    "down", "flapping", "timeout", "degraded", "unreachable", "failure",
]


class ProceduralQAEngine:
    """
    Ties together the Hybrid Retriever, Chat Memory, Network Topology,
    and the LLM into a cohesive conversational QA pipeline with
    chain-of-thought reasoning and query routing.

    Supports two modes:
    - Conversational (default): Uses ContextChatEngine with ChatMemoryBuffer for
      multi-turn chat with CoT reasoning. Follow-up questions are contextual.
    - Legacy/stateless: Falls back to RetrieverQueryEngine for single-shot QA
      (used by test scripts).
    """

    def __init__(self, retriever_pipeline, token_limit: int = 3072):
        """
        Expects an instance of TelecomHybridRetriever from Phase 3.

        Args:
            retriever_pipeline: TelecomHybridRetriever instance
            token_limit: Maximum tokens for the chat memory sliding window.
                         3072 is conservative for Llama-3.1-8B's 8K context window.
        """
        self.retriever = retriever_pipeline
        self.llm = get_llm_generator()
        self.token_limit = token_limit
        # Chat memory will be managed per-session (set externally by Streamlit)
        self.memory = None

        # Load network topology for cascade-aware reasoning
        self.topology = self._load_topology()

    def _load_topology(self) -> dict:
        """
        Load the network topology JSON file for cascade failure analysis.
        Returns an empty dict if the file doesn't exist.
        """
        topology_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "network_topology.json")
        )
        if os.path.exists(topology_path):
            with open(topology_path, "r") as f:
                data = json.load(f)
            print(f"✅ Network topology loaded: {len(data.get('network_topology', {}).get('nodes', []))} nodes")
            return data.get("network_topology", {})
        else:
            print("⚠️  network_topology.json not found. Topology-aware reasoning disabled.")
            return {}

    def _get_topology_context(self, query: str, filters: dict = None) -> str:
        """
        Build a topology context string for the given query.

        Identifies the relevant vendor from filters or query text, finds the
        corresponding network node(s), and formats the topology + cascade rules
        for injection into the LLM prompt.
        """
        if not self.topology:
            return ""

        # Determine vendor from filters or query
        vendor = None
        if filters and "equipment_vendor" in filters:
            vendor = filters["equipment_vendor"]
        else:
            for v in ["Nokia", "Cisco", "Juniper", "Ericsson", "Huawei"]:
                if v.lower() in query.lower():
                    vendor = v
                    break

        if not vendor:
            return ""

        # Find topology nodes for this vendor
        nodes = self.topology.get("nodes", [])
        relevant = [n for n in nodes if n.get("vendor") == vendor]
        if not relevant:
            return ""

        # Build context string
        parts = [f"Affected Vendor: {vendor}"]
        for node in relevant:
            role = node.get("role", "Unknown")
            connected = ", ".join(node.get("connected_to", []))
            parts.append(f"  • Node: {node['node_id']} | Role: {role} | Connected to: {connected}")

        # Add cascade rules
        rules = self.topology.get("rules", [])
        if rules:
            parts.append("\nCascade Failure Rules:")
            for rule in rules:
                parts.append(f"  • {rule}")

        return "\n".join(parts)

    def _classify_query(self, query: str, has_memory: bool = False) -> str:
        """
        Keyword-based query routing. Zero resource cost.
        Includes a 'conversational fallback': if memory exists, be more lenient.

        Returns:
            'telecom'  — query is about telecom alarms/SOPs/equipment
            'general'  — query is out-of-scope
        """
        query_lower = query.lower()

        # Conversational fallback: If this is a follow-up, treat it as telecom
        # (e.g. "and then?", "more details?", "further steps?")
        if has_memory:
            return "telecom"

        # Check if any telecom keyword appears in the query
        for keyword in TELECOM_KEYWORDS:
            if keyword in query_lower:
                return "telecom"

        # Also match ALARM_CODE_XXX patterns
        if "alarm" in query_lower or "code" in query_lower:
            return "telecom"

        return "general"

    def set_memory(self, memory: ChatMemoryBuffer):
        """
        Allow external code (e.g. Streamlit session state) to inject a
        session-specific ChatMemoryBuffer for conversational continuity.
        """
        self.memory = memory

    def query(self, query_str: str, filters: dict = None):
        """
        Conversational query with chain-of-thought + persistent memory
        + topology awareness + query routing.

        The ContextChatEngine is reused across calls (stored as self._chat_engine)
        so that ChatMemoryBuffer genuinely accumulates all previous turns.
        It is only rebuilt when the filters change (new vendor/alarm selection).

        Returns a response object with .response (text) and .source_nodes (citations).
        """
        # ── Query Routing ──
        # Check if we have active conversational context to bypass strict filtering
        has_memory = self.memory is not None and len(self.memory.get_all()) > 0
        query_type = self._classify_query(query_str, has_memory=has_memory)
        
        if query_type == "general":
            # Return a polite out-of-scope response without wasting retrieval/LLM resources
            return _OutOfScopeResponse(OUT_OF_SCOPE_RESPONSE)

        # ── Build topology context ──
        topology_ctx = self._get_topology_context(query_str, filters)
        topology_suffix = ""
        if topology_ctx:
            topology_suffix = TOPOLOGY_CONTEXT_TEMPLATE.format(topology_context=topology_ctx)

        # Full system prompt = base CoT prompt + topology context
        full_system_prompt = SYSTEM_PROMPT + topology_suffix

        # Only rebuild the chat engine when filters change, preserving memory otherwise
        filters_key = str(sorted(filters.items())) if filters else "none"
        if not hasattr(self, '_chat_engine') or self._filters_key != filters_key:
            self._filters_key = filters_key
            base_retriever = self.retriever.get_retriever(filters)

            # Use injected session memory, or create a fresh one for single calls
            memory = self.memory or ChatMemoryBuffer.from_defaults(
                token_limit=self.token_limit
            )

            self._chat_engine = ContextChatEngine.from_defaults(
                retriever=base_retriever,
                llm=self.llm,
                memory=memory,
                system_prompt=full_system_prompt,
                context_template=(
                    "Here are the relevant SOP documents retrieved for this query:\n"
                    "---------------------\n"
                    "{context_str}\n"
                    "---------------------\n"
                ),
            )
        else:
            # Filters unchanged — update system prompt for topology freshness
            # (topology context may change based on query content even with same filters)
            self._chat_engine._prefix_messages[0].content = full_system_prompt

        response = self._chat_engine.chat(query_str)
        return response

    def query_stateless(self, query_str: str, filters: dict = None):
        """
        Legacy stateless query (no memory, no CoT).
        Used by test scripts and evaluation notebooks for deterministic results.
        """
        base_retriever = self.retriever.get_retriever(filters)

        engine = RetrieverQueryEngine.from_args(
            retriever=base_retriever,
            llm=self.llm,
            text_qa_template=legacy_procedural_qa_prompt
        )

        response = engine.query(query_str)
        return response


class _OutOfScopeResponse:
    """
    Lightweight response object for out-of-scope queries.
    Mimics the LlamaIndex response interface so main.py doesn't break.
    """

    def __init__(self, message: str):
        self.response = message
        self.source_nodes = []

    def __str__(self):
        return self.response
