"""
component inventory data:
    id:STRING, component_id:STRING,batch:STRING,validity:DATE,AMOUNT:FLOAT,SUPPLIER_ID:STRING,transaction_id:LONG,PRICE:FLOAT,COSHER:STRING,saves:[STRING (List of saves ID)]


Functions:

Create new Inventory component (/inventory_component/add):
    body: {
        key:STRING (security)
        component_id:STRING,
        batch:STRING,
        validity:DATE,
        AMOUNT:FLOAT,
        SUPPLIER_ID:STRING,
        transaction_id:LONG
    }
    response:
    {
        status:INT(-1/200 - failed/success)
        description:STRING,
        ID:STRING (*IF SUCCESS)
    }


"""