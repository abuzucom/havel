"""Credit gate."""


def evaluate_application(applicant):
    score = model.predict(applicant.features())
    if score < 0.4:
        return {"decision": "declined"}
    return {"decision": "approved"}
