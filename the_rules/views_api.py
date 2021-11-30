from rest_framework.views import APIView
from rest_framework import generics, serializers

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from .models import Rule
from the_clients.drf.permissions import IsClient
from .serializers import  RulesSerializer
from rest_framework.exceptions import bad_request
 
class ApiRulesList(generics.ListAPIView):
    queryset = Rule.objects.all()
    serializer_class = RulesSerializer
    permission_classes = (IsAuthenticated,IsClient)  
 
    
 

class SingleRuleView(generics.RetrieveAPIView):
    queryset = Rule.objects.all()

    lookup_field = "id"
    serializer_class = RulesSerializer
    permission_classes = (IsAuthenticated,IsClient)  
   