"""Cold storage."""


def archive_old_accounts():
    """Move accounts older than two years to cheaper storage."""
    for account in db.accounts.older_than(days=730):
        cold_storage.put(account.id, account.to_dict())
        db.accounts.mark_archived(account.id)
