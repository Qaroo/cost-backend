import firebase_admin
from firebase_admin import credentials,firestore
from flask import Flask, request, make_response, abort, current_app as app, json, jsonify

from customers import customers_functions
from forms import forms_functions
from creations import creations_functions
from suppliers import supplier_functions
from werkzeug.security import generate_password_hash, check_password_hash
from components import components_functions
from components_inventory import components_inventory_functions
from flask_cors import CORS
import json
from formula import formulas_functions
import time

ip_whitelist = ['127.0.0.1']
password="t7vrOI8COf5nP5UE75SId6M&3eRZ#Q"
app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("cost-system-sdk.json")
firebase_admin.initialize_app(cred)

db = firestore.client()



#whitelist ip blocks:
"""
@app.before_request
def block_method():
    ip = request.remote_addr
    if ip not in ip_whitelist:
        print(f"{ip} blocked")
        abort(403)
"""


#create supplier route
@app.route("/suppliers/create", methods=["POST"])
def supplier_creation():
    body = convertData(request)
    auth = body["key"]
    if not auth or auth != password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    body["key"] = None

    res = supplier_functions.createsupplier(db, body)
    return res

#update supplier route
@app.route("/suppliers/update", methods=["POST"])
def supplier_update():
    body = convertData(request)
    auth = body["key"]
    if not auth or auth != password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    body["key"] = None
    id = body["id"]
    body.pop("id")
    res = supplier_functions.updatesupplier(db, body, id)
    return res

#update customer route
@app.route("/customers/update", methods=["POST"])
def customer_update():
    body = convertData(request)
    auth = body["key"]
    if not auth or auth != password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    body["key"] = None
    id = body["id"]
    body.pop("id")
    res = customers_functions.updatecustomer(db, body, id)
    return res

#add component to supplier route
@app.route("/suppliers/add_component", methods=["POST"])
def add_component_to_supplier():
    body = convertData(request)
    auth = body["key"]
    if not auth or auth != password or not check_password_hash(auth, password):
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    body["key"] = None

    res = supplier_functions.add_component(db, body["component_id"], body["supplier_id"])
    return res

@app.route("/suppliers/update_components", methods=["POSt"])
def update_supplier_components():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        document_data = supplier_functions.update_components(db, body["id"], body["components"])
        return document_data

    except Exception as e:
        return str(e)

@app.route("/formulas/info", methods=["POST"])
def formula_info():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        document_data = formulas_functions.get_formula_with_components_data(db, body["id"])
        return document_data

    except Exception as e:
        return str(e)

@app.route("/customers/info", methods=["POST"])
def customer_info():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        document_data = customers_functions.get_customer_with_formula_data(db, body["id"])
        return document_data

    except Exception as e:
        return str(e)


#get supplier info route.
@app.route("/suppliers/info", methods=["POST"])
def suppliers_info():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        docs = db.collection("suppliers").stream()
        for doc in docs:
            if doc.to_dict()["id"] == body["id"]:
                return db.collection("suppliers").document(body["id"]).get().to_dict()

        return "Didnt found Supplier ID"

    except Exception as e:
        return str(e)


@app.route("/formulas/get_inventory_for_formula", methods=["POST"])
def get_inventory_for_formula():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        res = formulas_functions.get_inventory_for_formula(db,body["formula_id"],body["bottles_amount"])
        return res




    except Exception as e:
        return str(e)

@app.route("/components/info", methods=["POST"])
def components_info():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        docs = db.collection("components").stream()
        for doc in docs:
            if doc.to_dict()["id"] == body["id"]:
                return db.collection("components").document(body["id"]).get().to_dict()

        return "Didnt found Component ID"



    except Exception as e:
        return str(e)

@app.route("/components_inventory/av_details", methods=["POST"])
def inventory_av_details():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        res = components_inventory_functions.avilablelity_details(db, body["id"])


        return res

    except Exception as e:
        return str(e)

@app.route("/creations/info", methods=["POST"])
def creation_info():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        document_data = creations_functions.get_document_data(db, body["id"])
        return document_data

    except Exception as e:
        return str(e)

@app.route("/formulas/list", methods=["POST"])
def formulas_list():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        res = formulas_functions.get_formulas(db)
        return res

    except Exception as e:
        return "Server Error: " + str(e)

@app.route("/components_inventory/list", methods=["POST"])
def components_inventory_list():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        res = components_inventory_functions.get_inventory_with_totals(db)
        return res

    except Exception as e:
        return "Server Error: " + str(e)





#Get suppliers List
@app.route("/components/list", methods=["POST"])
def components_list():
    try:
        body = convertData(request)
        print(f"body: {body}")
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        res = components_functions.get_components(db)
        return res

    except Exception as e:
        return "Server Error: " + str(e)

