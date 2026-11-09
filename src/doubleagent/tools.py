"""Tool definitions and the tool executor for the first agent (Lesson 1.2).

A *tool* is a function the model may ask us to run. The model only ever sees the
name, description and JSON Schema below; our code decides whether and how to run it.
"""

import json
from typing import Any

from anthropic.types import ToolParam

from doubleagent.erp import SupplierDirectory

LOOKUP_SUPPLIER = "lookup_supplier"

# The model chooses tools from the name and description alone, so write them for the model.
# `ToolParam` is a TypedDict: a dict literal with a checked shape.
LOOKUP_SUPPLIER_TOOL: ToolParam = {
    "name": LOOKUP_SUPPLIER,
    "description": (
        "Look up Acme Industrial suppliers in the ERP by supplier id (e.g. 'SUP-001') or by "
        "full or partial company name (e.g. 'Globex'). Returns every matching supplier with "
        "id, name, country, status (active, on_hold or pending), categories, payment terms "
        "in days, contact email and last-updated date. Returns an empty list if nothing "
        "matches. Use it before answering any question about a specific supplier."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "A supplier id or (part of) a name."}
        },
        "required": ["query"],
        "additionalProperties": False,
    },
}

TOOLS: list[ToolParam] = [LOOKUP_SUPPLIER_TOOL]


class ToolError(Exception):
    """Raised for a bad tool call; the agent reports it back to the model instead of crashing."""


def execute_tool(name: str, tool_input: dict[str, Any], directory: SupplierDirectory) -> str:
    """Run the tool the model asked for and return its result as a JSON string.

    Tool input is untrusted JSON from the model, so validate it before use.
    """
    # Allow-list of tool names (C#: a switch with a default that throws).
    if name != LOOKUP_SUPPLIER:
        raise ToolError(f"Unknown tool: {name}")
    query = tool_input.get("query")
    # isinstance(x, str) is C#'s `x is string`.
    if not isinstance(query, str):
        raise ToolError("lookup_supplier needs a string 'query'")
    matches = directory.search(query)
    # model_dump(mode="json") makes JSON-safe dicts (dates become ISO strings).
    return json.dumps({"matches": [s.model_dump(mode="json") for s in matches]})
