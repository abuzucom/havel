def save_note(order_id, text):
    return db.notes.insert({"order_id": order_id, "text": text})