@app.route("/forms/list", methods=["POST"])
def forms_list():
    try:
        body = convertData(request)
        print(f"body: {body}")
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        res = forms_functions.get_forms(db)
        return res

    except Exception as e:
        return "Server Error: " + str(e)

@app.route("/creations/list", methods=["POST"])
def creations_list():
    try:
        body = convertData(request)
        print(f"body: {body}")
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        res = creations_functions.get_creations(db)
        return res

    except Exception as e:
        return "Server Error: " + str(e)


@app.route("/suppliers/list", methods=["POST"])
def get_suppliers_list():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        dictionary = {}
        docs = db.collection("suppliers").stream()
        for doc in docs:
            dictionary[doc.to_dict()["id"]] = doc.to_dict()

        return dictionary


    except Exception as e:
        return "Server Error: " + str(e)

@app.route("/customers/list", methods=["POST"])
def get_customers_list():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        dictionary = {}
        docs = db.collection("customers").stream()
        for doc in docs:
            dictionary[doc.to_dict()["id"]] = doc.to_dict()

        return dictionary


    except Exception as e:
        return "Server Error: " + str(e)


@app.route("/suppliers/update", methods=["POST"])
def update_supplier():
    try:
        body = convertData(request)
        body = body.to_dict()
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        body.pop("key")

        db.collection("suppliers").document(body["id"]).update(body)


        return "Success"



    except Exception as e:
        return str(e)


def convertData(request):
    body_str = json.dumps(request.form.to_dict())
    body = json.loads(body_str)
    body = body["data"]
    return json.loads(body)
@app.route("/components/create", methods=["POST"])
def create_component():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        res = components_functions.create_new_component(db, body)
        return res
    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)

@app.route("/creations/create", methods=["POST"])
def create_creation():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        res = creations_functions.create_creation(db, body)
        return res
    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)

@app.route("/creations/update", methods=["POST"])
def update_creation():
    try:
        body = convertData(request)
        auth = body.get("key")  # Safely get key, will not raise an error if key is not present
        if auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        id = body.pop("id")
        res = creations_functions.update_creation(db, id, body.get("update"))  # Safely get update
        return res
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return str(e), 500  # Return the exception as a string with a 500 status code to indicate a server error


@app.route("/inventory_component/add", methods=["POST"])
def add_inventory_component():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        res = components_inventory_functions.add_component_inventory(db, body)
        return res

    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)

@app.route("/inventory_component/update_stock", methods=["POST"])
def update_inventory_component():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        id = body["id"]
        body.pop("id")
        res = components_inventory_functions.updateamount(db, body, id)
        return res

    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)

@app.route("/formulas/create", methods=["POST"])
def create_formula():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        return formulas_functions.create_formula(db, body["name"], body["components"], body["created_by"], body)

    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)

@app.route("/formulas/edit", methods=["POST"])
def edit_formula():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        return formulas_functions.update_formula(db,body["id"], body["name"], body["created_by"], body)

    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)

@app.route("/customers/create", methods=["POST"])
def create_customer():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        return customers_functions.createCustomer(db, body)

    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)




@app.route("/customers/add_formula", methods=["POST"])
def add_to_inventory():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        res = customers_functions.add_formula(db, body["customer"], body["formula"], body["customer_name"])
        return res

    except Exception as e:
        return str(e)


@app.route("/components/update", methods=["POST"])
def update_component():
    try:
        body = convertData(request)
        auth = body["key"]
        id = body["id"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        docs = db.collection("components").stream()
        for doc in docs:
            if doc.to_dict()["id"] == body["id"]:
                body.pop("id")
                res = components_functions.update_component(db, body, id)
                return res

        return {"status":-1,"description":"invalid component id."}

    except Exception as e:
        return str(e)


@app.route("/forms/create", methods=["POST"])
def create_form():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        return forms_functions.create_new_form(db, body)

    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)

@app.route("/forms/update", methods=["POST"])
def update_form():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        return forms_functions.update_form(db, body)

    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)

@app.route("/creations/finish", methods=["POST"])
def finish_creation():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        id = body["id"]
        return creations_functions.finish(db, id, body.get("update"))

    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)

@app.route("/creations/validate", methods=["POST"])
def validate_creation():
    try:
        body = convertData(request)
        auth = body["key"]
        if not auth or auth != password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        body.pop("key")
        id = body["id"]
        return creations_functions.validate(db, id)

    except Exception as e:
        body = convertData(request)
        print(type(body))
        return str(e)



app.run(port=5151)




