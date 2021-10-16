from django.db import models
from django.conf import settings



from django.utils.translation import gettext_lazy as _
from django.core import exceptions
import re
from django.core.validators import RegexValidator, MaxLengthValidator, MaxValueValidator, MinLengthValidator
from fernet_fields import EncryptedCharField, EncryptedIntegerField
from allauth.account.models import EmailAddress

from .country_data import ISO_3166_CODES, POSTCODES_REGEX
from django.core.exceptions import ValidationError

# Create your models here.
# --------------------------------------------
#
# --------------------------------------------

# https://github.com/django-oscar/django-oscar/blob/master/src/oscar/apps/address/abstract_models.py

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                     "allowed.")
'''
todo

class Profile(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE,
                                primary_key=True)
it is recommended that you set the primary_key explicitly to True to prevent concurrency issues in some database 
backends such as PostgreSQL. 


While designing the profile model, 
it is recommended that all the profile detail fields must be nullable or contain default values.


'''
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    # language = models.CharField(max_length=2)
    father_name = models.CharField(max_length=100, blank=True, default="")
    mother_name = models.CharField(max_length=100, blank=True, default="")
    pan = EncryptedCharField(max_length=10, blank=True, default="", validators=[MaxLengthValidator(10), ])
    aadhaar_number = EncryptedCharField(max_length=12, default="", blank=True, validators=[MaxLengthValidator(10), ])
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    mobile_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                     null=True)  # validators should be a list
    home_phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                         null=True)  # validators should be a list
    def __str__(self):
        return self.user.username


# --------------------------------------------------------
#
# --------------------------------------------------------

class Address(models.Model):
    class Types(models.TextChoices):
        HOME = 'H', _('Home')
        SHIPPING = 'S', _('Shipping')
        OFFICE = 'O', _('Office')
        BILLING = 'B', _('Billing')


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='addresses')

    type = models.CharField(max_length=1, choices=Types.choices, default=Types.HOME)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=3, choices=ISO_3166_CODES)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def clean(self):
        # Ensure postcodes are valid for country
        self.ensure_postcode_is_valid_for_country()

    def ensure_postcode_is_valid_for_country(self):
        """
        Validate postcode given the country
        """


        if self.postcode and self.country:
            # Ensure postcodes are always uppercase
            postcode = self.postcode.upper().replace(' ', '')

            regex = self.POSTCODES_REGEX.get(self.country, None)

            # Validate postcode against regex for the country if available
            if regex and not re.match(regex, postcode):
                msg = _("The postcode '%(postcode)s' is not valid "
                        "for %(country)s") \
                      % {'postcode': self.postcode,
                         'country': self.country}
                raise exceptions.ValidationError(
                    {'postcode': [msg]})

    def __str__(self):
        return '{}:{}'.format(Address.Types(self.type).label, self.address1)


# --------------------------------------------------------
#
# --------------------------------------------------------
class Phone(models.Model):
    class Types(models.TextChoices):
        HOME = 'H', _('Home')
        MOBILE = 'M', _('Mobile')
        OFFICE = 'O', _('Office')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='phones')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")

    type = models.CharField(max_length=1, choices=Types.choices, default=Types.MOBILE)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}:{}'.format(Phone.Types(self.type).label, self.phone_number)


# --------------------------------------------------------
# https://github.com/pennersr/django-allauth/blob/353386216b79f16709e97bb487c0bbbba2bc0c71/allauth/account/models.py#L18
# --------------------------------------------------------
class Email(models.Model):

    class Types(models.TextChoices):
        PERSONAL = 'P', _('Personal')
        OFFICIAL = 'O', _('Official')

    email_address = models.OneToOneField(EmailAddress, on_delete=models.CASCADE, related_name='type')

    type = models.CharField(max_length=1, choices=Types.choices)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}:{}'.format(Email.Types(self.type).label, self.email_address.email)

    # def clean(self):
    #     print("<><><><><><> NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
    #     raise ValidationError(
    #         _('Invalid value: %(value)s'),
    #         params={'value': '42'},
    #     )


class Bank(models.Model):
    bank_name = models.CharField(max_length=100,db_index=True,blank=True, null=True)
    ifsc_code = models.CharField(max_length=11,db_index=True,blank=True, null=True, unique=True)
    micr = models.CharField(max_length=9, blank=True, null=True)
    branch_name =models.CharField(max_length=100,blank=True, null=True)
    address= models.CharField(max_length=200,blank=True, null=True)
    city= models.CharField(max_length=100,db_index=True,blank=True, null=True   )
    district = models.CharField(max_length=100,blank=True, null=True)
    state = models.CharField(max_length=50,db_index=True,blank=True, null=True)
    phone = models.CharField(max_length=12,blank=True, null=True)

# --------------------------------------------------------
#
# --------------------------------------------------------
class Card(models.Model):
    class Types(models.TextChoices):
        DEBIT = 'D', _('Debit')
        CREDIT = 'C', _('Credit')

    card_number_regex_validator = RegexValidator(
        regex=r'^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$',
        message=_("Please enter a valid Card number (16 to 20 numeric digits)"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cards')

    type = models.CharField(max_length=1, choices=Types.choices, default=Types.DEBIT)
    name_on_card = models.CharField(max_length=100)
    card_number = EncryptedCharField(max_length=20, validators=[card_number_regex_validator])
    expiry_date = models.CharField(max_length=5)
    cvv = EncryptedIntegerField(validators=[MaxValueValidator(9999)])
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}:{}'.format(Card.Types(self.type).label, self.card_number[-4:])





# --------------------------------------------------------
#
# --------------------------------------------------------
class BankAccount(models.Model):
    class Types(models.TextChoices):
        SAVING = 'S', _('Saving')
        CURRENT = 'C', _('CURRENT')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bank_accounts')

    type = models.CharField(max_length=1, choices=Types.choices, default=Types.CURRENT)
    bank_name = models.CharField(max_length=100)

    holder_name = models.CharField(max_length=100)
    account_number = EncryptedCharField(max_length=100)
    ifsc_code = models.CharField(max_length=11)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}:{}:{}'.format(BankAccount.Types(self.type).label, self.bank_name, self.account_number[-4:])

# # --------------------------------------------------------
# #  Bank List http://www.vsbank.co.in/download/ifsc%20code%20list.pdf
# # --------------------------------------------------------




# rating


# orders


class BooleanSettings(models.Model):
    class AllowedSettings(models.TextChoices):
        TWO_FACTOR = 'TWO_FACTOR', _('Enable Two-Factor authentication ?')
        GENERATE_INVOICE = 'GENERATE_INVOICE', _('Generate invoice for each Transaction?')

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="booleansettings",
                             null=False, blank=False
                             )
    key = models.CharField(max_length=50, choices=AllowedSettings.choices, null=False, blank=False,
                           verbose_name="Setting")
    value = models.BooleanField(verbose_name="Enabled", default=False, blank=False, null=False)

    class Meta:
        ordering = ['user', 'key']
        constraints = [
            models.UniqueConstraint(fields=['user', 'key'], name='User unique Setting')
        ]

    def __str__(self):
        return self.key;

    @staticmethod
    def load(user):
        for setting in BooleanSettings.AllowedSettings:
            boolean_setting = BooleanSettings.objects.filter(user=user).filter(key=setting).first()
            if not boolean_setting:
                boolean_setting = BooleanSettings(user=user, key=setting)
                boolean_setting.save()