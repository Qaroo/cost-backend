from datetime import datetime
import uuid
import utilities




def get_customers(db):
    try:
        docs = db.collection("customers").stream()
        body = {}
        for doc in docs:
            body[doc.to_dict()["id"]] = doc.to_dict()

        return body


    except Exception as e:
        return {"status": -1, "description": str(e)}

def createCustomer(db, body):
    try:
        body["id"] = utilities.generate_id()
        now = datetime.now()
        formatted_date = now.strftime("%d/%m/%y-%H:%M")
        body["date"] = formatted_date

        print(f"Creating customer with data: {body}") # Add this line

        db.collection("customers").document(body["id"]).set(body)

        print("Customer created successfully") # Add this line

        return {"status":200, "description":"success"}
    except Exception as e:
        print(f"Error creating customer: {str(e)}") # Add this line
        return {"status": -1, "description": str(e)}

def updatecustomer(db, body, id):
    try:
        db.collection("customers").document(id).update(body)
        return {"status":200, "description":"success"}
    except Exception as e:
        return {"status": -1, "description": str(e)}



def add_formula(db, document_id, formula_id, customer_name):
    try:
        collection = "customers"
        components_collection = "formulas"
        formula_ref = db.collection(collection).document(document_id)
        formula_snapshot = formula_ref.get()
        formula_data = formula_snapshot.to_dict()

        if formula_data is not None and "formulas" in formula_data:
            formulas = formula_data["formulas"]
            formulas.append(formula_id)
            formula_ref.update({"formulas": formulas})

            # Update the "formulas" collection
            formulas_collection_ref = db.collection(components_collection).document(formula_id)
            formulas_collection_ref.update({"customer": document_id, "customer_name": customer_name})

            return {"description": "success"}
        else:
            return {"description": "Error: 'formulas' field not found or document data is empty"}
    except Exception as e:
        return {"description": "Error " + str(e)}


def get_customer_with_formula_data(db, document_id):
    collection = "customers"
    components_collection = "formulas"
    formula_ref = db.collection(collection).document(document_id)
    formula = formula_ref.get()

    if formula.exists:
        formula_data = formula.to_dict()

        # Get components data
        components_data = {}
        for component_id in formula_data['formulas']:
            component_ref = db.collection(components_collection).document(component_id)
            component = component_ref.get()

            if component.exists:
                component_data = component.to_dict()
                components_data[component_id] = component_data
            else:
                print(f"No such component: {component_id}")

        # Include components data in the formula's body
        formula_data['formulas'] = components_data
        return formula_data
    else:
        print(f"No such document: {document_id}")
        return None




