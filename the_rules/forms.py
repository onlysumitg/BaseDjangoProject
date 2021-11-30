from django import forms
from .models import Rule, RuleConditions


class CreateRuleForm(forms.ModelForm):
 

    class Meta:
        model = Rule
        fields = ['name','description','priority' ]




class CreateRuleConditionForm(forms.ModelForm):
 

    class Meta:
        model = RuleConditions
        fields = ['name','rule','condition','action','sequence' , 'is_active' ]
        widgets = {'condition': forms.HiddenInput() ,
                    'action' : forms.HiddenInput() ,
                    'rule' :forms.HiddenInput() ,
                    }
