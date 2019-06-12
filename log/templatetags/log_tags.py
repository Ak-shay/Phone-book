from django import template
from log.models import Call, Contact

register = template.Library()

@register.simple_tag
def call_name(call, user):
    return call.saved_name(user)