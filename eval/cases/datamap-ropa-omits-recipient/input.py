def track(event, user):
    mixpanel.send(event, {"email": user.email})
    ad_partner.send(event, {"email": user.email})
