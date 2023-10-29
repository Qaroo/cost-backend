import uuid
import utilities



def createsupplier(db, body):
    try:
        body["id"] = utilities.generate_id()
        db.collection("suppliers").document(body["id"]).set(body)
        return {"status":200, "description":"success"}
    except Exception as e:
        return {"status": -1, "description": str(e)}

def updatesupplier(db, body, id):
    try:
        db.collection("suppliers").document(id).update(body)
        return {"status":200, "description":"success"}
    except Exception as e:
        return {"status": -1, "description": str(e)}


def add_component(db, component_id, supplier_id):
    try:
        if db.collection("suppliers").document(supplier_id) == None:
            return {"status": -1, "description": "Unvalid Supplier ID"}
        if db.collection("components").document(component_id) == None:
            return {"status": -1, "description": "Unvalid Component ID"}

        data = db.collection("suppliers").document(supplier_id).get().to_dict()

        if data["components"] == None or data["components"].isEmpty():
            data["components"] = [component_id]
        else:
            data["components"].append(component_id)

        db.collection("suppliers").document(supplier_id).update({"components":data["components"]})

    except Exception as e:
        return {"status": -1, "description": str(e)}

def update_components(db, supplier_id, components):
    try:
        if db.collection("suppliers").document(supplier_id) == None:
            return {"status": -1, "description": "Unvalid Supplier ID"}


        db.collection("suppliers").document(supplier_id).update({"components":components})
        return {"status":200, "description":"success"}

    except Exception as e:
        return {"status": -1, "description": str(e)}

def get_suppliers(db):
    try:
        docs = db.collection("suppliers").stream()
        body = {}
        for doc in docs:
            body[doc.to_dict()["id"]] = doc.to_dict()

        return body

    except Exception as e:
        return {"status": -1, "description": str(e)}


    except Exception as e:
        return {"status": -1, "description": str(e)}




