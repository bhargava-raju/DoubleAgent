"""Tool definitions and the tool executor for the first agent (Lesson 1.2).

A *tool* is a function the model may ask us to run. The model only ever sees the
name, description and JSON Schema below; our code decides whether and how to run it.
"""

import json  # noqa: F401  (you will need it)
from typing import Any

from anthropic.types import ToolParam

from doubleagent.erp import SupplierDirectory

LOOKUP_SUPPLIER = "lookup_supplier"

# TODO (1.2): describe the tool for the model.
#   - name: LOOKUP_SUPPLIER
#   - description: when to use it and what it returns (the model reads this, so be specific)
#   - input_schema: a JSON Schema object with one required string property, "query"
#     (a supplier name or id); set "additionalProperties": False
LOOKUP_SUPPLIER_TOOL: ToolParam = {
    "name": LOOKUP_SUPPLIER,
    "description": "TODO",
    "input_schema": {"type": "object", "properties": {}},
}

TOOLS: list[ToolParam] = [LOOKUP_SUPPLIER_TOOL]


class ToolError(Exception):
    """Raised for a bad tool call; the agent reports it back to the model instead of crashing."""


def execute_tool(name: str, tool_input: dict[str, Any], directory: SupplierDirectory) -> str:
    """Run the tool the model asked for and return its result as a JSON string.

    TODO (1.2):
      - for LOOKUP_SUPPLIER: read tool_input["query"], call directory.search(...) and return
        json.dumps of {"matches": [...]} where each match is `supplier.model_dump(mode="json")`
      - raise ToolError for an unknown tool name or a missing/non-string "query"
    """
    raise NotImplementedError
