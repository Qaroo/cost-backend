"""
Formula data:
    {
        id:STRING,
        created_at:DATE,
        name:STRING,
        components: [{
            component:String (ID),
            quantity:FLOAT,
        }],
        productions:[String] (ID of production),
    }


Create new formula (/formula/create):

    body:
        {
            key:STRING,
            name:STRING,
            aliasses:[STRING],
            components: [{
                component:String (ID),
                quantity:FLOAT,
            }],
        }
    response:
        {
            status:INT,         (-1/200) - (failed/success)
            description:STRING,
            formula_id:STRING (IF SUCCESS),
        }


"""