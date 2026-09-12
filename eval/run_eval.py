#!/usr/bin/env python3
"""Golden-corpus harness for AUDIT.md.

Validates every case under eval/cases/ against its expected.json. Model
invocation is pluggable: this script never calls a model API directly and
ships no credentials. Point --model-call at a Python callable to run cases
live; omit it to run structure-only (the default), which validates fixture
and expected.json shape without asking a model anything.

Usage:
    python eval/run_eval.py
    python eval/run_eval.py --model-call mymodule:call_model
    python eval/run_eval.py --case keyboard-inaccessible-modal-pr --model-call mymodule:call_model

A --model-call target is a callable with the signature:
    call_model(system_prompt: str, mode: str, case_text: str) -> str
returning the model's raw text response (the human-readable report,
including its final VERDICT:/RISK:/CONFORMANCE: line and, where AUDIT.md
section 6 requires it, the VERDICT_JSON companion block).
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIT_PATH = REPO_ROOT / "AUDIT.md"
CASES_DIR = Path(__file__).resolve().parent / "cases"

VALID_MODES = {"PR", "File", "Piece", "Wholesale", "Data-map"}
CASE_INPUT_NAMES = (
    "diff.patch",
    "input.py",
    "input.ts",
    "input.tsx",
    "input.js",
    "input.sql",
    "input.json",
    "input.yaml",
    "input.tf",
    "input.html",
    "input.md",
    "input.txt",
    "input.sh",
    "datamap.md",
    "ropa.json",
    "notice.md",
)

DECLARED_SCOPE_PREFIX = "DECLARED_SCOPE:"
UNDECLARED = "undeclared"
DISCLAIMER_PREFIX = "NOT LEGAL ADVICE:"
VALID_REGIME_SOURCES = {"declared", "elicited", "undeclared"}
DELTA_TOKEN_RE = re.compile(r"^(2\.\d+)@([a-z0-9-]+)$")

VERDICT_LINE_RE = re.compile(
    r"^(VERDICT|RISK(?: \(partial\))?|ACCURACY):\s*(.+)$", re.MULTILINE
)
VERDICT_JSON_RE = re.compile(r"VERDICT_JSON:\s*(\{.*\})", re.DOTALL)


class CaseError(Exception):
    pass


_PROFILE_CACHE = None


def _profiles():
    """Return the profile table through the checker, loaded once."""
    global _PROFILE_CACHE
    if _PROFILE_CACHE is None:
        spec = importlib.util.spec_from_file_location(
            "check_regime_refs", REPO_ROOT / "scripts" / "check_regime_refs.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _PROFILE_CACHE = (module, module.load_profiles(REPO_ROOT))
    return _PROFILE_CACHE


def _validate_scope(name: str, expected: dict) -> None:
    """Validate the declared scope and the asserted regime set agree.

    declared_scope is the input side. expected_regimes and
    expected_regime_source are the assertion side. A case asserting a regime
    set beyond the reach of its own declaration is malformed rather than
    failing.
    """
    checker, profiles = _profiles()
    declared = expected.get("declared_scope")
    source = expected.get("expected_regime_source")
    if source is not None and source not in VALID_REGIME_SOURCES:
        raise CaseError(
            f"{name}: expected_regime_source '{source}' is not one of "
            f"{sorted(VALID_REGIME_SOURCES)}. Correct the value.")

    asserted = expected.get("expected_regimes")
    if asserted is not None:
        if not isinstance(asserted, list):
            raise CaseError(
                f"{name}: expected_regimes must be a list of slugs.")
        unknown = sorted(set(asserted) - profiles["slugs"])
        if unknown:
            raise CaseError(
                f"{name}: expected_regimes names unknown {', '.join(unknown)}. "
                "Add each to docs/regimes/scope-profiles.md or correct the case.")

    if declared is not None:
        try:
            reachable = checker.expand_scope(declared, profiles)
        except checker.ScopeError as error:
            raise CaseError(f"{name}: {error}")
        if declared == UNDECLARED and asserted:
            raise CaseError(
                f"{name}: declared_scope is undeclared and expected_regimes is "
                "non-empty. An undeclared scope reaches no regime.")
        if asserted is not None and not set(asserted) <= reachable:
            beyond = sorted(set(asserted) - reachable)
            raise CaseError(
                f"{name}: expected_regimes names {', '.join(beyond)} beyond the "
                f"reach of declared_scope '{declared}'. Widen the declaration or "
                "narrow the assertion.")

    for token in expected.get("expected_classes", []):
        if "@" not in token:
            continue
        match = DELTA_TOKEN_RE.match(token)
        if match is None:
            raise CaseError(
                f"{name}: expected_classes token '{token}' is malformed. "
                "Use the form 2.N@slug.")
        if match.group(2) not in profiles["slugs"]:
            raise CaseError(
                f"{name}: expected_classes token '{token}' names an unknown slug. "
                "Add it to docs/regimes/scope-profiles.md or correct the token.")


def load_case(case_dir: Path) -> dict:
    expected_path = case_dir / "expected.json"
    if not expected_path.is_file():
        raise CaseError(f"{case_dir.name}: missing expected.json")
    expected = json.loads(expected_path.read_text(encoding="utf-8"))

    for key in ("mode", "expected_verdict", "expected_classes", "notes"):
        if key not in expected:
            raise CaseError(f"{case_dir.name}: expected.json missing '{key}'")
    if expected["mode"] not in VALID_MODES:
        raise CaseError(
            f"{case_dir.name}: mode '{expected['mode']}' not one of {sorted(VALID_MODES)}"
        )
    # allow_non_ascii is a structural flag for corpus tests. It does not
    # change harness behavior. A case with non-ASCII fixture content must
    # set allow_non_ascii: true and state the reason in fixture_notes.
    if expected.get("allow_non_ascii") and "fixture_notes" not in expected:
        raise CaseError(
            f"{case_dir.name}: allow_non_ascii: true requires fixture_notes explaining why"
        )

    _validate_scope(case_dir.name, expected)

    input_files = [
        case_dir / name for name in CASE_INPUT_NAMES if (case_dir / name).is_file()
    ]
    if not input_files:
        raise CaseError(f"{case_dir.name}: no recognized input file present")

    context_path = case_dir / "context.md"
    context_text = context_path.read_text(encoding="utf-8") if context_path.is_file() else ""

    case_text = build_case_text(expected, input_files)
    return {
        "name": case_dir.name,
        "mode": expected["mode"],
        "expected": expected,
        "context": context_text,
        "case_text": case_text,
    }


def build_case_text(expected: dict, input_files: list) -> str:
    """Return the case text, led by the same DECLARED_SCOPE line CI emits.

    The workflow Build case text step writes that line at the head of
    case_text.txt. The corpus exercises the real channel rather than a
    fixture-only one. A case omitting declared_scope tests the ask branch and
    carries no line.
    """
    body = "\n\n".join(path.read_text(encoding="utf-8") for path in input_files)
    declared = expected.get("declared_scope")
    if declared is None:
        return body
    return f"{DECLARED_SCOPE_PREFIX} {declared}\n\n{body}"


def discover_cases(only: str | None = None) -> list[dict]:
    if not CASES_DIR.is_dir():
        raise CaseError(f"cases directory not found: {CASES_DIR}")
    dirs = sorted(p for p in CASES_DIR.iterdir() if p.is_dir())
    if only:
        dirs = [p for p in dirs if p.name == only]
        if not dirs:
            raise CaseError(f"no case named '{only}' under {CASES_DIR}")
    return [load_case(d) for d in dirs]


def verdict_matches(expected_verdict: str, response_text: str) -> tuple[bool, str]:
    match = VERDICT_LINE_RE.search(response_text)
    if not match:
        return False, "no VERDICT:/RISK:/ACCURACY: line found in response"
    actual_line = f"{match.group(1)}: {match.group(2)}".strip()
    if expected_verdict in actual_line:
        return True, actual_line
    return False, actual_line


def json_companion_ok(response_text: str) -> tuple[bool, str]:
    match = VERDICT_JSON_RE.search(response_text)
    if not match:
        return False, "no VERDICT_JSON: block found"
    try:
        json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        return False, f"VERDICT_JSON block did not parse: {exc}"
    return True, "VERDICT_JSON parsed"


def resolve_model_call(spec: str):
    module_name, _, func_name = spec.partition(":")
    if not module_name or not func_name:
        raise CaseError("--model-call must be in the form module:function")
    sys.path.insert(0, str(REPO_ROOT))
    module = importlib.import_module(module_name)
    return getattr(module, func_name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", help="run only the named case")
    parser.add_argument(
        "--model-call",
        help="module:function callable invoked as call(system_prompt, mode, case_text) -> str",
    )
    args = parser.parse_args()

    if not AUDIT_PATH.is_file():
        print(f"AUDIT.md not found at {AUDIT_PATH}", file=sys.stderr)
        return 1
    system_prompt = AUDIT_PATH.read_text(encoding="utf-8")

    try:
        cases = discover_cases(args.case)
    except CaseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not args.model_call:
        print(f"structure check only: {len(cases)} case(s) validated, no model call configured")
        for case in cases:
            print(f"  ok  {case['name']} (mode={case['mode']})")
        return 0

    model_call = resolve_model_call(args.model_call)

    failures = 0
    for case in cases:
        response = model_call(system_prompt, case["mode"], case["context"] + "\n\n" + case["case_text"])
        ok, detail = verdict_matches(case["expected"]["expected_verdict"], response)
        if ok and DISCLAIMER_PREFIX not in response:
            ok = False
            detail = f"response omits the required {DISCLAIMER_PREFIX} trailing line"
        status = "pass" if ok else "FAIL"
        print(f"  {status}  {case['name']}: expected '{case['expected']['expected_verdict']}', got '{detail}'")
        if not ok:
            failures += 1

        if case["expected"].get("expect_json"):
            json_ok, json_detail = json_companion_ok(response)
            json_status = "pass" if json_ok else "FAIL"
            print(f"  {json_status}  {case['name']} (VERDICT_JSON): {json_detail}")
            if not json_ok:
                failures += 1

    total = len(cases)
    print(f"\n{total - failures}/{total} verdict checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
