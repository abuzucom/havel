#!/usr/bin/env python3
"""Local-only model-call example for eval/run_eval.py.

Return a fixed synthetic response. The --model-call seam stays exercised
without a provider credential. Never point the harness at this module to
judge a real case. The response is a constant and proves nothing about
the case.
"""


def call_model(system_prompt: str, mode: str, case_text: str) -> str:
    """Return a fixed synthetic verdict for structural testing only."""
    return (
        "VERDICT: BLOCK - synthetic test\n"
        'VERDICT_JSON: {"mode": "PR", "verdict": "BLOCK", "findings": []}'
    )
