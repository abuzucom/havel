"""Identity check."""


def verify_age(user_id, document_image, selfie):
    result = idv.verify(document_image, selfie)
    db.kyc.insert({
        "user_id": user_id,
        "document_image": document_image,
        "selfie": selfie,
        "face_match_score": result.score,
        "extracted": result.all_fields,
    })
    return result.age >= 18
