import json

import pytest

from doubleagent.erp import SupplierDirectory
from doubleagent.tools import LOOKUP_SUPPLIER, LOOKUP_SUPPLIER_TOOL, ToolError, execute_tool


@pytest.fixture
def directory() -> SupplierDirectory:
    return SupplierDirectory.from_json_file()


def test_search_by_id_is_exact(directory: SupplierDirectory) -> None:
    assert [s.name for s in directory.search("sup-003")] == ["Umbrella Safety Supplies"]


def test_search_by_partial_name(directory: SupplierDirectory) -> None:
    assert {s.id for s in directory.search("globex")} == {"SUP-001", "SUP-005"}


def test_search_no_match_and_blank(directory: SupplierDirectory) -> None:
    assert directory.search("Wayne Enterprises") == []
    assert directory.search("   ") == []


def test_tool_definition_is_complete() -> None:
    assert LOOKUP_SUPPLIER_TOOL["name"] == LOOKUP_SUPPLIER
    assert LOOKUP_SUPPLIER_TOOL.get("description", "TODO") != "TODO"
    schema = LOOKUP_SUPPLIER_TOOL["input_schema"]
    assert schema["type"] == "object"
    assert schema["properties"]["query"]["type"] == "string"  # type: ignore[index]
    assert schema.get("required") == ["query"]
    assert schema.get("additionalProperties") is False


def test_execute_lookup_returns_json(directory: SupplierDirectory) -> None:
    result = json.loads(execute_tool(LOOKUP_SUPPLIER, {"query": "Initech"}, directory))
    assert result["matches"][0]["id"] == "SUP-002"
    assert result["matches"][0]["status"] == "on_hold"
    assert result["matches"][0]["last_updated"] == "2026-08-30"


def test_execute_unknown_tool_raises(directory: SupplierDirectory) -> None:
    with pytest.raises(ToolError):
        execute_tool("delete_everything", {}, directory)


def test_execute_bad_input_raises(directory: SupplierDirectory) -> None:
    with pytest.raises(ToolError):
        execute_tool(LOOKUP_SUPPLIER, {"name": "Initech"}, directory)
    with pytest.raises(ToolError):
        execute_tool(LOOKUP_SUPPLIER, {"query": 42}, directory)
