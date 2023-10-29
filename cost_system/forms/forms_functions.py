import utilities
from datetime import datetime


def create_new_form(db, body):
    try:
        body["id"] = utilities.generate_id()
        now = datetime.now()

        # Format the date and time
        formatted_date = now.strftime("%d/%m/%y-%H:%M")
        body["date"] = formatted_date
        db.collection("forms").document(body["id"]).set(body)
        return {"status":200, "description":"success"}
    except Exception as e:
        return {"status": -1, "description": str(e)}

def update_form(db, body):
    try:
        id = body["id"]
        body.pop("id")
        db.collection("forms").document(id).update(body)
        return {"status":200, "description":"success"}
    except Exception as e:
        return {"status": -1, "description": str(e)}

def get_forms(db):
    try:
        docs = db.collection("forms").stream()
        body = {}
        for doc in docs:
            body[doc.to_dict()["id"]] = doc.to_dict()

        return body
    except Exception as e:
        return {"status": -1, "description": str(e)}
