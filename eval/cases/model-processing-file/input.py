"""Support summarizer."""


def summarize_ticket(ticket):
    prompt = f"Summarize this support ticket:\n{ticket.full_record()}"
    return llm.complete(prompt)


def index_customers():
    for customer in db.customers.all():
        vectors.upsert(customer.id, embed(customer.to_dict()))
