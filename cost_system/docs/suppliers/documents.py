"""
Supplier data:
    ID, name, phone1, phone2, contact1, contact2, mail, address, ISO, cerificates (PDFS List), List of components (IDS)

Functions:

Create Supplier (/suppliers/create):
    body:
    {
        name:SRRING
        phone1:STRING
        phone2:STRING
        contact1:STRING
        contact2:STRING
        mail:STRING
        address:STRING
        ISO:STRING
        cerificates:LIST<URL> //for the pdf links
    }

    response:
    {
        status:(200/-1) (success/failed)
        description:STRING
        id:STRING //supplier id
    }

Add component to supplier (/suppliers/add_component):
    body:
    {
        key:STRING (hashed password)
        supplier:STRING //supplier id
        component:STRING //component id
    }
    response:
    {
        status:(200/-1) (success/failed)
        description:STRING
    }

Get info of supplier (/suppliers/info):
    body:
    {
        key:STRING (security)
        id:STRING //of the supplier
    }
    response:
    {
        phone1:STRING
        phone2:STRING
        contact1:STRING
        contact2:STRING
        mail:STRING
        address:STRING
        ISO:STRING
        cerificates:LIST<URL> //for the pdf links
        components:LIST<STRING> //for the components ids
    }

Get Suppliers List
    body:
    {
        key:STRING (security)
    }
    response:
    {
        [
        {
        supplier_id: {
            phone1:STRING
            phone2:STRING
            contact1:STRING
            contact2:STRING
            mail:STRING
            address:STRING
            ISO:STRING
            cerificates:LIST<URL> //for the pdf links
            components:LIST<STRING> //for the components ids
            }
        }
        ]
    }

Get list of suppliers:
    body:
    {
        key:STRING (security)
    }
    response:
    [
    {
        phone1:STRING
        phone2:STRING
        contact1:STRING
        contact2:STRING
        mail:STRING
        address:STRING
        ISO:STRING
        ISO:STRING
        cerificates:LIST<URL> //for the pdf links
        components:LIST<STRING> //for the components ids
    }
    ]

Update Supplier:
    body:
    {
        key:STRING (security)
        DATA TO UPDATE: {
            X:Y
        }
    }
    response:
    {
        status:(200/-1) (success/failed)
        description:STRING
    }
"""
