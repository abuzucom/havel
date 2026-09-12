"""Profiling."""

STATE_OPT_OUT = {"UT": "/opt-out"}


def build_profile(user):
    """Profile for a significant decision with no opt-out path."""
    return scores.write(user.id, model.score(user))
