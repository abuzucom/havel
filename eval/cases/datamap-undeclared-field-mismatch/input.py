def create(form):
    return db.accounts.insert({
        "email": form["email"],
        "device_fingerprint": form["fp"],
        "ip_address": form["ip"],
    })
