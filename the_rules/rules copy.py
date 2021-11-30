

# https://github.com/venmo/business-rules
# https://github.com/venmo/business-rules-ui


from business_rules.variables import ( 
    BaseVariables,
    numeric_rule_variable,
    string_rule_variable,
    select_rule_variable
    
)



from business_rules.actions import BaseActions, rule_action

from business_rules.fields import FIELD_TEXT,FIELD_NUMERIC
from business_rules import run_all


import datetime

class ProductVariables(BaseVariables):

    def __init__(self):
        pass

    @numeric_rule_variable
    def current_inventory(self):
        return 10

    @numeric_rule_variable(label='Days until expiration')
    def expiration_days(self):
        last_order = self.product.orders[-1]
        return (last_order.expiration_date - datetime.date.today()).days

    @string_rule_variable()
    def current_month(self):
        return datetime.datetime.now().strftime("%B")

    # @select_rule_variable(options=Products.top_holiday_items())
    # def goes_well_with(self):
    #     return products.related_products


class ProductActions(BaseActions):

    def __init__(self):
         pass

    @rule_action(params={"sale_percentage": FIELD_NUMERIC})
    def put_on_sale(self, sale_percentage):
        print('its on sale',sale_percentage)

    @rule_action(params={"number_to_order": FIELD_NUMERIC})
    def order_more(self, number_to_order):
        print("ordering more ....")


rules = [
    { "conditions": { "all": [
      { "name": "current_month",
        "operator": "equal_to",
        "value": 'November',
      },
      { "name": "current_inventory",
        "operator": "greater_than",
        "value": 5,
      },
  ]},
  "actions": [
      { "name": "put_on_sale",
        "params": {"sale_percentage": 0.25},
      },
  ],
},



]

# run_all(rule_list=rules,
#             defined_variables=ProductVariables(),
#             defined_actions=ProductActions(),
#             stop_on_first_trigger=True
#            )


cnd = {"all":[
                {"name":"address_state","operator":"contains","value":"s"},
                {"name":"address_zip","operator":"contains","value":"232"},
                {"any":[
                    {"name":"last_4_of_card","operator":"contains","value":"44"},
                    {"name":"last_4_of_card","operator":"equals","value":"244"},
                    {"all":[
                        {"name":"address_state","operator":"contains","value":"s1"},
                        {"name":"address_state","operator":"contains","value":"s3"},
                        ]}
                    ]
                }
            ]
        }

x1= []

str1 =""
def check_conditions_recursively(conditions, opr):
    global str1
 
    keys = list(conditions.keys())
    if keys == ['all']:
        opr = ""
        assert len(conditions['all']) >= 1
        str1 += "("
        for condition in conditions['all']:
            
            str1 += f" {opr} "
            check_conditions_recursively(condition,opr)
            opr ="and"
               
        str1 += ")"
        return True

    elif keys == ['any']:
        opr = ""
        assert len(conditions['any']) >= 1
        str1 += "("
        for condition in conditions['any']:
            
            str1 += f" {opr} "
            check_conditions_recursively(condition,opr)
            opr ="or"
               
        str1 += ")"
        return True

    else:
        # help prevent errors - any and all can only be in the condition dict
        # if they're the only item
        assert not ('any' in keys or 'all' in keys)
       
        str1+= str_condition(conditions)
      
        return True


def str_condition(condition):
    return f'{condition["name"]} {condition["operator"]} "{condition["value"]}"'
  

check_conditions_recursively(cnd,"")

print("Str --------------------------------->>" , str1)