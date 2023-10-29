import uuid
from datetime import datetime
import utilities
from customers import customers_functions
from components import components_functions

def create_formula(db, name, components, created_by, bod):
    try:
        body = {}
        body["id"] = utilities.generate_id()
        now = datetime.now()
        formatted_date = now.strftime("%d/%m/%y-%H:%M")
        body["date"] = formatted_date
        body["name"] = name
        body["status"] = bod["status"]
        body["components"] = components
        body["created_by"] = created_by
        body["barcode"] = bod["barcode"]
        body["description"] = bod["description"]
        body["note"] = bod["note"]
        body["dailyAmount"] = bod["dailyAmount"]
        body["bottleSize"] = bod["bottleSize"]
        body["productionHours"] = bod["productionHours"]
        body["customer_name"] = bod["customer_name"]
        body["customer"] = bod["customer_id"]
        body["graphics"] = bod["graphics"]
        db.collection("formulas").document(body["id"]).set(body)
        customers_functions.add_formula(db, body["customer"], body["id"], body["customer_name"])
        return {"status": 200, "description": "success"}
    except Exception as e:
        return {"status": -1, "description": str(e)}

def update_formula(db, id, name, created_by, bod):
    try:
        updated_body = {
            "name": name,
            "status": bod["status"],
            "created_by": created_by,
            "barcode": bod["barcode"],
            "description": bod["description"],
            "note": bod["note"],
            "dailyAmount": bod["dailyAmount"],
            "bottleSize": bod["bottleSize"],
            "productionHours": bod["productionHours"],
        }
        db.collection("formulas").document(id).update(updated_body)
        return {"status": 200, "description": "success"}
    except Exception as e:
        return {"status": -1, "description": str(e)}



def get_document_data(db, formula_id):
    doc_ref = db.collection("formulas").document(formula_id)
    doc = doc_ref.get()
    if doc.exists:

        body = {}
        doc = doc.to_dict()

        return doc
    else:
        return (f"No such document: {formula_id}")



def get_formula_with_components_data(db, document_id):
    collection = "formulas"
    components_collection = "components"
    formula_ref = db.collection(collection).document(document_id)
    formula = formula_ref.get()

    if formula.exists:
        formula_data = formula.to_dict()

        # Get components data
        components_data = {}
        for component_id, ratio in formula_data['components'].items():
            component_ref = db.collection(components_collection).document(component_id)
            component = component_ref.get()

            if component.exists:
                component_data = component.to_dict()
                component_data['ratio'] = ratio
                components_data[component_id] = component_data
            else:
                print(f"No such component: {component_id}")

        # Include components data in the formula's body
        formula_data['components'] = components_data
        return formula_data
    else:
        print(f"No such document: {document_id}")
        return None

def get_inventory_for_formula(db, formula_id, bottlesAmount):
    formula_ref = db.collection("formulas").document(formula_id)
    formula = formula_ref.get()
    res = {}
    if formula.exists:
        formula_data = formula.to_dict()
        comps = formula_data["components"]
        for k,v in comps.items():
            res[k] = {}
            amount = v/100 * bottlesAmount
            components_functions.get_inventories(db, k)
            res[k]["inventories"] = components_functions.get_inventories(db, k)
            res[k]["needed_amount"] = amount

    return res


def get_formulas(db):
    try:
        docs = db.collection("formulas").stream()
        body = {}
        for doc in docs:
            body[doc.to_dict()["id"]] = doc.to_dict()
        return body
    except Exception as e:
        return {"status": -1, "description": str(e)}
