from re import S
from rest_framework import  serializers
from the_gateway_credentials.serializers import GatewayCredentialsSerializerWithGatewayName
from .models import Rule, RuleConditions


class RuleConditionsSerializer(serializers.ModelSerializer):
    gateway = GatewayCredentialsSerializerWithGatewayName(many=False, read_only=True)

 
    class Meta:
        model = RuleConditions
        fields = ('id','sequence','name','is_active','readable_text','gateway')

class RulesSerializer(serializers.ModelSerializer):
    conditions = RuleConditionsSerializer(many=True, read_only=True)

 
 
    class Meta:
        model = Rule
        fields = ('name','description','priority','conditions')


 