  return hashlib.sha256(salt + email.encode()).hexdigest()
