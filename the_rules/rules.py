

# https://github.com/venmo/business-rules
# https://github.com/venmo/business-rules-ui


from business_rules.variables import ( 
    BaseVariables,
    numeric_rule_variable,
    string_rule_variable,
    select_rule_variable
    
)



from business_rules.actions import BaseActions, rule_action

from business_rules.fields import FIELD_TEXT,FIELD_NUMERIC,FIELD_SELECT
from business_rules import run_all


import datetime
import calendar

#from the_gateway_credentials.models import GatewayCredentials


class PaymentRequestVariables(BaseVariables):

    def __init__(self, payment_request):
        self.payment_request = payment_request


    @select_rule_variable(options= list(calendar.month_name))
    def current_month(self):
        return datetime.datetime.now().strftime("%B")

    @select_rule_variable(options= list(calendar.day_name))
    def current_day(self):
        return datetime.datetime.now().strftime("%A")

    @numeric_rule_variable
    def payment_amount(self):
        
        print(" ** "*20)
        print("self.payment_request.amount",self.payment_request.amount)
        print(" ** "*20)
        return self.payment_request.amount

    @string_rule_variable()
    def transaction_type(self):
        return self.payment_request.get_request_type_display()

    @string_rule_variable()
    def card_bin(self):
        return str(self.payment_request.card)[1:6]

    @string_rule_variable()
    def last_4_of_card(self):
        return str(self.payment_request.card)[-4:]

    @string_rule_variable()
    def address_state(self):
        return self.payment_request.state

    @string_rule_variable()
    def address_zip(self):
        return self.payment_request.zip
    # @select_rule_variable(options=Products.top_holiday_items())
    # def goes_well_with(self):
    #     return products.related_products


class PaymentRequestActions(BaseActions):

    def __init__(self, payment_request):
        self.payment_request = payment_request

    @rule_action(params={"gateway": FIELD_SELECT})
    def use(self, gateway):
        # gwc = GatewayCredentials.get_by_id(gateway)
        # self.payment_request.gateway = gwc
        # self.payment_request.save()
        print('please use >>>>>>>>>>>>>>>>>>>>>>>>>>>>> =======> ',gateway, gwc)

    # @rule_action(params={"sale_percentage": FIELD_NUMERIC})
    # def put_on_sale(self, sale_percentage):
    #     print('its on sale',sale_percentage)

    # @rule_action(params={"number_to_order": FIELD_NUMERIC})
    # def order_more(self, number_to_order):
    #     print("ordering more ....")




# from business_rules import run_all
# run_all(rule_list=rules,
#             defined_variables=ProductVariables(),
#             defined_actions=ProductActions(),
#             stop_on_first_trigger=True
#            )


def get_rules_date():
    from business_rules import export_rule_data
    return export_rule_data(PaymentRequestVariables, PaymentRequestActions)