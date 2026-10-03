"""Read-only access to the sample ERP's supplier records (Lesson 1.2).

In Module 3 this becomes a real HTTP service; for now it reads a JSON file.
"""

import json
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

DEFAULT_SUPPLIERS_FILE = Path(__file__).resolve().parents[2] / "data" / "erp" / "suppliers.json"

SupplierStatus = Literal["active", "on_hold", "pending"]


class Supplier(BaseModel):
    id: str
    name: str
    country: str
    status: SupplierStatus
    categories: list[str]
    payment_terms_days: int
    contact_email: str
    last_updated: date


class SupplierDirectory:
    """An in-memory list of suppliers. (C#: a tiny read-only repository.)"""

    def __init__(self, suppliers: list[Supplier]) -> None:
        self._suppliers = suppliers

    @classmethod
    def from_json_file(cls, path: Path = DEFAULT_SUPPLIERS_FILE) -> "SupplierDirectory":
        raw = json.loads(path.read_text(encoding="utf-8"))
        return cls([Supplier.model_validate(item) for item in raw])

    def search(self, query: str) -> list[Supplier]:
        """Find suppliers by id or name.

        TODO (1.2):
          - an exact, case-insensitive match on `id` returns just that supplier
          - otherwise return every supplier whose name contains `query`, case-insensitively
          - a blank query returns an empty list
        """
        raise NotImplementedError
