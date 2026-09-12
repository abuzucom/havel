"""Fixture exercising 2.18 under cpa."""

STATE_OPT_OUT = {"CO": "/opt-out"}


def decide(applicant):
    return {"decision": "declined" if model.score(applicant) < 0.4 else "approved"}
