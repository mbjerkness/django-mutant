
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _

from dynamodef.models.field import FieldDefinition
from django.core.exceptions import ValidationError

class EmailFieldDefinition(FieldDefinition):
    
    class Meta:
        app_label = 'dynamodef'
        proxy = True
        defined_field_class = fields.EmailField
        defined_field_category = _(u'web')
        
class URLFieldDefinition(FieldDefinition):
    
    class Meta:
        app_label = 'dynamodef'
        proxy = True
        defined_field_class = fields.URLField
        defined_field_category = _(u'web')
        
class SlugFieldDefinition(FieldDefinition):
    
    class Meta:
        app_label = 'dynamodef'
        proxy = True
        defined_field_class = fields.SlugField
        defined_field_category = _(u'web')
        
    @classmethod
    def get_field_description(cls):
        return _("Slug (up to 255)")
        
class IPAddressFieldDefinition(FieldDefinition):
    
    class Meta:
        app_label = 'dynamodef'
        proxy = True
        defined_field_class = fields.IPAddressField
        defined_field_category = _(u'web')

# We should eat our own dogfood and
# provide those options as FieldDefinitionOptionChoice initial_data
# fixture
try:
    # Django 1.4+
    GenericIPAddressField = fields.GenericIPAddressField
except AttributeError:
    pass
else:
    PROTOCOL_CHOICES = (('both', _(u'both')),
                        ('IPv4', _(u'IPv4')),
                        ('IPv6', _(u'IPv6')))
    
    protocol_help_text = _(u'Limits valid inputs to the specified protocol.')
    
    unpack_ipv4_help_text = _(u'Unpacks IPv4 mapped addresses like '
                              u'``::ffff::192.0.2.1`` to ``192.0.2.1``')
    
    class GenericIPAddressFieldDefinition(FieldDefinition):
        
        protocol = fields.CharField(_(u'protocol'), max_length=4,
                                    choices=PROTOCOL_CHOICES, default='both')
        
        unpack_ipv4 = fields.BooleanField(_(u'unpack ipv4'), default=False)
        
        class Meta:
            app_label = 'dynamodef'
            defined_field_class = GenericIPAddressField
            defined_field_options = ('protocol', 'unpack_ipv4',)
            defined_field_category = _(u'web')
            
        def clean(self):
            if self.unpack_ipv4 and self.procotol != 'both':
                msg = _(u"Can only be used when ``protocol`` is set to 'both'.")
                raise ValidationError({'unpack_ipv4': msg})
