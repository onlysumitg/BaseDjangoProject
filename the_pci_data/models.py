from django.db import models
 

from fernet_fields import EncryptedCharField, EncryptedIntegerField

 

# Create your models here.
class PCI_Data(models.Model):
    value = EncryptedCharField(max_length=100,)
     