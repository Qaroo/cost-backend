"""
component data:
     id:STRING,
     name:STRING,
     aliasses:[STRING],
     botancial_he:STRING,
     botancial_en:STRING,
     type:STRING,
     subtype:STRING,
     work_time:FLOAT,
     work_temp:FLOAT,
     alert_amount:FLOAT



Create New Component /components/create:
    body:
    {
        key:STRING (security),
        name:STRING,
        aliasses:[STRING],
        botancial_he:STRING,
        botancial_en:STRING,
        type:STRING,
        subtype:STRING,
        work_time:FLOAT,
        work_temp:FLOAT,
        alert_amount:FLOAT
    }

    response:
    {
        status:INT(-1/200 - failed/success)
        description:STRING,
        ID:STRING (*IF SUCCESS)
    }

Update Existing component (/components/update):

    body:
    {
        key:STRING (security),
        id:STRING
        body to update...
    }
    response:
    {
        status:INT(-1/200 - failed/success)
        description:STRING,
        ID:STRING (*IF SUCCESS)
    }




"""