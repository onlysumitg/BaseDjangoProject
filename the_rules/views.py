import json
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
 
# Create your views here.
from .rules import get_rules_date
from the_gateway_credentials.models import GatewayCredentials
from the_system.settings import get_page_size
from django.contrib.messages.views import SuccessMessageMixin

from .models import Rule, RuleConditions
from .forms import CreateRuleForm, CreateRuleConditionForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from the_user.decorators import otp_required, must_be
from the_user.initial_groups import CUSTOMER_CARE_SUPERVISER, CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER, ADMIN
from the_user.utils import user_is


# --------------------------------------------------------------
#
# --------------------------------------------------------------
class RulesList(ListView):
    model = Rule
    paginate_by = get_page_size()

    @method_decorator(must_be(group_name=CUSTOMER_CARE_REP))
    @method_decorator(otp_required)
    @method_decorator(login_required)
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)


# --------------------------------------------------------------
#
# --------------------------------------------------------------
@must_be(group_name=CUSTOMER_CARE_REP)
@otp_required
@login_required
def show_rules(request):
    available_gateways = GatewayCredentials.objects.all()
    context = {"rules":json.dumps(get_rules_date()) , "available_gateways":available_gateways}
    return render(request, 'the_rules/builder.html', context)


# --------------------------------------------------------------
#
# --------------------------------------------------------------
 
class RuleCreate(SuccessMessageMixin,CreateView):
    model = Rule
    form_class = CreateRuleForm
    success_message = "Rule %(name)s was created successfully"

    @method_decorator(must_be(group_name=ADMIN))
    @method_decorator(otp_required)
    @method_decorator(login_required)
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)
 
# --------------------------------------------------------------
#
# --------------------------------------------------------------
 
class RuleUpdate(SuccessMessageMixin, UpdateView):
    model = Rule
    form_class = CreateRuleForm
    template_name_suffix = '_update_form'
    success_message = "Rule %(name)s was updated successfully"


    @method_decorator(must_be(group_name=ADMIN))
    @method_decorator(otp_required)
    @method_decorator(login_required)
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)
# --------------------------------------------------------------
#
# --------------------------------------------------------------
class RuleDetails(DetailView):
    model = Rule

    def get_object(self,queryset=None):
        user = self.request.user
        pk = self.kwargs['pk']
        transaction = get_object_or_404(Rule, pk=pk )
        return transaction


    @method_decorator(must_be(group_name=CUSTOMER_CARE_REP))
    @method_decorator(otp_required)
    @method_decorator(login_required)
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)
 
# --------------------------------------------------------------
#
# --------------------------------------------------------------
class RuleConditionsCreate(SuccessMessageMixin, CreateView):
    model = RuleConditions
    form_class = CreateRuleConditionForm

    success_message = "Rule condition %(name)s was created successfully"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        rule_pk = self.kwargs['rule_pk']

        available_gateways = GatewayCredentials.objects.all()
        context["rules"] = json.dumps(get_rules_date()) 
        context["available_gateways"] =available_gateways


        context['rule'] =  get_object_or_404(Rule, pk=rule_pk)
        return context
        
    def get_initial(self):
        rule = get_object_or_404(Rule, pk=self.kwargs['rule_pk'])
        return {
            'rule':rule,
        }

    @method_decorator(must_be(group_name=ADMIN))
    @method_decorator(otp_required)
    @method_decorator(login_required)
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)

# --------------------------------------------------------------
#
# --------------------------------------------------------------
class RuleConditionsUpdate(SuccessMessageMixin, UpdateView):
    model = RuleConditions
    form_class = CreateRuleConditionForm
    success_message = "Rule condition %(name)s was updated successfully"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        rule_pk = self.kwargs['rule_pk']
        pk = self.kwargs['pk']

        available_gateways = GatewayCredentials.objects.all()
        context["rules"] = json.dumps(get_rules_date()) 
        context["available_gateways"] =available_gateways


        context['rule'] =  get_object_or_404(Rule, pk=rule_pk)
        context['condition'] =  get_object_or_404(RuleConditions, pk=pk)
        return context
        
    def get_initial(self):
        rule = get_object_or_404(Rule, pk=self.kwargs['rule_pk'])
        return {
            'rule':rule,
        }

    @method_decorator(must_be(group_name=ADMIN))
    @method_decorator(otp_required)
    @method_decorator(login_required)
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)