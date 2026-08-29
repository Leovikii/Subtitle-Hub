#!/usr/bin/env python3
"""Count declared entity forms in visible ASS Dialogue and block forbidden Chinese forms."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from audit_subtitle import AuditError, HAN, parse_events, visible


class TermAuditError(RuntimeError):
    pass


GROUPS = ("approved_forms", "forbidden_forms", "source_forms")


def load_terms(path: Path) -> list[dict[str, object]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as error:
        raise TermAuditError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise TermAuditError("term manifest must be an object with schema_version 1")
    terms = payload.get("terms")
    if not isinstance(terms, list) or not terms:
        raise TermAuditError("term manifest requires a nonempty terms array")

    term_ids: set[str] = set()
    owners: dict[tuple[str, str], str] = {}
    normalized: list[dict[str, object]] = []
    for index, raw in enumerate(terms, start=1):
        if not isinstance(raw, dict):
            raise TermAuditError(f"term {index} must be an object")
        term_id = raw.get("term_id")
        if not isinstance(term_id, str) or not term_id.strip():
            raise TermAuditError(f"term {index} requires a nonempty term_id")
        if term_id in term_ids:
            raise TermAuditError(f"duplicate term_id {term_id!r}")
        term_ids.add(term_id)

        item: dict[str, object] = {"term_id": term_id}
        for group in GROUPS:
            if group != "source_forms" and group not in raw:
                raise TermAuditError(f"{term_id} requires {group}")
            forms = raw.get(group, [])
            if not isinstance(forms, list) or any(not isinstance(form, str) or not form for form in forms):
                raise TermAuditError(f"{term_id}.{group} must be an array of nonempty strings")
            if len(forms) != len(set(forms)):
                raise TermAuditError(f"{term_id}.{group} contains duplicate forms")
            item[group] = forms
            namespace = "source" if group == "source_forms" else "chinese"
            for form in forms:
                key = (namespace, form)
                owner = owners.get(key)
                if owner:
                    raise TermAuditError(f"form {form!r} is assigned more than once: {owner} and {term_id}.{group}")
                owners[key] = f"{term_id}.{group}"
        if not item["approved_forms"]:
            raise TermAuditError(f"{term_id}.approved_forms must not be empty")
        normalized.append(item)
    return normalized


def occurrences(text: str, form: str) -> int:
    return text.count(form)


def audit_file(path: Path, terms: list[dict[str, object]]) -> dict[str, object]:
    events = parse_events(path.read_text(encoding="utf-8-sig"))
    result: list[dict[str, object]] = []
    for term in terms:
        groups: dict[str, list[dict[str, object]]] = {}
        for group in GROUPS:
            forms: list[dict[str, object]] = []
            for form in term[group]:
                hits = []
                for event in events:
                    clean = visible(event.text)
                    if group != "source_forms" and not HAN.search(clean):
                        continue
                    count = occurrences(clean, form)
                    if count:
                        hits.append({"event": event.index, "start_cs": event.start, "count": count})
                forms.append({"form": form, "count": sum(hit["count"] for hit in hits), "hits": hits})
            groups[group] = forms
        result.append({"term_id": term["term_id"], **groups})
    return {"file": str(path), "dialogue_events": len(events), "terms": result}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terms", required=True, type=Path, help="Disposable schema-1 JSON term manifest")
    parser.add_argument("files", nargs="+", type=Path, help="ASS masters to scan")
    parser.add_argument("--output", type=Path, help="Optional disposable JSON output; stdout is the default")
    args = parser.parse_args()
    try:
        terms = load_terms(args.terms.resolve())
        files = [audit_file(path.resolve(), terms) for path in args.files]
    except (AuditError, TermAuditError, OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    forbidden_hits = sum(
        form["count"]
        for file in files
        for term in file["terms"]
        for form in term["forbidden_forms"]
    )
    report = {
        "schema_version": 1,
        "files": files,
        "summary": {"forbidden_hits": forbidden_hits, "passed": forbidden_hits == 0},
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    if forbidden_hits:
        print(f"term audit failed: {forbidden_hits} forbidden occurrence(s)", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
