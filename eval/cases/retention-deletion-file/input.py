"""Account deletion."""


def delete_account(user_id):
    """Mark the row deleted and return success."""
    db.users.update(user_id, {"deleted_at": now()})
    return {"status": "deleted"}
