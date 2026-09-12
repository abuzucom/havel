def send_reminder(user):
    """Email only. The SMS path was removed."""
    mailer.send(user.email, template="reminder")
