import utilities


def add_component_inventory(db, body):
    try:

        docs = db.collection("components").stream()

        for doc in docs:
            if doc.to_dict()["id"] == body["component_id"]:
                body["id"] = utilities.generate_id()
                db.collection("components_inventory").document(body["id"]).set(body)
                return {"status": 200, "description": "success"}

        return {"status": -1, "description": "Unvalid ID"}


    except Exception as e:
        return {"status": -1, "description": str(e)}

def updateamount(db, body, id):
    try:
        db.collection("components_inventory").document(id).update(body)
        return {"status":200, "description":"success"}
    except Exception as e:
        return {"status": -1, "description": str(e)}

def get_inventory_with_totals(db):
    components_inventory = db.collection('components_inventory')
    creation = db.collection('creation')

    inventory_dict = {}

    inventory_docs = components_inventory.stream()
    for doc in inventory_docs:
        doc_data = doc.to_dict()
        inventory_dict[doc.id] = doc_data
        inventory_dict[doc.id]["total_amount"] = 0

    doc_ref = db.collection("suppliers").document(inventory_dict[doc.id]["supplier_id"])
    supplier_doc = doc_ref.get()
    if supplier_doc.exists:
        inventory_dict[doc.id]["supplier_name"] = supplier_doc.to_dict().get('name', 'No Name')
    else:
        inventory_dict[doc.id]["supplier_name"] = "no name"

    creation_docs = creation.stream()
    for doc in creation_docs:
        components = doc.to_dict()
        print(components)  # Print each components object once
        if "status" in components and (components["status"] == "history" or components["status"] == "product"):
            continue
        for id, value in components["components"].items():
            if id in inventory_dict:
                inventory_dict[id]["total_amount"] += value

    return inventory_dict


def avilablelity_details(db, inventory_id):
    inventory_dict = {}
    creation = db.collection('creation')
    creation_docs = creation.stream()
    for doc in creation_docs:
        components = doc.to_dict()
        current_id = components["id"]
        for id, value in components["components"].items():
            if id == inventory_id:
                if id not in inventory_dict:
                    inventory_dict[current_id] = {"total_amount": 0, "creation": components}

                inventory_dict[current_id]["total_amount"] += value

    return inventory_dict

def get_inventory_item(db, inventory_id):
    inventory_dict = {}
    creation = db.collection('components_inventory')
    creation_docs = creation.stream()
    body = {}
    for doc in creation_docs:
        components = doc.to_dict()
        current_id = components["id"]
        if current_id == inventory_id:
            body = components
            break

    return body






