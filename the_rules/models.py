from django.db import models
from django.db.models.base import Model
import json

from the_gateway_credentials.models import GatewayCredentials
# Create your models here.

class Rule(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    description = models.TextField(null=True, blank=True)
    priority = models.DecimalField(max_digits=5, decimal_places=2, default=1, unique=True)

    class Meta:
        ordering = ['-priority']

    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('the_rules:detail', kwargs={'pk' : self.pk })


    def active_conditions(self):
        return self.conditions.filter(is_active=True)

    def inactive_conditions(self):
        return self.conditions.filter(is_active=False) 
    
    def get_rules(self):
        rules = []
        conditions = self.conditions.filter(is_active=True)

        for condition in conditions:
            rules.append(condition.build_rule())

        print(" >>>>>>>>>>>>>>>>>>>>>>>>>>s>>>>>>>>rules>>>>>. ")
        print(rules)
        print(" >>>>>>>>>>>>>>>>>>>>>>>>>>e>>>>>>>>rules>>>>>. ")

        return rules


    def __str__(self):
        return self.name

    @classmethod
    def get_default(cls):
        return Rule.objects.order_by('-priority').first()


# ----------------------------------------------------------------
#
# ----------------------------------------------------------------

class RuleConditions(models.Model):
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name="conditions")
    name = models.CharField(max_length=25, default="")
    condition = models.TextField()
    action = models.TextField()
    readable_text = models.TextField(null = True,blank= True)
    is_active = models.BooleanField(default=True)
    gateway = models.ForeignKey(GatewayCredentials, null=True, blank=True, on_delete=models.CASCADE, related_name="inconditions")
    sequence = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    class Meta:
        ordering = ['sequence']
        unique_together = [['rule', 'name'],['rule', 'sequence'] ]

    def save(self,*args, **kwargs):
        global str1
        str1 = ""
        self.readable_text = get_readable_text(json.loads(str(self.condition)))
        #self.readable_text += get_readable_for_Action(json.loads(str(self.action)))

        self.gateway = self.get_gateway()


        super().save(*args,**kwargs)

        
    def __str__(self) -> str:
        return f"{self.rule.name}:{self.name}"



    def get_gateway(self):
        actions = json.loads(str(self.action))
        print("apoint1" ,  type(actions))
        if type(actions) is list:
            action = actions[0]
            print("apoint2" ,  type(action), action)
            if type(action) is dict:
                try:
                    gateway_id= int(action['params']['gateway'])
                    print("apoint2" ,  gateway_id)
                    gateway = GatewayCredentials.objects.get(pk=gateway_id) 
                    return gateway
                except Exception as e:
                    print("point4",e)
                    return None
        
        return None



    def build_rule(self):
        rule = {}
        rule['conditions'] = json.loads(str(self.condition))
        rule['actions'] = json.loads(str(self.action))
        return rule

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('the_rules:update_condition', kwargs={'pk' : self.pk , 'rule_pk':self.rule.pk})



def get_readable_for_Action(actions):
    if type(actions) is list:
        action = actions[0]
        if type(action) is dict:
            return f"{action['name']} - {action['params']['gateway']}"
    
    return ""


 


str1= ""
def get_readable_text(conditions, opr=''):
     
    global str1
 
    keys = list(conditions.keys())
    if keys == ['all']:
        opr = ""
        assert len(conditions['all']) >= 1
        str1 += "("
        for condition in conditions['all']:
            
            str1 += f" {opr} "
            get_readable_text(condition,opr)
            opr ="and"
               
        str1 += ")"
        return str1

    elif keys == ['any']:
        opr = ""
        assert len(conditions['any']) >= 1
        str1 += "("
        for condition in conditions['any']:
            
            str1 += f" {opr} "
            get_readable_text(condition,opr)
            opr ="or"
               
        str1 += ")"
        return str1

    else:
        # help prevent errors - any and all can only be in the condition dict
        # if they're the only item
        assert not ('any' in keys or 'all' in keys)
       
        str1+= str_condition(conditions)
         
        return str1


def str_condition(condition):
    return f'{condition["name"]} {condition["operator"]} "{condition["value"]}"'