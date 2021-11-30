from django.urls import re_path, path
from . import   views_api 

app_name = 'the_rules_api'
urlpatterns = [

    

     path("rules", views_api.ApiRulesList.as_view(), name="rules_list"),
     path('rules/<int:id>', views_api.SingleRuleView.as_view(), name="rule_detail"),

]
