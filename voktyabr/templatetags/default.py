
from django import template
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from datetime import date

register = template.Library()


class set_var_node(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = _(var_name)
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError(
            "'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return set_var_node(parts[1], parts[3])

register.tag('set', set_var)


@register.tag
def make_list(parser, token):
    bits = list(token.split_contents())
    if len(bits) >= 4 and bits[-2] == "as":
        varname = bits[-1]
        items = bits[1:-2]
        return make_list_none(items, varname)
    else:
        raise template.TemplateSyntaxError(
            "%r expected format is 'item [item ...] as varname'" % bits[0])


class make_list_none(template.Node):

    def __init__(self, items, varname):
        self.items = map(template.Variable, items)
        self.varname = varname

    def render(self, context):
        context[self.varname] = [i.resolve(context) for i in self.items]
        return ""


@register.inclusion_tag("breadcrumbs.html", takes_context=False)
def breadcrumbs(list):
    return {"list": list}


@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    return qty * unit_price
