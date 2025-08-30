"""Utility functions for exporting query results to CSV / JSON.

They accept sequences of rows (tuples, lists, dicts). Optionally you can
pass column headers so JSON becomes a list of objects instead of arrays.
Non JSON-serializable types (date, Decimal, etc.) are converted to strings.
"""
import csv
import json
from datetime import date, datetime
from decimal import Decimal
from typing import Iterable, Sequence, Any, Optional, List

def _coerce_cell(val: Any):
	if isinstance(val, (date, datetime)):
		return val.isoformat()
	if isinstance(val, Decimal):
		return float(val)
	return val

def _normalize_rows(data: Sequence, headers: Optional[Sequence[str]] = None):
	if not data:
		return []
	first = data[0]
	# If already dicts, just coerce cell values
	if isinstance(first, dict):
		return [ {k: _coerce_cell(v) for k,v in row.items()} for row in data ]
	# If tuples/lists and headers provided and length matches
	if headers and isinstance(first, (tuple, list)) and len(headers)==len(first):
		out = []
		for row in data:
			out.append({h: _coerce_cell(v) for h,v in zip(headers, row)})
		return out
	# Fallback: list of lists
	return [ [_coerce_cell(c) for c in row] for row in data ]

def export_to_csv(data: Sequence, filename: str, headers: Optional[Sequence[str]] = None):
	rows = data
	with open(filename, 'w', newline='', encoding='utf-8') as f:
		writer = csv.writer(f)
		if headers:
			writer.writerow(headers)
		for row in rows:
			if isinstance(row, dict):
				if not headers:
					headers = list(row.keys())
					f.seek(0)
					writer.writerow(headers)
				writer.writerow([row.get(h, "") for h in headers])
			else:
				writer.writerow(list(row))

def export_to_json(data: Sequence, filename: str, headers: Optional[Sequence[str]] = None):
	normalized = _normalize_rows(data, headers)
	with open(filename, 'w', encoding='utf-8') as f:
		json.dump(normalized, f, ensure_ascii=False, indent=2)
