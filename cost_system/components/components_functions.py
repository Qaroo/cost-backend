import utilities
from datetime import datetime


def create_new_component(db, body):
    try:
        body["id"] = utilities.generate_id()
        now = datetime.now()

        # Format the date and time
        formatted_date = now.strftime("%d/%m/%y-%H:%M")
        body["date"] = formatted_date
        db.collection("components").document(body["id"]).set(body)
        return {"status":200, "description":"success"}
    except Exception as e:
        return {"status": -1, "description": str(e)}

def update_component(db, body, id):
    try:
        db.collection("components").document(id).update(body)
        return {"status": 200, "description": "success"}
    except Exception as e:
        return {"status": -1, "description": str(e)}

def get_components(db):
    try:
        docs = db.collection("components").stream()
        body = {}
        for doc in docs:
            body[doc.to_dict()["id"]] = doc.to_dict()

        return body
    except Exception as e:
        return {"status": -1, "description": str(e)}

def get_inventories(db, id):
    try:
        docs = db.collection("components_inventory").stream()
        body = {}
        for doc in docs:
            if(doc.to_dict()["component_id"] == id):
                body[doc.to_dict()["id"]] = doc.to_dict()

        return body
    except Exception as e:
        return {"status": -1, "description": str(e)}
