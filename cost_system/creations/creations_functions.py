from datetime import datetime
import utilities
from components_inventory import components_inventory_functions


def get_creations(db):
    try:
        docs = db.collection("creation").stream()
        body = {}
        for doc in docs:
            body[doc.to_dict()["id"]] = doc.to_dict()

        return body
    except Exception as e:
        return {"status": -1, "description": str(e)}


def create_creation(db, body):
    try:
        print("Generating ID for the document")
        body["id"] = utilities.generate_id()
        now = datetime.now()

        # Format the date and time
        formatted_date = now.strftime("%d/%m/%y-%H:%M")
        body["created_at"] = formatted_date

        if body.get("components") is None:
            doc_ref = db.collection('formulas').document(body["formula_id"])
            doc2 = doc_ref.get()
            body["components"] = {}
            if doc2.exists:
                print("Document exists, processing components")
                components = doc2.to_dict()["components"]
                for k, v in components.items():
                    body["components"][body["selected_inventory"][k]] = v / 100 * body["bottles"]
            else:
                print("No such document, setting components to an empty list")

        body.pop("selected_inventory")

        print(f"Setting the 'creation' document with ID {body['id']}")
        db.collection("creation").document(body["id"]).set(body)
        print("Operation completed successfully")
        return {"status": 200, "description": "success"}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"status": -1, "description": str(e)}



def get_document_data(db, creation_id):
    doc_ref = db.collection("creation").document(creation_id)
    doc = doc_ref.get()
    if doc.exists:
        doc = doc.to_dict()

        # Rename "components" to "inventory"
        doc['inventory'] = doc.pop('components')

        # Iterate over "inventory" items and replace values
        doc["components"] = {}
        for key in list(doc['inventory'].keys()):  # Make a copy of keys to avoid RuntimeError
            doc['components'][key] = components_inventory_functions.get_inventory_item(db, key)

        return doc
    else:
        return (f"No such document: {creation_id}")


def update_creation(db, creation_id, body):
    doc_ref = db.collection("creation").document(creation_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update(body)
        return doc_ref.get().to_dict()  # Return the document's data as a dictionary
    else:
        return (f"No such document: {creation_id}"), 404  # Return a 404 status code to indicate the document was not found


def finish(db, creation_id, body):
    doc_ref = db.collection("creation").document(creation_id)
    doc = doc_ref.get()
    if doc.exists:
        body["status"] = "waiting_for_validate"
        update_creation(db, creation_id, body)
        return doc_ref.get().to_dict()  # Return the document's data as a dictionary
    else:
        return (f"No such document: {creation_id}"), 404  # Return a 404 status code to indicate the document was not found


def validate(db, creation_id):
    print("Validating...")
    doc_ref = db.collection("creation").document(creation_id)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Document exists for creation_id: {creation_id}")
        update_creation(db, creation_id, {"status":"product"})
        data = doc.to_dict()
        components = data["components"]
        for inv_id, amount in components.items():
            print(f"Processing component with inv_id: {inv_id}, amount: {amount}")
            inv_ref = db.collection("components_inventory").document(inv_id)
            inv_doc = inv_ref.get()
            if inv_doc.exists:
                print(f"Inventory document exists for inv_id: {inv_id}")
                inv_data = inv_doc.to_dict()
                print(f"Inventory data before update: {inv_data}")
                inv_ref.update({"amount":inv_data["amount"]-amount})  # Using inv_ref here
                updated_inv_doc = inv_ref.get()  # Fetching the document again
                print(f"Updated inventory data: {updated_inv_doc.to_dict()}")
        return {"status":"200","description":"Creation has been filled to the end successfully and all the stocks has been updated."}
    else:
        print(f"No document found for creation_id: {creation_id}")
        return (f"No such document: {creation_id}"), 404  # Return a 404 status code to indicate the document was not found

