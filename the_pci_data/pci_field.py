from django.conf import settings
from django.core.exceptions import FieldError, ImproperlyConfigured
from django.db import models
from django.utils.encoding import force_bytes, force_text
from django.utils.functional import cached_property
from .models import PCI_Data

__all__ = [
    'PCIField',
    'PCITextField',
    'PCICharField',
    'PCIEmailField',
    'PCIIntegerField',
    'PCIDateField',
    'PCIDateTimeField',
]


class PCIField(models.Field):
    """A field that encrypts values using Fernet symmetric encryption."""
    _internal_type = 'CharField'

    def __init__(self, *args, **kwargs):
        if kwargs.get('primary_key'):
            raise ImproperlyConfigured(
                "%s does not support primary_key=True."
                % self.__class__.__name__
            )
        if kwargs.get('unique'):
            raise ImproperlyConfigured(
                "%s does not support unique=True."
                % self.__class__.__name__
            )
        if kwargs.get('db_index'):
            raise ImproperlyConfigured(
                "%s does not support db_index=True."
                % self.__class__.__name__
            )
        super().__init__(*args, **kwargs)

 

   

    # def get_internal_type(self):
    #     return self._internal_type

    # prepare value to write in db
    def get_db_prep_save(self, value, connection):
        value = super().get_db_prep_save(value, connection)
        if value is not None:
            return self.tokenize(value)

    def tokenize(self, value):
        pci_data = PCI_Data()
        pci_data.value = str(value)
        pci_data.save()
        return pci_data.pk

    # read value from DB
    def from_db_value(self, value, expression, connection, *args):
        if value is not None:
            return self.to_python(self.de_tokenize(value))

    def de_tokenize(self, value):
        actual_value = value
        try:
            pci_data = PCI_Data.objects.get(pk=value)
            actual_value = pci_data.value
        except:
            actual_value = value
        return actual_value

    @cached_property
    def validators(self):
        # Temporarily pretend to be whatever type of field we're masquerading
        # as, for purposes of constructing validators (needed for
        # IntegerField and subclasses).
        self.__dict__['_internal_type'] = super().get_internal_type()
        try:
            return super().validators
        finally:
            del self.__dict__['_internal_type']         



def get_prep_lookup(self):
    """Raise errors for unsupported lookups"""
    raise FieldError("{} '{}' does not support lookups".format(
        self.lhs.field.__class__.__name__, self.lookup_name))


# Register all field lookups (except 'isnull') to our handler
for name, lookup in models.Field.class_lookups.items():
    # Dynamically create classes that inherit from the right lookups
    if name != 'isnull':
        lookup_class = type('PCIField' + name, (lookup,), {
            'get_prep_lookup': get_prep_lookup
        })
        PCIField.register_lookup(lookup_class)


class PCITextField(PCIField, models.TextField):
    pass


class PCICharField(PCIField, models.CharField):
    pass


class PCIEmailField(PCIField, models.EmailField):
    pass


class PCIIntegerField(PCIField, models.IntegerField):
    def from_db_value(self, value, expression, connection, *args):
        if value is not None:
            return self.to_python(int(self.de_tokenize(value)))


class PCIDateField(PCIField, models.DateField):
    pass


class PCIDateTimeField(PCIField, models.DateTimeField):
    pass